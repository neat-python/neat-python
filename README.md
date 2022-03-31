# NEAT-Python
The basic idea behind NEAT is to evolve both network topology (structural adaptation) and weights/biases (parametrical adaptation).

As a starting point, you can check the XOR experiment in the examples folder.

### Version 0.1
Version .1 was developed only for academic purposes in 2007. Back then there weren't many neural networks APIs available in Python and most of them where not suitable for the idea we needed for our experiments. The project was hosted by Google Code and versioned using [Apache Subversion](https://subversion.apache.org) (or simply SVN for those born in the GIT era).

The main ideia was to experiment with Continuous-Time Neural Networks (CTNN) in an Artificial Life environment, similar to works by Larry Yaeger called [Polyworld](https://www.academia.edu/37664413/Evaluating_Topological_Models_of_Neuromodulation_in_Polyworld) and Karl Sims [Evolved Creatures](https://www.karlsims.com/papers/siggraph94.pdf). A benchmark with the inverted double pole demonstrated that CTNNs could better handle the task as we've shown in the paper [Structural and Parametric Evolution of Continuous-Time Recurrent Neural Networks](https://ieeexplore.ieee.org/document/46659123).

The Python code was based on the C++ version by [Kenneth O'Stanley](http://www.cs.ucf.edu/~kstanley/neat.html) and his famous paper on [NeuroEvolution of Augmented Topologies](http://nn.cs.utexas.edu/keyword?stanley:ec02). The inclusion of some C code was necessary to significantly increase the speed of the neural module.

Currently this version is only compatible with Python <= 2.7

### Things TODO:

* Update to support Python 3 - WIP
* Create a pip package to facilitate the compilation for the C code.
* Probably use PyTorch or TensorFlow, with a slightly different genome encoding to accommodate these changes. I'm aware of some approaches in the same direction by the NEAT community.
* Add more activation functions and expand the ability to each neuron to adapt its own activation function.

# Changelog

v0.2 - After 14+ years, I decided to make it compatiple with Python 3+ :)
