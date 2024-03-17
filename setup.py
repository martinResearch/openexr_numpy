"""Setup script."""

from setuptools import find_packages, setup

libname = "openexr_numpy"

setup(
    name=libname,
    version="0.0.1",
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
