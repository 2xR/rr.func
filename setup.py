import pathlib
import re

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent
readme_file = here / "README.rst"
source_file = here / "src" / "rr" / "func.py"
version_match = re.search(r"__version__\s*=\s*(['\"])(.*)\1", source_file.read_text())
if version_match is None:
    raise Exception("unable to extract version from {}".format(source_file))
version = version_match.group(2)

setup(
    name="rr.func",
    version=version,
    description="Additional functional programming tools for Python",
    long_description=readme_file.read_text(),
    url="https://github.com/2xR/rr.func",
    author="Rui Jorge Rei",
    author_email="rui.jorge.rei@googlemail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    packages=["rr"] + ["rr." + p for p in find_packages("src/rr")],
    package_dir={"": "src"},
)
