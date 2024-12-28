import os
import shutil

from Cython.Build import cythonize
from distutils.command.build_ext import build_ext
from distutils.core import Distribution, Extension


def build() -> None:
    extensions = [
        Extension(
            "iter",
            ["rusty_iterators_cython/iter.pyx"],
            extra_compile_args=["-march=native", "-O3"],
            extra_link_args=[],
            include_dirs=[],
            libraries=["m"],
        )
    ]
    ext_modules = cythonize(extensions, include_path=[], compiler_directives={"binding": True, "language_level": 3})
    distribution = Distribution({"name": "extended", "ext_modules": ext_modules})
    distribution.package_dir = "extended"

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)


if __name__ == "__main__":
    build()
