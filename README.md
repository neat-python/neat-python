# NEAT-Python

The basic idea behind NEAT is to evolve both network topology (structural adaptation) and weights/biases (parametrical adaptation).

As a starting point, you can check the XOR experiment in the `examples` folder.

This repository is the 2007 academic implementation (version 0.1), now updated for **Python 3.10+**.
It is not the PyPI package `neat-python` (that name belongs to [CodeReclaimers/neat-python](https://github.com/CodeReclaimers/neat-python)).
This tree keeps the original CTNN / Izhikevich / integrate-and-fire phenotypes and pole-balancing experiments.

### Requirements

- Python >= 3.10
- Optional: `matplotlib` and `pydot` for plots and network diagrams (`uv sync --extra viz`)

### Install

```bash
uv sync
```

Or, after packaging:

```bash
uv pip install -e .
```

### XOR example

```bash
cd examples/xor
uv run python xor2.py
```

### Version 0.2

Version 0.1 was developed only for academic purposes in 2007. The Python code was based on the C++ version by [Kenneth O. Stanley](http://www.cs.ucf.edu/~kstanley/neat.html) and his paper on [NeuroEvolution of Augmented Topologies](http://nn.cs.utexas.edu/keyword?stanley:ec02). A C++ neural module was included for speed; this release defaults to the pure-Python implementations so a compiler is not required.

The original C++ sources remain in the tree (`neat/nn/nn_cpp`, `neat/iznn`, `neat/ifnn`, `examples/pole_balancing/double_pole/dpole.cpp`) but are not built. The double-pole integrator is now a Python port (`dpole.py`).

Paper: [Structural and Parametric Evolution of Continuous-Time Recurrent Neural Networks](https://ieeexplore.ieee.org/document/46659123).

### Things TODO

* Create a pip package (project name: `neat-python-classic`) once this port is stable.
* Probably use PyTorch or TensorFlow, with a slightly different genome encoding to accommodate these changes.
* Add more activation functions and expand the ability of each neuron to adapt its own activation function.
