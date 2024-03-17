"""Setup script."""

import os
import re

from setuptools import find_packages, setup

libname = "openexr_numpy"

# get the version from the __init__ file
# using a regular expression
with open(os.path.join(os.path.dirname(__file__), libname, "__init__.py")) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError("Unable to find own __version__ string")

setup(
    name=libname,
    version=version,
    author="Martin de La Gorce",
    author_email="martin.delagorce@gmail.com",
    description="Module read and write Open EXR image files using numpy arrays.",
    packages=find_packages(),
    license="MIT",
    ext_modules=[],  # additional source file(s)),
    include_dirs=[],
    package_data={},
    install_requires=["numpy", "openexr", "imath"],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
)
