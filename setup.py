from setuptools import setup

package = "byapi"
version = "1.2.0"


def read_file(filename):
    try:
        with open(filename) as f:
            return f.read()
    except Exception:
        return ""

long_description = read_file("README.rst") or read_file("README.md")
entry_points = {}

setup(
    name=package,
    version=version,
    description="The Python Development Package of BiggerYun API",
    long_description=long_description,
    author="xiegaofeng",
    author_email="xiegaofeng@grandcloud.cn",
    packages=[package],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    scripts=[],
    python_requires='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
    setup_requires=[],
    entry_points=entry_points)
