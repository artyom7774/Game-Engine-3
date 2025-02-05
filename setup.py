from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

import shutil
import os
import sysconfig

EXTENSION = ".pyd"


class CustomBuildExt(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)

        ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
        if ext_suffix and filename.endswith(ext_suffix):
            filename = filename[: -len(ext_suffix)] + EXTENSION

        return filename

    def copy_extensions_to_source(self):
        super().copy_extensions_to_source()
        for ext in self.extensions:
            if not ext.sources:
                continue
            fullname = self.get_ext_fullname(ext.name)
            original_path = self.get_ext_fullpath(fullname)

            source_pyx = ext.sources[0]
            source_dir = os.path.dirname(source_pyx)

            os.makedirs(source_dir, exist_ok=True)

            target_path = os.path.join(source_dir, os.path.basename(original_path))
            shutil.copy(original_path, target_path)


def find_pyx_files(directory):
    pyx_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pyx"):
                pyx_files.append(os.path.join(root, file))
    return pyx_files


extensions = []
pyx_files = find_pyx_files("engine")

for pyx_file in pyx_files:
    module_name = os.path.splitext(pyx_file)[0].replace(os.path.sep, '.')
    extensions.append(
        Extension(
            name=module_name,
            sources=[pyx_file],
        )
    )

setup(
    name="engine",
    ext_modules=extensions,
    cmdclass={"build_ext": CustomBuildExt},
    packages=find_packages(),
    annotate=True,
    compiler_directives={
        "boundscheck": False,
        "wraparound": False,
        "language_level": 3
    }
)
