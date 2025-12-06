from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

from Cython.Build import cythonize

import sysconfig
import platform
import shutil
import os

EXTENSION = ".pyd" if platform.system() == "Windows" else ".so"


class CustomBuildExt(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)

        ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")

        if ext_suffix and filename.endswith(ext_suffix):
            filename = filename[:-len(ext_suffix)] + EXTENSION

        return filename

    def copy_extensions_to_source(self):
        super().copy_extensions_to_source()

        build_lib = self.build_lib
        for ext in self.extensions:
            if not ext.sources:
                continue

            fullname = self.get_ext_fullname(ext.name)
            filename = self.get_ext_filename(fullname)
            source_path = self.get_ext_fullpath(fullname)

            source_pyx = ext.sources[0]
            target_dir = os.path.dirname(source_pyx)

            os.makedirs(target_dir, exist_ok=True)

            target_path = os.path.join(target_dir, os.path.basename(filename))

            if os.path.exists(source_path):
                shutil.copy2(source_path, target_path)

                print(f"Copied {source_path} to {target_path}")


def find_pyx_files(directory):
    pyx_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pyx"):
                full_path = os.path.join(root, file)
                pyx_files.append(full_path)

    return pyx_files


def create_extension(pyx_file):
    module_name = os.path.splitext(pyx_file)[0].replace(os.path.sep, '.')

    compile_args = []
    link_args = []

    if platform.system() == "Windows":
        compile_args = ["/O2", "/fp:fast"]
        link_args = []

    else:
        compile_args = ["-O2", "-Wall", "-std=c99"]
        link_args = []

    return Extension(
        name=module_name,
        sources=[pyx_file],
        extra_compile_args=compile_args,
        extra_link_args=link_args,
        define_macros=[("CYTHON_TRACE", "1")] if os.getenv("CYTHON_DEBUG") else []
    )


def main():
    pyx_files = find_pyx_files("engine")

    if not pyx_files:
        print("No .pyx files found in 'engine' directory!")
        return

    extensions = [create_extension(pyx_file) for pyx_file in pyx_files]

    compiler_directives = {
        "boundscheck": False,
        "wraparound": False,
        "initializedcheck": False,
        "nonecheck": False,
        "language_level": 3,
        "optimize.use_switch": True,
        "optimize.unpack_method_calls": True,
    }

    if os.getenv("CYTHON_DEBUG"):
        compiler_directives.update({
            "linetrace": True,
            "binding": True,
        })

    cythonized_extensions = cythonize(
        extensions,
        compiler_directives=compiler_directives,
        annotate=bool(os.getenv("CYTHON_ANNOTATE")),
        force=bool(os.getenv("CYTHON_FORCE_REBUILD")),
        quiet=not bool(os.getenv("CYTHON_VERBOSE")),
    )

    setup(
        name="engine",
        version="1.0.0",
        description="Game Engine Cython Extensions",
        ext_modules=cythonized_extensions,
        cmdclass={"build_ext": CustomBuildExt},
        packages=find_packages(),
        zip_safe=False,
        python_requires=">=3.7",
        setup_requires=["cython>=0.29.0"],
    )


if __name__ == "__main__":
    main()