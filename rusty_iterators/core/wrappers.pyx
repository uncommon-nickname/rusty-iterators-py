cimport cython
from rusty_iterators.core.interface cimport IterInterface
from rusty_iterators.core.async_interface cimport AsyncIterInterface

@cython.final
cdef class SeqWrapper(IterInterface):
    cdef object s
    cdef int ptr

    def __init__(self, object s):
        self.s = s
        self.ptr = 0

    def __str__(self):
        return f"SeqWrapper(ptr={self.ptr}, s={len(self.s)})"

    cpdef bint can_be_copied(self):
        return True

    cpdef copy(self):
        obj = SeqWrapper(self.s)
        obj.ptr = self.ptr
        return obj

    cpdef next(self):
        try:
            item = self.s[self.ptr]
        except IndexError as exc:
            raise StopIteration from exc
        self.ptr += 1
        return item

@cython.final
cdef class IterWrapper(IterInterface):
    cdef object it

    def __cinit__(self,object it):
        self.it = it

    def __str__(self):
        return f"IterWrapper(it={self.it})"

    cpdef bint can_be_copied(self):
        if isinstance(self.it, IterInterface):
            return self.it.can_be_copied()
        return False

    cpdef copy(self):
        if isinstance(self.it, IterInterface):
            return IterWrapper(self.it.copy())

        raise Exception(
            "Iterator containing a python generator cannot be copied.\n"
            "Python generators can't be trivially copied, if you really need to create a copy, "
            "you should collect the generator into a Sequence and create a LIter from it."
        )

    cpdef next(self):
        return next(self.it)


@cython.final
cdef class AsyncIterWrapper(AsyncIterInterface):
    cdef object ait

    def __cinit__(self, object ait):
        self.ait = ait

    def __str__(self):
        return f"AsyncIterWrapper(ait={self.ait})"

    @cython.iterable_coroutine
    async def anext(self):
        return await anext(self.ait)
