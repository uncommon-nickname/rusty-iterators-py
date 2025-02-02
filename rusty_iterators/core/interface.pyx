import cython

from rusty_iterators.lib._async import AsyncIterAdapter

cdef class IterInterface:
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def as_async(self):
        return AsyncIterAdapter(self)
        
    def __repr__(self):
        return self.__str__()

    cpdef next(self):
        raise NotImplementedError
    
    cpdef bint can_be_copied(self):
        raise NotImplementedError
    
    cpdef copy(self):
        raise NotImplementedError

    cpdef collect(self):
        cdef list result = []
        cdef object item

        while True:
            try:
                item = self.next()
            except StopIteration:
                break
            result.append(item)
        return result

    cpdef filter(self, object func):
        return Filter(self, func)

    cpdef map(self, object func):
        return Map(self, func)

    cpdef cycle(self, bint use_cache=True):
        return CacheCycle(self) if use_cache else CopyCycle(self)
        
@cython.final
cdef class Filter(IterInterface):
    def __cinit__(self, IterInterface it, object func):
        self.it = it
        self.func = func

    cpdef next(self):
        cdef object item
        while True:
            item = self.it.next()
            if self.func(item):
                return item

    cpdef copy(self):
        return Filter(self.it.copy(), self.func)

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    def __str__(self):
        return f"Filter(it={self.it})"

@cython.final
cdef class Map(IterInterface):
    def __cinit__(self, IterInterface other, object func):
        self.other = other
        self.func = func

    cpdef next(self):
        return self.func(self.other.next())

@cython.final
cdef class CacheCycle(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it
        self.ptr = 0
        self.use_cache = False
        self.cache = []
        
    def __str__(self):
        return f"CycleCached(ptr={self.ptr}, cache={len(self.cache)}, it={self.it})"

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
