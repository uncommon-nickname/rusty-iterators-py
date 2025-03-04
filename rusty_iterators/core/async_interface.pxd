cdef class AsyncIterInterface:
    cpdef AsyncMap amap(self, object afunc)
    cpdef AsyncIterInterface copy(self)

cdef class AsyncIterAdapter(AsyncIterInterface):
    cdef object it

cdef class AsyncMap(AsyncIterInterface):
    cdef AsyncIterInterface ait
    cdef object afunc
