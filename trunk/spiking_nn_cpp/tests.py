import spiking_nn as snc

neuron = snc.Neuron()
print neuron.potential, neuron.has_fired
print neuron.current
neuron.current += 1
print neuron.current
