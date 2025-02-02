cdef class IterInterface:
    cpdef bint can_be_copied(self)
    cpdef object copy(self)
    cpdef object next(self)
    cpdef object collect(self)
    cpdef object filter(self, object func)
    cpdef object map(self, object func)
    cpdef object cycle(self, bint use_cache = *)

cdef class Filter(IterInterface):
    cdef IterInterface it
    cdef object func
    cpdef object next(self)
    cpdef object copy(self)
    cpdef bint can_be_copied(self)

cdef class Map(IterInterface):
    cdef IterInterface other
    cdef object func
    cpdef object next(self)

cdef class CacheCycle(IterInterface):
    cdef IterInterface it
    cdef int ptr
    cdef bint use_cache
    cdef list cache
    cpdef object next(self)
    cpdef object copy(self)
    cpdef bint can_be_copied(self)

cdef class CopyCycle(IterInterface):
    cdef IterInterface it
    cdef IterInterface orig
    cpdef object next(self)
    cpdef object copy(self)
    cpdef bint can_be_copied(self)
