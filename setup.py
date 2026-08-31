#!/usr/bin/env python

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools
import os
import io

__version__ = "0.9.2"
FASTTEXT_SRC = "src"

# Based on https://github.com/pybind/python_example


class get_pybind_include:
    """Resolve pybind11's include path after build dependencies are installed."""

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


try:
    coverage_index = sys.argv.index("--coverage")
except ValueError:
    coverage = False
else:
    del sys.argv[coverage_index]
    coverage = True

fasttext_src_cc = sorted(
    os.path.join(FASTTEXT_SRC, filename)
    for filename in os.listdir(FASTTEXT_SRC)
    if filename.endswith(".cc") and filename != "main.cc"
)

ext_modules = [
    Extension(
        str("fasttext_pybind"),
        [
            str("python/fasttext_module/fasttext/pybind/fasttext_pybind.cc"),
        ]
        + fasttext_src_cc,
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            # Path to fasttext source code
            FASTTEXT_SRC,
        ],
        language="c++",
    ),
]


def has_flag(compiler, flags):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
        f.write("int main (int argc, char **argv) { return 0; }")
        try:
            compiler.compile([f.name], extra_postargs=flags)
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++17 compiler flag."""
    standards = ["-std=c++17"]
    for standard in standards:
        if has_flag(compiler, [standard]):
            return standard
    raise RuntimeError("Unsupported compiler -- at least C++17 support " "is needed!")


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""

    c_opts = {
        "msvc": ["/EHsc", "/std:c++17"],
        "unix": ["-O3", "-funroll-loops", "-pthread"],
    }

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = list(self.c_opts.get(ct, []))
        extra_link_args = ["-pthread"] if ct == "unix" else []

        if coverage:
            coverage_option = "--coverage"
            opts = [flag for flag in opts if flag != "-O3"]
            opts.extend(["-O0", "-fno-inline"])
            opts.append(coverage_option)
            extra_link_args.append(coverage_option)

        if ct == "unix":
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, ["-fvisibility=hidden"]):
                opts.append("-fvisibility=hidden")
        elif ct == "msvc":
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = extra_link_args
        build_ext.build_extensions(self)


def _get_readme():
    with io.open("python/README.md", encoding="utf-8") as fid:
        return fid.read()


setup(
    name="fasttext",
    version=__version__,
    author="Onur Celebi",
    author_email="celebio@fb.com",
    description="fasttext Python bindings",
    long_description=_get_readme(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    url="https://github.com/facebookresearch/fastText",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.10",
    install_requires=["numpy"],
    cmdclass={"build_ext": BuildExt},
    packages=[
        str("fasttext"),
        str("fasttext.util"),
        str("fasttext.tests"),
    ],
    package_dir={str(""): str("python/fasttext_module")},
    zip_safe=False,
)
