cdef class AsyncIterInterface:
    cpdef AsyncMap amap(self, object afunc)

cdef class AsyncIterAdapter(AsyncIterInterface):
    cdef object it

cdef class AsyncMap(AsyncIterInterface):
    cdef AsyncIterInterface ait
    cdef object afunc
