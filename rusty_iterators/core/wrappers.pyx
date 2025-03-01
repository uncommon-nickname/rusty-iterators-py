cimport cython
from rusty_iterators.core.interface cimport IterInterface
from rusty_iterators.core.async_interface cimport AsyncIterInterface

@cython.final
cdef class CopiableGenerator:
    cdef object it
    cdef list cache
    cdef int ptr

    def __cinit__(self, object it, list cache, int ptr):
        self.it = it
        self.cache = cache
        self.ptr = ptr

    def __iter__(self):
        return self

    @cython.boundscheck(False)
    def __next__(self):
        cdef object item

        if self.ptr < len(self.cache):
            item = self.cache[self.ptr]
        else:
            item = next(self.it)
            self.cache.append(item)
        self.ptr += 1

        return item

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"CopiableGenerator(self.it={self.it})"

    cpdef CopiableGenerator copy(self):
        cdef CopiableGenerator obj = CopiableGenerator(self.it, self.cache, self.ptr)
        return obj

@cython.final
cdef class SeqWrapper(IterInterface):
    cdef object s
    cdef int ptr

    def __init__(self, object s):
        self.s = s
        self.ptr = 0

    def __str__(self):
        return f"SeqWrapper(ptr={self.ptr}, s={len(self.s)})"

    cpdef SeqWrapper copy(self):
        cdef SeqWrapper obj

        obj = SeqWrapper(self.s)
        obj.ptr = self.ptr

        return obj

    cpdef object next(self):
        try:
            item = self.s[self.ptr]
        except IndexError as exc:
            raise StopIteration from exc
        self.ptr += 1
        return item

@cython.final
cdef class IterWrapper(IterInterface):
    cdef object it

    def __cinit__(self, object it):
        self.it = it

    def __str__(self):
        return f"IterWrapper(it={self.it})"

    cpdef IterWrapper copy(self):
        if isinstance(self.it, (IterInterface, CopiableGenerator)):
            return IterWrapper(self.it.copy())

        # NOTE: 01.03.2025 <@uncommon-nickname>
        # Using this wrapper type, makes the item consumption slower.
        # Not only we have to maintain the cache, but also call more
        # functions. To take as small performance hit as possible, we
        # initialize this type only if user decides to make a copy.
        self.it = CopiableGenerator(self.it, [], 0)

        return IterWrapper(self.it.copy())

    cpdef object next(self):
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
