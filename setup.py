import re

from setuptools import setup, find_packages


with open("README.rst", "rt") as readme_file:
    readme = readme_file.read()

# Extract version information directly from the source code.
with open("src/rr/func.py", "rt") as source_file:
    source = source_file.read()
match = re.search(r"__version__\s*=\s*(['\"])(\d+(\.\d+){2}([-+]?\w+)*)\1", source)
if match is None:
    raise Exception("unable to extract version from {}".format(source_file.name))
version = match.group(2)

setup(
    name="rr.func",
    version=version,
    description="Additional functional programming tools for Python",
    long_description=readme,
    url="https://github.com/2xR/rr.func",
    author="Rui Jorge Rei",
    author_email="rui.jorge.rei@googlemail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    data_files=[("", ["LICENSE.txt", "README.rst"])],
    install_requires=["future~=0.15.2"],
)