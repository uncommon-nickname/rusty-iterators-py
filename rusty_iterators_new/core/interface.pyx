import cython

cdef class Interface:
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
cdef class Filter(Interface):
    cdef Interface other
    cdef object func

    def __cinit__(self, Interface other, object func):
        self.other = other
        self.func = func

    cpdef next(self):
        cdef object item
        while True:
            item = self.other.next()
            if self.func(item):
                return item

@cython.final
cdef class Map(Interface):
    cdef Interface other
    cdef object func

    def __cinit__(self, Interface other, object func):
        self.other = other
        self.func = func

    cpdef next(self):
        return self.func(self.other.next())
