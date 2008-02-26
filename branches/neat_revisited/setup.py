# Installation script
from distutils.core import setup, Extension
setup(
      name='neat-python',
      version='0.1',
      description='A NEAT (NeuroEvolution of Augmenting Topologies) implementation',
      packages=['neat', 'neat/iznn', 'neat/nn', 'neat/ctrnn'],
      ext_modules=[Extension('neat/iznn/iznn_cpp', ['neat/iznn/iznn.cpp'])],
)