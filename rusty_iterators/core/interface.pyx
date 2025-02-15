import cython

from rusty_iterators.lib._async import AsyncIterAdapter

cdef object _aggregate_sum(object acc, object x):
    return acc + x

cdef class IterInterface:
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __repr__(self):
        return self.__str__()

    def all(self, f=None):
        return all(f(i) for i in self) if f else all(self)

    def any(self, f=None):
        return any(f(i) for i in self) if f else any(self)

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

    cpdef advance_by(self, int n):
        if n < 0:
            raise ValueError("Amount to advance by must be greater or equal to 0.")

        for _ in range(n):
            try:
                self.next()
            except StopIteration:
                break

        return self

    cpdef copy(self):
        raise NotImplementedError

    cpdef cycle(self, bint use_cache=True):
        return CacheCycle(self) if use_cache else CopyCycle(self)

    cpdef enumerate(self):
        return Enumerate(self)

    cpdef filter(self, object func):
        return Filter(self, func)

    cpdef fold(self, object init, object func):
        for item in self:
            init = func(init, item)
        return init

    cpdef map(self, object func):
        return Map(self, func)

    cpdef moving_window(self, int size, bint use_cache = True):
        return CacheMovingWindow(self, size) if use_cache else CopyMovingWindow(self, size)

    cpdef next(self):
        raise NotImplementedError

    cpdef nth(self, int n):
        return self.advance_by(n).next()

    cpdef reduce(self, object func):
        cdef object init = self.next()
        return self.fold(init, func)

    cpdef step_by(self, int step):
        return StepBy(self, step)

    cpdef sum(self):
        # NOTE: 14.02.2025 <@uncommon-nickname>
        # Closure functions are not yet supported by Cython transpiler.
        return self.reduce(_aggregate_sum)

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

    cpdef chain(self, IterInterface second):
        return Chain(self, second)

@cython.final
cdef class Enumerate(IterInterface):
    def __cinit__(self, IterInterface it):
        self.it = it
        self.curr_idx = 0

    def __str__(self):
        return f"Enumerate(curr_idx={self.curr_idx}, it={self.it})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        cdef Enumerate obj

        obj = Enumerate(self.it.copy())
        obj.curr_idx = self.curr_idx
        return obj

    cpdef next(self):
        cdef object item

        item = self.it.next()
        result = (self.curr_idx, item)
        self.curr_idx += 1
        return result


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
cdef class CacheMovingWindow(IterInterface):
    def __cinit__(self, IterInterface it, int size):
        if size <= 0:
            raise ValueError("Moving window size has to be greater or equal to one.")
        self.it = it
        self.size = size
        self.cache = []
        self.ptr = 0

    def __str__(self):
        return f"CacheMovingWindow(size={self.size}, cache={self.cache}, it={self.it})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        cdef CacheMovingWindow obj

        obj = CacheMovingWindow(self.it.copy(), self.size)
        obj.cache = self.cache[::]
        obj.ptr = self.ptr

        return obj

    cpdef next(self):
        cdef list result

        if len(self.cache) == self.size:
            self.ptr %= self.size
            self.cache[self.ptr] = self.it.next()
            self.ptr += 1

            result = []
            for _ in range(self.size):
                self.ptr %= self.size
                result.append(self.cache[self.ptr])
                self.ptr += 1
            return result

        for _ in range(self.size):
            self.cache.append(self.it.next())

        result = self.cache[::]
        return result


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
cdef class CopyMovingWindow(IterInterface):
    def __cinit__(self, IterInterface it, int size):
        if size <= 0:
            raise ValueError("Moving window size has to be greater or equal to one.")
        self.it = it.copy()
        self.size = size
        self.orig = it

    def __str__(self):
        return f"CopyMovingWindow(size={self.size}, it={self.it}, orig={self.orig})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        cdef CopyMovingWindow obj

        obj = CopyMovingWindow(self.it.copy(), self.size)
        obj.orig = self.orig.copy()

        return obj

    cpdef next(self):
        cdef list result

        result = [self.it.next() for _ in range(self.size)]
        self.orig.next()
        self.it = self.orig.copy()

        return result

@cython.final
cdef class StepBy(IterInterface):
    def __cinit__(self, IterInterface it, step: int) -> None:
        if step <= 0:
            raise ValueError("Step has to be greater than zero.")

        self.first_take = True
        self.it = it
        self.step_minus_one = step - 1

    def __str__(self):
        return f"StepBy(first_take={self.first_take}, step={self.step_minus_one + 1}, it={self.it})"

    cpdef bint can_be_copied(self):
        return self.it.can_be_copied()

    cpdef copy(self):
        cdef StepBy obj
        obj = StepBy(self.it.copy(), self.step_minus_one + 1)
        obj.first_take = self.first_take
        return obj

    cpdef next(self):
        if self.first_take:
            self.first_take = False
        else:
            self.it.advance_by(self.step_minus_one)

        return self.it.next()


@cython.final
cdef class Take(IterInterface):
    def __cinit__(self, IterInterface it, int amount):
        if amount <= 0:
            raise ValueError("You have to `take` at least one item.")

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
cdef class Chain(IterInterface):
    def __cinit__(self, IterInterface first, IterInterface second):
        self.first = first
        self.second = second
        self.use_second = False

    def __str__(self):
        return f"Chain(use_second={self.use_second}, first={self.first}, second={self.second})"

    cpdef bint can_be_copied(self):
        return self.first.can_be_copied() and self.second.can_be_copied()

    cpdef copy(self):
        obj = Chain(self.first.copy(), self.second.copy())
        obj.use_second = self.use_second
        return obj

    cpdef next(self):
        if self.use_second:
            return self.second.next()

        try:
            return self.first.next()

        except StopIteration:
            self.use_second = True
            return self.next()
