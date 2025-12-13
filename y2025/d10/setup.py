from setuptools import setup
from mypyc.build import mypycify

setup(
    name='y2025-d10',
    packages=['y2025.d10'],
    ext_modules=mypycify(["main.py"])
)
