from Cython.Build import cythonize
from setuptools import Extension, setup

setup(
    name="rusty_iter",
    ext_modules=cythonize(
        [
            Extension(
                "rusty_iter_core",
                ["core/rusty_iter_core.pyx"],
                extra_compile_args=["-march=native", "-O3"],
                libraries=["m"],
            )
        ],
        compiler_directives={"binding": True, "language_level": 3},
    ),
    zip_safe=False,
)
