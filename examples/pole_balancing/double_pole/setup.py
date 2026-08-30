# Optional C++ extension for the cart-pole experiment.
# The default is the pure-Python integrator in dpole.py.
# python setup.py build_ext -i
from setuptools import setup, Extension
setup(
      name='Cart-pole experiment',
      ext_modules=[
               Extension('dpole', ['dpole.cpp'])]
)
