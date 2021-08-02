#

from . import handle
import ctypes
from enum import IntEnum
import io
import struct
import array

nacs_seq_new_manager = handle.nacs_seq.nacs_seq_new_manager
nacs_seq_new_manager.restype = ctypes.c_void_p
nacs_seq_new_manager.argtypes = []

nacs_seq_free_manager = handle.nacs_seq.nacs_seq_free_manager
nacs_seq_free_manager.restype = None
nacs_seq_free_manager.argtypes = [ctypes.c_void_p]

nacs_seq_manager_tick_per_sec = handle.nacs_seq.nacs_seq_manager_tick_per_sec
nacs_seq_manager_tick_per_sec.restype = ctypes.c_int64
nacs_seq_manager_tick_per_sec.argtypes = [ctypes.c_void_p]

nacs_seq_manager_take_messages = handle.nacs_seq.nacs_seq_manager_take_messages
nacs_seq_manager_take_messages.restype = ctypes.POINTER(ctypes.c_uint8)
nacs_seq_manager_take_messages.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]

nacs_seq_manager_enable_debug = handle.nacs_seq.nacs_seq_manager_enable_debug
nacs_seq_manager_enable_debug.restype = None
nacs_seq_manager_enable_debug.argtypes = [ctypes.c_void_p, ctypes.c_bool]

nacs_seq_manager_debug_enabled = handle.nacs_seq.nacs_seq_manager_debug_enabled
nacs_seq_manager_debug_enabled.restype = ctypes.c_bool
nacs_seq_manager_debug_enabled.argtypes = [ctypes.c_void_p]

nacs_seq_manager_enable_dump = handle.nacs_seq.nacs_seq_manager_enable_dump
nacs_seq_manager_enable_dump.restype = None
nacs_seq_manager_enable_dump.argtypes = [ctypes.c_void_p, ctypes.c_bool]

nacs_seq_manager_dump_enabled = handle.nacs_seq.nacs_seq_manager_dump_enabled
nacs_seq_manager_dump_enabled.restype = ctypes.c_bool
nacs_seq_manager_dump_enabled.argtypes = [ctypes.c_void_p]

nacs_seq_manager_create_sequence = handle.nacs_seq.nacs_seq_manager_create_sequence
nacs_seq_manager_create_sequence.restype = ctypes.c_void_p
nacs_seq_manager_create_sequence.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]

nacs_seq_manager_free_sequence = handle.nacs_seq.nacs_seq_manager_free_sequence
nacs_seq_manager_free_sequence.restype = None
nacs_seq_manager_free_sequence.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

nacs_seq_manager_load_config_file = handle.nacs_seq.nacs_seq_manager_load_config_file
nacs_seq_manager_load_config_file.restype = None
nacs_seq_manager_load_config_file.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

nacs_seq_manager_load_config_string = handle.nacs_seq.nacs_seq_manager_load_config_string
nacs_seq_manager_load_config_string.restype = None
nacs_seq_manager_load_config_string.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

nacs_seq_manager_expseq_init_run = handle.nacs_seq.nacs_seq_manager_expseq_init_run
nacs_seq_manager_expseq_init_run.restype = None
nacs_seq_manager_expseq_init_run.argtypes = [ctypes.c_void_p]

nacs_seq_manager_expseq_pre_run = handle.nacs_seq.nacs_seq_manager_expseq_pre_run
nacs_seq_manager_expseq_pre_run.restype = None
nacs_seq_manager_expseq_pre_run.argtypes = [ctypes.c_void_p]

nacs_seq_manager_expseq_start = handle.nacs_seq.nacs_seq_manager_expseq_start
nacs_seq_manager_expseq_start.restype = None
nacs_seq_manager_expseq_start.argtypes = [ctypes.c_void_p]

nacs_seq_manager_expseq_cancel = handle.nacs_seq.nacs_seq_manager_expseq_cancel
nacs_seq_manager_expseq_cancel.restype = None
nacs_seq_manager_expseq_cancel.argtypes = [ctypes.c_void_p]

nacs_seq_manager_expseq_wait = handle.nacs_seq.nacs_seq_manager_expseq_wait
nacs_seq_manager_expseq_wait.restype = ctypes.c_bool
nacs_seq_manager_expseq_wait.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

nacs_seq_manager_expseq_post_run = handle.nacs_seq.nacs_seq_manager_expseq_post_run
nacs_seq_manager_expseq_post_run.restype = ctypes.c_uint32
nacs_seq_manager_expseq_post_run.argtypes = [ctypes.c_void_p]

nacs_seq_manager_expseq_get_global = handle.nacs_seq.nacs_seq_manager_expseq_get_global
nacs_seq_manager_expseq_get_global.restype = ctypes.c_double
nacs_seq_manager_expseq_get_global.argtypes = [ctypes.c_void_p, ctypes.c_uint32]

nacs_seq_manager_expseq_set_global = handle.nacs_seq.nacs_seq_manager_expseq_set_global
nacs_seq_manager_expseq_set_global.restype = None
nacs_seq_manager_expseq_set_global.argtypes = [ctypes.c_void_p, ctypes.c_uint32,
                                               ctypes.c_double]

nacs_seq_manager_expseq_cur_bseq_length = handle.nacs_seq.nacs_seq_manager_expseq_cur_bseq_length
nacs_seq_manager_expseq_cur_bseq_length.restype = ctypes.c_uint64
nacs_seq_manager_expseq_cur_bseq_length.argtypes = [ctypes.c_void_p]

nacs_seq_manager_expseq_get_builder_dump = handle.nacs_seq.nacs_seq_manager_expseq_get_builder_dump
nacs_seq_manager_expseq_get_builder_dump.restype = ctypes.POINTER(ctypes.c_uint8)
nacs_seq_manager_expseq_get_builder_dump.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]

nacs_seq_manager_expseq_get_seq_dump = handle.nacs_seq.nacs_seq_manager_expseq_get_seq_dump
nacs_seq_manager_expseq_get_seq_dump.restype = ctypes.POINTER(ctypes.c_uint8)
nacs_seq_manager_expseq_get_seq_dump.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]

nacs_seq_manager_expseq_get_seq_opt_dump = handle.nacs_seq.nacs_seq_manager_expseq_get_seq_opt_dump
nacs_seq_manager_expseq_get_seq_opt_dump.restype = ctypes.POINTER(ctypes.c_uint8)
nacs_seq_manager_expseq_get_seq_opt_dump.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]

nacs_seq_manager_expseq_get_nidaq_data = handle.nacs_seq.nacs_seq_manager_expseq_get_nidaq_data
nacs_seq_manager_expseq_get_nidaq_data.restype = ctypes.POINTER(ctypes.c_double)
nacs_seq_manager_expseq_get_nidaq_data.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                                   ctypes.POINTER(ctypes.c_size_t)]

class ChannelInfo(ctypes.Structure):
    _fields_ = [('id', ctypes.c_uint32),
                ('name', ctypes.c_char_p)]

nacs_seq_manager_expseq_get_nidaq_channel_info = handle.nacs_seq.nacs_seq_manager_expseq_get_nidaq_channel_info
nacs_seq_manager_expseq_get_nidaq_channel_info.restype = ctypes.POINTER(ChannelInfo)
nacs_seq_manager_expseq_get_nidaq_channel_info.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                                           ctypes.POINTER(ctypes.c_uint32)]

nacs_seq_manager_expseq_get_zynq_bytecode = handle.nacs_seq.nacs_seq_manager_expseq_get_zynq_bytecode
nacs_seq_manager_expseq_get_zynq_bytecode.restype = ctypes.POINTER(ctypes.c_uint8)
nacs_seq_manager_expseq_get_zynq_bytecode.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                                      ctypes.POINTER(ctypes.c_size_t)]

class ZynqClock(ctypes.Structure):
    _fields_ = [('time', ctypes.c_int64),
                ('period', ctypes.c_uint8)]

nacs_seq_manager_expseq_get_zynq_clock = handle.nacs_seq.nacs_seq_manager_expseq_get_zynq_clock
nacs_seq_manager_expseq_get_zynq_clock.restype = ctypes.POINTER(ZynqClock)
nacs_seq_manager_expseq_get_zynq_clock.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                                   ctypes.POINTER(ctypes.c_uint32)]

free = handle.libc['free']
free.restype = None
free.argtypes = [ctypes.c_void_p]

class Error:
    def __init__(self, msg, _type, code, type1, id1, type2, id2):
        self.msg = msg
        self.type = _type
        self.code = code
        self.type1 = type1
        self.id1 = id1
        self.type2 = type2
        self.id2 = id2

class ExpSeq:
    def __init__(self, mgr, ptr):
        self._ptr = ptr
        self.__mgr = mgr

    def __del__(self):
        try:
            nacs_seq_manager_free_sequence(self.__mgr._ptr, self._ptr)
        except:
            self.__mgr.check_message(True)
            raise
        self.__mgr.check_message()

    def guarded(func):
        def f(self, *args, **kwargs):
            try:
                res = func(self, *args, **kwargs)
            except:
                self.__mgr.check_message(True)
                raise
            self.__mgr.check_message()
            return res
        return f

    @guarded
    def init_run(self):
        nacs_seq_manager_expseq_init_run(self._ptr)

    @guarded
    def pre_run(self):
        nacs_seq_manager_expseq_pre_run(self._ptr)

    @guarded
    def start(self):
        nacs_seq_manager_expseq_start(self._ptr)

    @guarded
    def cancel(self):
        nacs_seq_manager_expseq_cancel(self._ptr)

    @guarded
    def wait(self, timeout_ms):
        return nacs_seq_manager_expseq_wait(self._ptr, timeout_ms)

    @guarded
    def post_run(self):
        return nacs_seq_manager_expseq_post_run(self._ptr)

    @guarded
    def get_global(self, idx):
        return nacs_seq_manager_expseq_get_global(self._ptr, idx)

    @guarded
    def set_global(self, idx, val):
        nacs_seq_manager_expseq_set_global(self._ptr, idx, val)

    @guarded
    def cur_bseq_length(self):
        return nacs_seq_manager_expseq_cur_bseq_length(self._ptr)

    def get_builder_dump(self):
        out_size = ctypes.c_size_t()
        ptr = nacs_seq_manager_expseq_get_builder_dump(self._ptr, out_size)
        if not ptr or out_size.value == 0:
            return
        return ctypes.string_at(ptr, out_size.value).decode()

    def get_seq_dump(self):
        out_size = ctypes.c_size_t()
        ptr = nacs_seq_manager_expseq_get_seq_dump(self._ptr, out_size)
        if not ptr or out_size.value == 0:
            return
        return ctypes.string_at(ptr, out_size.value).decode()

    def get_seq_opt_dump(self):
        out_size = ctypes.c_size_t()
        ptr = nacs_seq_manager_expseq_get_seq_opt_dump(self._ptr, out_size)
        if not ptr or out_size.value == 0:
            return
        return ctypes.string_at(ptr, out_size.value).decode()

    @guarded
    def get_nidaq_data(self, name):
        out_size = ctypes.c_size_t()
        ptr = nacs_seq_manager_expseq_get_nidaq_data(self._ptr, name.encode(), out_size)
        if not ptr:
            return
        ptr = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double * out_size.value))
        return array.array('d', ptr[0])

    @guarded
    def get_nidaq_channel_info(self, name):
        out_size = ctypes.c_uint32()
        ptr = nacs_seq_manager_expseq_get_nidaq_channel_info(self._ptr, name.encode(), out_size)
        if not ptr:
            return
        return [(v.id, v.name.decode()) for v in ptr[:out_size.value]]

    @guarded
    def get_zynq_bytecode(self, name):
        out_size = ctypes.c_size_t()
        ptr = nacs_seq_manager_expseq_get_zynq_bytecode(self._ptr, name.encode(), out_size)
        if not ptr:
            return
        ptr = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_uint8 * out_size.value))
        return array.array('B', ptr[0])

    @guarded
    def get_zynq_clock(self, name):
        out_size = ctypes.c_uint32()
        ptr = nacs_seq_manager_expseq_get_zynq_clock(self._ptr, name.encode(), out_size)
        if not ptr:
            return
        return [(v.time, v.period) for v in ptr[:out_size.value]]

    del guarded

class MsgType(IntEnum):
    Info = 0
    Warn = 1
    Error = 2
    SeqError = 3
    Debug = 4

def _default_logger(msgtyp, msg):
    print(msg, end='')

def unpack(stream, fmt):
    size = struct.calcsize(fmt)
    buf = stream.read(size)
    return struct.unpack(fmt, buf)

def unpack_msg_str(stream):
    sz, = unpack(stream, '=I')
    return stream.read(sz).decode()

class Manager:
    def __init__(self):
        self._ptr = nacs_seq_new_manager()
        self.__logger = _default_logger

    def __del__(self):
        nacs_seq_free_manager(self._ptr)

    def info(self, t, msg):
        self.__logger(MsgType.Info, msg)

    def warn(self, t, msg):
        self.__logger(MsgType.Warn, msg)

    def error(self, t, msg):
        self.__logger(MsgType.Error, msg)

    def debug(self, t, msg):
        self.__logger(MsgType.Debug, msg)

    def check_message(self, extern_err=False):
        out_size = ctypes.c_size_t()
        ptr = nacs_seq_manager_take_messages(self._ptr, out_size)
        if not ptr or out_size.value == 0:
            return
        stream = io.BytesIO(ctypes.string_at(ptr, out_size.value))
        free(ptr)
        msgs = []
        error_idx = -1
        while True:
            msgtyp = stream.read(1)
            if not msgtyp:
                break
            msgtyp = msgtyp[0]
            if msgtyp == MsgType.Info:
                t, = unpack(stream, '=Q')
                msgs.append((MsgType.Info, t, unpack_msg_str(stream)))
            elif msgtyp == MsgType.Warn:
                t, = unpack(stream, '=Q')
                msgs.append((MsgType.Warn, t, unpack_msg_str(stream)))
            elif msgtyp == MsgType.Error:
                t, = unpack(stream, '=Q')
                error_idx = len(msgs)
                msgs.append((MsgType.Error, t, unpack_msg_str(stream)))
            elif msgtyp == MsgType.SeqError:
                t, = unpack(stream, '=Q')
                error_idx = len(msgs)
                _type, = unpack(stream, '=B')
                code, = unpack(stream, '=H')
                type1, = unpack(stream, '=B')
                id1, = unpack(stream, '=Q')
                type2, = unpack(stream, '=B')
                id2, = unpack(stream, '=Q')
                err = Error(unpack_msg_str(stream), _type, code, type1, id1, type2, id2)
                msgs.append((MsgType.SeqError, t, err))
            elif msgtyp == MsgType.Debug:
                t, = unpack(stream, '=Q')
                msgs.append((MsgType.Debug, t, unpack_msg_str(stream)))
            else:
                self.warn(f'Unknown message type: {msgtyp}')

        # The caller wants to raise an exception, so we don't need to throw anything.
        # This happens if the c function throws something that python can catch
        # (happens on windows).
        if extern_err:
            error_idx = -1

        for (i, (msgtyp, t, msg)) in enumerate(msgs):
            if msgtyp == MsgType.Info:
                self.info(t, msg)
            elif msgtyp == MsgType.Warn:
                self.warn(t, msg)
            elif msgtyp == MsgType.Error:
                if error_idx == i:
                    continue
                # Error messages have no extra new lines at the end.
                self.error(t, msg + '\n')
            elif msgtyp == MsgType.SeqError:
                if error_idx == i:
                    continue
                # Error messages have no extra new lines at the end.
                self.error(t, msg.msg + '\n')
            elif msgtyp == MsgType.Debug:
                self.debug(t, msg)

        if error_idx >= 0:
            msgtyp, t, error = msgs[error_idx]
            if msgtyp == MsgType.Error:
                error = RuntimeError(error)
            raise error

    def guarded(func):
        def f(self, *args, **kwargs):
            try:
                res = func(self, *args, **kwargs)
            except:
                self.check_message(True)
                raise
            self.check_message()
            return res
        return f

    @guarded
    def tick_per_sec(self):
        return nacs_seq_manager_tick_per_sec(self._ptr)

    @guarded
    def create_sequence(self, data):
        ptr = nacs_seq_manager_create_sequence(self._ptr,
                                               ctypes.c_uint8.from_buffer(data), len(data))
        if not ptr:
            return
        # Construct the object before checking for error to make sure that
        # the pointer is freed even if there's an unexpected error.
        return ExpSeq(self, ptr)

    @guarded
    def load_config_file(self, fname):
        nacs_seq_manager_load_config_file(self._ptr, fname.encode())

    @guarded
    def load_config_string(self, config):
        nacs_seq_manager_load_config_string(self._ptr, config.encode())

    def enable_debug(self, enable):
        nacs_seq_manager_enable_debug(self._ptr, enable)

    def debug_enabled(self):
        return nacs_seq_manager_debug_enabled(self._ptr)

    def enable_dump(self, enable):
        nacs_seq_manager_enable_dump(self._ptr, enable)

    def dump_enabled(self):
        return nacs_seq_manager_dump_enabled(self._ptr)

    del guarded
