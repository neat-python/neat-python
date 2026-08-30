# Optional C++ ANN extension (Python 2 C API; not built by default).
# python setup.py build_ext -i
from setuptools import setup, Extension
setup(
      name='neat-python',      
      packages=['nn_cpp'],
      ext_modules=[               
               Extension('ann', ['ANN.cpp', 'PyANN.cpp']),],
)
