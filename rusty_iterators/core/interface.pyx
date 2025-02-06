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

    cpdef take(self, int amount):
        return Take(self, amount)

    cpdef unzip(self):
        cdef list left = []
        cdef list right = []

        for left_item, right_item in self:
            left.append(left_item)
            right.append(right_item)

        return left, right

    cpdef zip(self, IterInterface second):
        return Zip(self, second)

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


@cython.final
cdef class Zip(IterInterface):
    def __cinit__(self, IterInterface first, IterInterface second):
        self.first = first
        self.second = second

    def __str__(self):
        return f"Zip(first={self.first}, second={self.second})"

    cpdef bint can_be_copied(self):
        return self.first.can_be_copied() and self.second.can_be_copied()

    cpdef copy(self):
        return Zip(self.first.copy(), self.second.copy())

    cpdef next(self):
        return (self.first.next(), self.second.next())

@cython.final
cdef class Take(IterInterface):
    def __cinit__(self, IterInterface it, int amount):
        if amount <= 0:
            raise Exception("You have to `take` at least one item.")

        self.it = it
        self.amount = amount
        self.taken = 0

    def __str__(self):
        return f"Take(amount={self.amount}, taken={self.taken}, it={self.it})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        cdef Take obj

        obj = Take(self.it.copy(), self.amount)
        obj.taken = self.taken

        return obj

    cpdef next(self):
        if self.taken == self.amount:
            raise StopIteration

        cdef object item

        item = self.it.next()
        self.taken += 1
        return item
