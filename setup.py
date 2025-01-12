import glob
import os
import shutil

from Cython.Build import cythonize
from setuptools import Extension, setup  # type: ignore


def copy_so_files() -> None:
    files_to_copy = [
        {
            "source_dir": "core",
            "target_dir": "rusty_iterators",
            "prefix": "rusty_iter_core",
        },
        {
            "source_dir": "lib",
            "target_dir": "rusty_iterators",
            "prefix": "iter_interface",
        },
    ]

    for file_def in files_to_copy:
        source_dir = file_def["source_dir"]
        target_dir = file_def["target_dir"]
        prefix = file_def["prefix"]

        for file_path in glob.glob(os.path.join(source_dir, "*.so")):
            file_name = os.path.basename(file_path)
            if file_name.startswith(prefix):
                dest_path = os.path.join(target_dir, file_name)
                shutil.copyfile(file_path, dest_path)
                print(f"$$$$$: {file_path} -> {dest_path}")


setup(
    name="rusty-iterators",
    version="0.1.0",
    packages=["rusty_iterators", "rusty_iterators.core", "rusty_iterators.lib"],
    ext_modules=cythonize(
        [
            Extension(
                "rusty_iterators.core.rusty_iter_core",
                ["rusty_iterators/core/rusty_iter_core.pyx"],
                extra_compile_args=["-march=native", "-O3"],
                libraries=["m"],
            ),
            Extension(
                "rusty_iterators.lib.iter_interface",
                ["rusty_iterators/lib/iter_interface.pyx"],
            ),
        ],
        compiler_directives={"language_level": "3", "binding": True},
    ),
    include_package_data=True,
    # package_data={
    #     "rusty_iterators.stubs.core": ["*.pyi"],
    #     "rusty_iterators.stubs.lib": ["*.pyi"],
    # },
    package_data={
        "rusty_iterators": ["py.typed"],
        "": ["stubs/**/*.pyi"],
    },
    # cmdclass={"build_ext": CustomBuildExt},
)

# copy_so_files()
