import sys
from pathlib import Path

from setuptools import setup

if sys.implementation.name != "cpython":
    raise SystemError("This package will only work on CPython.")

if sys.version_info[0:2] < (3, 6):
    raise RuntimeError("This package requires Python 3.6+.")

setup(
    name="pytecode",
    use_scm_version={
        "version_scheme": "guess-next-dev",
        "local_scheme": "dirty-tag"
    },
    packages=[
        "pytecode",
    ],
    url="https://github.com/SunDwarf",
    license="LGPLv3",
    author="Laura Dickinson",
    author_email="l@veriny.tf",
    description="A library for compiling bytecode functions.",
    long_description=Path(__file__).with_name("README.rst").read_text(encoding="utf-8"),
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[],
    extras_require={},
    test_requires=[],
    python_requires=">=3.6",
)
