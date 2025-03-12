from Cython.Build import cythonize
from setuptools import Extension, setup

setup(
    ext_modules=cythonize(
        [
            Extension(
                "rusty_iterators.core.async_interface",
                ["rusty_iterators/core/async_interface.pyx"],
                extra_compile_args=["-march=native", "-O3"],
                libraries=["m"],
            ),
            Extension(
                "rusty_iterators.core.interface",
                ["rusty_iterators/core/interface.pyx"],
                extra_compile_args=["-march=native", "-O3"],
                libraries=["m"],
            ),
            Extension(
                "rusty_iterators.core.wrappers",
                ["rusty_iterators/core/wrappers.pyx"],
                extra_compile_args=["-march=native", "-O3"],
                libraries=["m"],
            ),
        ],
        nthreads=5,
        compiler_directives={"language_level": 3, "binding": True},
    ),
)
