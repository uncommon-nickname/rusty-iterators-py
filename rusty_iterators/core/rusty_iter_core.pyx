include "interface.pyx"

import cython

@cython.final
cdef class RustyIter(Interface):
    cdef object generator

    def __cinit__(self, object generator):
        self.generator = generator

    cpdef next(self):
        return next(self.generator)
    
    @classmethod
    def from_items(cls, *args):
        return SeqWrapper(args)
