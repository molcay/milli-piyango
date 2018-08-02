import setuptools
import milli_piyango

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=milli_piyango.__name__,
    version=milli_piyango.__version__,
    author="M. Olcay TERCANLI",
    author_email="molcaytercanli@gmail.com",
    description="A package for getting lottery data from mpi.gov.tr(Turkish Lottery)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/molcay/milli-piyango",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
