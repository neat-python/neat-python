"""Integrate-and-fire networks. Uses the C++ extension when available."""

try:
    from neat.ifnn.ifnn_cpp import Neuron
except ImportError:
    from neat.ifnn.ifnn_pure import Neuron

from neat.iznn.iznn_pure import Synapse
from neat.iznn.network import Network


def create_phenotype(chromosome):
    """ Receives a chromosome and returns its phenotype (a neural network) """

    neurons = {}
    input_neurons = []
    output_neurons = []
    for ng in chromosome.node_genes:
        neurons[ng.id] = Neuron(ng.bias)
        if ng.type == 'INPUT':
            input_neurons.append(neurons[ng.id])
        elif ng.type == 'OUTPUT':
            output_neurons.append(neurons[ng.id])

    synapses = [Synapse(neurons[cg.innodeid], neurons[cg.outnodeid], cg.weight)
                 for cg in chromosome.conn_genes if cg.enabled]

    return Network(neurons, input_neurons, output_neurons, synapses)


__all__ = ['Neuron', 'create_phenotype']
