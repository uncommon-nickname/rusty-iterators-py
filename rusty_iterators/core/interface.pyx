import cython

from rusty_iterators.lib._async import AsyncIterAdapter

cdef class IterInterface:
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __repr__(self):
        return self.__str__()

    def as_async(self):
        return AsyncIterAdapter(self)

    cpdef bint can_be_copied(self):
        raise NotImplementedError

    cpdef collect(self):
        cdef list result
        result = self.collect_into(list)
        return result

    cpdef collect_into(self, factory):
        return factory(self)

    cpdef copy(self):
        raise NotImplementedError

    cpdef cycle(self, bint use_cache=True):
        return CacheCycle(self) if use_cache else CopyCycle(self)

    cpdef filter(self, object func):
        return Filter(self, func)

    cpdef map(self, object func):
        return Map(self, func)

    cpdef next(self):
        raise NotImplementedError

@cython.final
cdef class Filter(IterInterface):
    def __cinit__(self, IterInterface it, object func):
        self.it = it
        self.func = func

    def __str__(self):
        return f"Filter(it={self.it})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        return Filter(self.it.copy(), self.func)

    cpdef next(self):
        cdef object item
        while True:
            item = self.it.next()
            if self.func(item):
                return item

@cython.final
cdef class Map(IterInterface):
    def __cinit__(self, IterInterface it, object func):
        self.it = it
        self.func = func

    def __str__(self):
        return f"Map(it={self.it})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        return Map(self.it.copy(), self.func)

    cpdef next(self):
        return self.func(self.it.next())

@cython.final
cdef class CacheCycle(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it
        self.ptr = 0
        self.use_cache = False
        self.cache = []

    def __str__(self):
        return f"CycleCached(ptr={self.ptr}, cache_size={len(self.cache)}, it={self.it})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        obj = CacheCycle(self.it.copy())
        obj.cache = self.cache[:]
        obj.ptr = self.ptr
        obj.use_cache = self.use_cache
        return obj

    cpdef next(self):
        if self.use_cache:
            self.ptr = self.ptr % len(self.cache)
            item = self.cache[self.ptr]
            self.ptr += 1
            return item

        try:
            item = self.it.next()
            self.cache.append(item)
            return item

        except StopIteration:
            if len(self.cache) == 0:
                raise

            self.use_cache = True
            return self.next()

@cython.final
cdef class CopyCycle(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it.copy()
        self.orig = it

    def __str__(self):
        return f"CycleCopy(it={self.it}, orig={self.orig})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        obj = CopyCycle(self.it.copy())
        obj.orig = self.orig.copy()
        return obj

    cpdef next(self):
        try:
            return self.it.next()
        except StopIteration:
            self.it = self.orig.copy()
            return self.it.next()
