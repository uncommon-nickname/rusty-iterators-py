import cython

cdef class IterInterface:
    cpdef bint can_be_copied(self)
    cpdef object collect(self)
    cpdef object collect_into(self, object factory)
    cpdef object copy(self)
    cpdef object cycle(self, bint use_cache = *)
    cpdef object filter(self, object func)
    cpdef object map(self, object func)
    cpdef object next(self)
    cpdef object take(self, int amount)
    cpdef object unzip(self)
    cpdef object zip(self, IterInterface second)

cdef class Filter(IterInterface):
    cdef IterInterface it
    cdef object func

    cpdef bint can_be_copied(self)
    cpdef object copy(self)
    cpdef object next(self)

cdef class Map(IterInterface):
    cdef IterInterface it
    cdef object func

    cpdef bint can_be_copied(self)
    cpdef object copy(self)
    cpdef object next(self)

cdef class CacheCycle(IterInterface):
    cdef IterInterface it
    cdef int ptr
    cdef bint use_cache
    cdef list cache

    cpdef bint can_be_copied(self)
    cpdef object copy(self)
    cpdef object next(self)

cdef class CopyCycle(IterInterface):
    cdef IterInterface it
    cdef IterInterface orig

    cpdef bint can_be_copied(self)
    cpdef object copy(self)
    cpdef object next(self)


cdef class Zip(IterInterface):
    cdef IterInterface first
    cdef IterInterface second

    cpdef bint can_be_copied(self)
    cpdef object copy(self)
    cpdef object next(self)


cdef class Take(IterInterface):
    cdef IterInterface it
    cdef int amount
    cdef int taken

    cpdef bint can_be_copied(self)
    cpdef object copy(self)
    cpdef object next(self)
