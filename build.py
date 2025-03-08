# ruff: noqa: I001
import os
import shutil
from distutils.command.build_ext import build_ext

from Cython.Build import cythonize
from setuptools import Extension
from setuptools.dist import Distribution


def compile_cython() -> None:
    print("🔧 Compiling Cython extensions...")

    extensions = [
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
    ]

    dist = Distribution(
        {
            "ext_modules": cythonize(
                extensions, compiler_directives={"language_level": "3", "binding": True}
            )
        }
    )

    cmd = build_ext(dist)  # type:ignore[arg-type]
    cmd.ensure_finalized()
    cmd.run()

    for output in cmd.get_outputs():  # type: ignore[no-untyped-call]
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)

    print("✅ Shared libraries (.so) generated.")


if __name__ == "__main__":
    compile_cython()
