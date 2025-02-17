cdef class IterInterface:
    cpdef object advance_by(self, int n)
    cpdef bint can_be_copied(self)
    cpdef object chain(self, IterInterface second)
    cpdef object collect(self)
    cpdef object collect_into(self, object factory)
    cpdef object copy(self)
    cpdef object cycle(self, bint use_cache = *)
    cpdef object enumerate(self)
    cpdef object flatten(self)
    cpdef object filter(self, object func)
    cpdef object fold(self, object init, object func)
    cpdef void for_each(self, object func)
    cpdef object last(self)
    cpdef object map(self, object func)
    cpdef object moving_window(self, int size, bint use_cache = *)
    cpdef object next(self)
    cpdef object nth(self, int n)
    cpdef object reduce(self, object func)
    cpdef object step_by(self, int step)
    cpdef object sum(self)
    cpdef object take(self, int amount)
    cpdef object unzip(self)
    cpdef object zip(self, IterInterface second)

cdef class Enumerate(IterInterface):
    cdef IterInterface it
    cdef int curr_idx

cdef class Filter(IterInterface):
    cdef IterInterface it
    cdef object func

cdef class Flatten(IterInterface):
    cdef IterInterface it
    cdef int ptr
    cdef list cache

cdef class Map(IterInterface):
    cdef IterInterface it
    cdef object func

cdef class CacheCycle(IterInterface):
    cdef IterInterface it
    cdef int ptr
    cdef bint use_cache
    cdef list cache

cdef class CacheMovingWindow(IterInterface):
    cdef IterInterface it
    cdef int size
    cdef list cache
    cdef int ptr

cdef class CopyCycle(IterInterface):
    cdef IterInterface it
    cdef IterInterface orig

cdef class CopyMovingWindow(IterInterface):
    cdef IterInterface it
    cdef IterInterface orig
    cdef int size

cdef class StepBy(IterInterface):
    cdef bint first_take
    cdef IterInterface it
    cdef int step_minus_one

cdef class Take(IterInterface):
    cdef IterInterface it
    cdef int taken
    cdef int amount

cdef class Zip(IterInterface):
    cdef IterInterface first
    cdef IterInterface second

cdef class Chain(IterInterface):
    cdef IterInterface first
    cdef IterInterface second
    cdef bint use_second
