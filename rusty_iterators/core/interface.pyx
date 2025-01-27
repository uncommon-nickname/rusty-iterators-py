import cython

cdef class IterInterface:
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

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

    cpdef next(self):
        raise NotImplementedError

    cpdef map(self, object func):
        return Map(self, func)

@cython.final
cdef class Filter(IterInterface):
    cdef IterInterface other
    cdef object func

    def __cinit__(self, IterInterface other, object func):
        self.other = other
        self.func = func

    cpdef next(self):
        cdef object item
        while True:
            item = self.other.next()
            if self.func(item):
                return item

@cython.final
cdef class Map(IterInterface):
    cdef IterInterface other
    cdef object func

    def __cinit__(self, IterInterface other, object func):
        self.other = other
        self.func = func

    cpdef next(self):
        return self.func(self.other.next())

@cython.final
cdef class SeqWrapper(IterInterface):
    cdef object s
    cdef int ptr

    def __init__(self, object s):
        self.s = s
        self.ptr = 0

    def __str__(self):
        return f"SeqWrapper(ptr={self.ptr}, s={len(self.s)})"

    def copy(self):
        return True

    cpdef next(self):
        try:
            item = self.s[self.ptr]
        except IndexError as exc:
            raise StopIteration from exc
        self.ptr += 1
        return item

@cython.final
cdef class IterWrapper(IterInterface):
    cdef IterInterface it

    def __cinit__(self,IterInterface it):
        self.it = it

    def __str__(self):
        return f"IterWrapper(it={self.it})"

    def can_be_copied(self) -> bool:
        if isinstance(self.it, IterInterface):
            return self.it.can_be_copied()
        return False

    def copy(self):
        if isinstance(self.it, IterInterface):
            return IterWrapper(self.it.copy())

        raise Exception(
            "Iterator containing a python generator cannot be copied.\n"
            "Python generators can't be trivially copied, if you really need to create a copy, "
            "you should collect the generator into a Sequence and create a LIter from it."
        )

    cpdef next(self):
        return next(self.it)
