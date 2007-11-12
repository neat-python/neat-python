import spiking_nn as snc

neuron = snc.Neuron()
print neuron.potential, neuron.has_fired
print neuron.current
neuron.current += 1
print neuron.current
neuron.advance()
neuron = snc.Neuron(0)
neuron = snc.Neuron(0, 0.02)
neuron = snc.Neuron(0, 0.02, 0.2)
neuron = snc.Neuron(0, 0.02, 0.2, -65.0)
neuron1 = snc.Neuron(0, 0.02, 0.2, -65.0, 8.0)
neuron2 = snc.Neuron(0, c=-65.0)
snc.Synapse(neuron1, neuron2, 0)