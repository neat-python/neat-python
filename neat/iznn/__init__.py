"""Izhikevich spiking networks. Uses the C++ extension when available."""

try:
    from neat.iznn.iznn_cpp import Neuron, Synapse
except ImportError:
    from neat.iznn.iznn_pure import Neuron, Synapse

from neat.iznn.network import Network, create_phenotype

__all__ = ['Neuron', 'Synapse', 'Network', 'create_phenotype']
