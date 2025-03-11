cimport cython

cdef class AsyncIterInterface:
    def __aiter__(self):
        return self

    @cython.iterable_coroutine
    async def __anext__(self):
        return await self.anext()

    def __repr__(self):
        return self.__str__()

    @cython.iterable_coroutine
    async def anext(self):
        raise NotImplementedError

    @cython.iterable_coroutine
    async def acollect(self):
        cdef list result = [item async for item in self]
        return result

    cpdef AsyncMap amap(self, object afunc):
        return AsyncMap(self, afunc)

    cpdef AsyncIterInterface copy(self):
        raise NotImplementedError

@cython.final
cdef class AsyncIterAdapter(AsyncIterInterface):
    def __cinit__(self, object it):
        self.it = it

    def __str__(self):
        return f"AsyncIterAdapter(it={self.it})"

    @cython.iterable_coroutine
    async def anext(self):
        try:
            return next(self.it)
        except StopIteration as exc:
            raise StopAsyncIteration from exc

    cpdef AsyncIterAdapter copy(self):
        cdef AsyncIterAdapter obj

        obj = AsyncIterAdapter(self.it.copy())

        return obj

@cython.final
cdef class AsyncMap(AsyncIterInterface):
    def __cinit__(self, AsyncIterInterface ait, object afunc):
        self.ait = ait
        self.afunc = afunc

    def __str__(self):
        return f"AsyncMap(ait={self.ait})"

    @cython.iterable_coroutine
    async def anext(self):
        return await self.afunc(await self.ait.anext())

    cpdef AsyncMap copy(self):
        cdef AsyncMap obj

        obj = AsyncMap(self.ait.copy(), self.afunc)

        return obj
