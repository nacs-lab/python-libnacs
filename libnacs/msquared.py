#!/usr/bin/python

# Copyright (c) 2019 - 2019 Yichao Yu <yyc1992@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not,
# see <http://www.gnu.org/licenses/>.

import asyncio
import concurrent.futures
from enum import Enum
import json
import threading
import time

class JSONStream:
    def __init__(self):
        self.__buff = ''
        self.__decoder = json.JSONDecoder()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            obj, pos = self.__decoder.raw_decode(self.__buff)
        except json.JSONDecodeError as e:
            # If the error happens past the last character, we have an incomplete object.
            # Stash it and continue. Otherwise:
            if e.pos != len(self.__buff):
                # Shouldn't really happen but if it does, throw away invalid data.
                self.__buff = ''
            raise StopIteration
        self.__buff = self.__buff[pos:].lstrip()
        return obj

    def add_bytes(self, data):
        if self.__buff:
            self.__buff += data.decode()
        else:
            self.__buff = data.decode().lstrip()

class MSquaredProtocol(asyncio.Protocol):
    def __init__(self):
        loop = asyncio.get_running_loop()
        self.__done = loop.create_future()
        self.__transport = None
        # 2**29. The max ID acceptable is (2**31 - 2)
        # this means that we are only wasting 25% of the good range
        # This avoid overlapping with the messages automatically generated by the server
        # (negative numbers also seems to work but this is currently good enough...)
        self.__id = 536870912
        self.__json = JSONStream()
        self.__handlers = []
        self.__background_task = None
        self.do_ping = True
        self.print_message = False
        self.print_data = False

    async def __background(self):
        while True:
            await asyncio.sleep(1)
            if self.do_ping:
                self.send_raw('ping', dict(text_in="Ping"))
            t = time.time()
            i = 0
            while i < len(self.__handlers):
                if self.__handlers[i][1] < t:
                    try:
                        self.__handlers.pop(i)[0].timeout()
                    except Exception as e:
                        print(e)
                i += 1

    def connection_made(self, transport):
        self.__transport = transport
        self.__background_task = asyncio.shield(self.__background())

    def data_received(self, data):
        if self.print_data:
            print(data)
        self.__json.add_bytes(data)
        for obj in self.__json:
            if self.print_message:
                print(obj)
            try:
                msg = obj['message']
                param = msg['parameters'] if 'parameters' in msg else {}
                self.message_recieved(msg['op'], msg['transmission_id'][0], param)
            except Exception as e:
                print(e)

    def message_recieved(self, op, tid, msg):
        for i in range(len(self.__handlers)):
            try:
                if not self.__handlers[i][0].process_msg(op, tid, msg):
                    continue
            except Exception as e:
                print(e)
                continue
            if self.__handlers[i][0].done():
                self.__handlers.pop(i)
            break

    def add_handler(self, future, timeout=30):
        self.__handlers.append((future, time.time() + timeout))

    def connection_lost(self, exc):
        self.__transport.close()
        self.__background_task.cancel()
        self.__done.set_result(True)

    def next_id(self):
        tid = self.__id
        self.__id += 1
        return tid

    def send_raw(self, op, params, transmission_id=None):
        if transmission_id is not None:
            tid = transmission_id
        elif op == 'ping':
            # Don't do useless counting with `ping`.
            tid = 0
        else:
            tid = self.__id
            self.__id += 1
        if params:
            msg = (b'{"message":{"transmission_id":[' + str(tid).encode() + b'],"op":"' +
                       op.encode() + b'","parameters":' +
                       json.dumps(params, separators=(',', ':')).encode() + b'}}')
        else:
            msg = (b'{"message":{"transmission_id":[' + str(tid).encode() + b'],"op":"' +
                       op.encode() + b'"}}')
        self.__transport.write(msg)

    def done(self):
        return self.__done

    def stop(self):
        self.__transport.close()

class MSquared:
    class State(Enum):
        Stopped = 0
        Starting = 1
        Started = 2
        Stopping = 3

    class Reply(concurrent.futures.Future):
        def __init__(self, cmd, tid, has_final):
            super().__init__()
            self.__cmd = cmd
            self.__tid = tid
            self.__has_final = has_final
            self.__reply = None

        def process_msg(self, op, tid, msg):
            if op == self.__cmd + '_reply':
                if not self.__has_final:
                    self.set_result(msg)
                    return True
                if 'status' in msg and msg['status'] != [0]:
                    self.set_result({'reply': msg})
                    return True
                self.__reply = msg
                return True
            elif op == self.__cmd + '_f_r' and self.__reply is not None:
                self.set_result({'reply': self.__reply, 'final': msg})
                return True
            elif tid == self.__tid and op == 'parse_fail':
                self.set_result({'parse_fail': msg})
                return True
            return False

        def timeout(self):
            if self.__reply is not None:
                self.set_result({'reply': self.__reply})
            else:
                self.set_result({})

    def run_on_worker(func):
        def f(self, *args, **kwargs):
            async def func1():
                await self.__initialized
                return func(self, *args, **kwargs)
            future = asyncio.run_coroutine_threadsafe(func1(), self.__loop)
            try:
                return future.result()
            except concurrent.futures.CancelledError:
                return
        return f

    @run_on_worker
    def cmd(self, name, report=False, **params):
        tid = self.__protocol.next_id()
        reply = self.Reply(name, tid, report)
        self.__protocol.add_handler(reply)
        if report:
            params['report'] = 'finished'
        self.__protocol.send_raw(name, params, transmission_id=tid)
        return reply

    def __init__(self, addr, host_addr):
        self.__addr = addr
        self.__host_addr = host_addr
        self.__loop = None
        self.__initialized = None
        self.__protocol = None
        self.__worker = None
        self.__state = self.State.Stopped
        self.__init_cv = threading.Condition()
        self.__do_ping = True
        self.__print_message = False
        self.__print_data = False
        self.start()

    @run_on_worker
    def send_raw(self, *args, **kwargs):
        self.__protocol.send_raw(*args, **kwargs)

    def move_wave(self, wl):
        return self.cmd('move_wave_t', True, wavelength=[wl])

    def poll_move_wave(self):
        return self.cmd('poll_move_wave_t')

    def tune_etalon(self, percent):
        return self.cmd('tune_etalon', True, setting=[percent])

    def tune_resonator(self, percent):
        return self.cmd('tune_resonator', True, setting=[percent])

    def fine_tune_resonator(self, percent):
        return self.cmd('fine_tune_resonator', True, setting=[percent])

    def etalon_lock(self, on):
        return self.cmd('etalon_lock', True, operation="on" if on else "off")

    def etalon_lock_status(self):
        return self.cmd('etalon_lock_status')

    def select_etalon_profile(self, profile):
        return self.cmd('select_profile', profile=[profile])

    def system_status(self):
        return self.cmd('get_status')

    def alignment_status(self):
        return self.cmd('get_alignment_status')

    def set_alignment_mode(self, mode):
        return self.cmd('beam_alignment', True, mode=[mode])

    def alignment_adjust_x(self, val):
        return self.cmd('beam_adjust_x', True, x_value=[val])

    def alignment_adjust_y(self, val):
        return self.cmd('beam_adjust_y', True, y_value=[val])

    def wavelength_range(self):
        return self.cmd('get_wavelength_range')

    @run_on_worker
    def __sync_props(self):
        # The control thread waits for this and there's no need for synchronization
        self.__protocol.do_ping = self.__do_ping
        self.__protocol.print_message = self.__print_message
        self.__protocol.print_data = self.__print_data

    def __new_protocol(self):
        res = MSquaredProtocol()
        with self.__init_cv:
            res.do_ping = self.__do_ping
            res.print_message = self.__print_message
            res.print_data = self.__print_data
        return res

    @property
    def do_ping(self):
        return self.__do_ping

    @do_ping.setter
    def do_ping(self, do_ping):
        self.__do_ping = do_ping
        if self.__loop is not None:
            self.__sync_props()

    @property
    def print_message(self):
        return self.__print_message

    @print_message.setter
    def print_message(self, print_message):
        self.__print_message = print_message
        if self.__loop is not None:
            self.__sync_props()

    @property
    def print_data(self):
        return self.__print_data

    @print_data.setter
    def print_data(self, print_data):
        self.__print_data = print_data
        if self.__loop is not None:
            self.__sync_props()

    async def __run(self):
        self.__loop = asyncio.get_running_loop()
        self.__initialized = self.__loop.create_future()
        with self.__init_cv:
            if self.__state != self.State.Starting:
                return
            self.__state = self.State.Started
            self.__init_cv.notify_all()

        try:
            transport, self.__protocol = await self.__loop.create_connection(
                self.__new_protocol, *self.__addr)
        except:
            await asyncio.sleep(1)
            return

        self.__protocol.send_raw('start_link', dict(ip_address=self.__host_addr))
        self.__initialized.set_result(True)

        try:
            await self.__protocol.done()
        finally:
            pass

    def __worker_fun(self):
        while True:
            asyncio.run(self.__run())
            with self.__init_cv:
                if self.__state == self.State.Stopping:
                    return
                self.__state = self.State.Starting

    def start(self):
        # `__worker` is only written to by the controller thread. no need for synchronization
        if self.__worker is not None:
            return
        with self.__init_cv:
            self.__state = self.State.Starting
            self.__worker = threading.Thread(target = self.__worker_fun)
            self.__worker.start()
            self.__init_cv.wait_for(lambda: self.__state == self.State.Started)

    @run_on_worker
    def __req_stop(self):
        self.__protocol.stop()

    def stop(self):
        if self.__worker is None:
            return
        # `__state` can be `Starting` or `Started`
        # The worker thread checks the state before changing it
        # and the `__req_stop` below forces a state change so we should stop it soon enough
        with self.__init_cv:
            self.__state = self.State.Stopping
        self.__req_stop()
        self.__worker.join()
        self.__worker = None
        self.__state = self.State.Stopped

    @staticmethod
    def wait(res, timeout=1):
        try:
            return res.result(timeout)
        except concurrent.futures.TimeoutError:
            return
        except concurrent.futures.CancelledError:
            return {'cancel': True}

    del run_on_worker
