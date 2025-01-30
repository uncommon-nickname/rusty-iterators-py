import os
import shutil

from Cython.Build import cythonize
from distutils.command.build_ext import build_ext
from setuptools import Extension
from setuptools.dist import Distribution


def compile_cython() -> None:
    print("🔧 Compiling Cython extensions...")

    extensions = [
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
        {"ext_modules": cythonize(extensions, compiler_directives={"language_level": "3", "binding": True})}
    )

    cmd = build_ext(dist)
    cmd.ensure_finalized()
    cmd.run()

    for output in cmd.get_outputs():  # type: ignore[no-untyped-call]
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)

    print("✅ Shared libraries (.so) generated.")


def copy_stub_files() -> None:
    stub_src = os.path.join(os.path.dirname(__file__), "stubs", "rusty_iterators")
    package_dst = os.path.join(os.path.dirname(__file__), "rusty_iterators")

    if os.path.exists(stub_src):
        for root, _, files in os.walk(stub_src):
            rel_path = os.path.relpath(root, stub_src)
            target_path = os.path.join(package_dst, rel_path)
            os.makedirs(target_path, exist_ok=True)

            for file in files:
                if file.endswith(".pyi"):
                    shutil.copyfile(os.path.join(root, file), os.path.join(target_path, file))

    print("✅ Type stubs copied successfully!")


if __name__ == "__main__":
    compile_cython()
    copy_stub_files()
