#!/usr/bin/env python3

from wheel.bdist_wheel import bdist_wheel as bdist_wheel_
from setuptools import setup, Extension, Command
from distutils.util import get_platform

import glob
import sys
import os

directory = os.path.dirname(os.path.realpath(__file__))

setup(
    name="rxsignal",
    packages=["rxsignal"],
    version="0.0.0",
    license="MIT",
    description="",
    author="mirmik",
    author_email="mirmikns@yandex.ru",
    url="https://github.com/mirmik/rxsignal",
    long_description=open(os.path.join(directory, "README.md"), "r").read(),
    long_description_content_type="text/markdown",
    keywords=["testing", "signal"],
)
