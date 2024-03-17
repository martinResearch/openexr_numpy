"""Setup script"""

from setuptools import find_packages, setup

libname = "openexr_numpy"

setup(
    name=libname,
    version="0.0.1",
    author="Martin de La Gorce",
    author_email="martin.delagorce@gmail.com",
    description="Module to postpone the execution of a function.",
    packages=find_packages(),
    license="MIT",
    ext_modules=[],  # additional source file(s)),
    include_dirs=[],
    package_data={},
    install_requires=["typeguard"],
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
)
