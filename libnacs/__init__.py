#

from . import handle

nacs_seq_bin_to_bytecode = handle.nacs_seq.nacs_seq_bin_to_bytecode
nacs_seq_bin_to_bytecode.restype = ctypes.c_char_p
f.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_c_size_t,
              ctypes.POINTER(ctypes.c_c_size_t)]

PyBytes_FromStringAndSize = ctypes.pythonapi['PyBytes_FromStringAndSize']
PyBytes_FromStringAndSize.restype = ctypes.py_object
PyBytes_FromStringAndSize.argtypes = [ctypes.c_char_p, ctypes.c_ssize_t]

free = handle.libc['free']
free.restype = None
free.argtypes = [ctypes.c_void_p]

def bin_to_bytecode(bin):
    outsize = ctypes.c_c_size_t()
    ptr = nacs_seq_bin_to_bytecode(ctypes.c_int.from_buffer(bin), len(bin),
                                   ctypes.byref(outsize))
    b = PyBytes_FromStringAndSize(ptr, outsize.value)
    free(ptr)
    return b