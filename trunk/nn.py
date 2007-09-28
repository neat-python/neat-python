# -*- coding: UTF-8 -*-
from math import exp
import random
#random.seed(0)
#from psyco.classes import *

class Neuron:
        """ A simple artificial neuron """	
	def __init__(self, tipo, response=1):
	   self.synapses = []
	   self.tipo = tipo # input, hidden, output, bias ("type" is a reserved word!)
	   self.response = response
	   if self.tipo is 'bias': 
              self.activation = -1
           else: 
  	      # in a recurrent network all neurons must have an "initial state"
              self.activation = 0 

	def activate(self):
	   if(len(self.synapses) > 0):
	     soma = 0
	     for s in self.synapses:
		  soma += s.incoming()
	     return self.f(soma, self.response)
	   else:
	     return self.activation # for input neurons (sensors)

	def append(self, s):
	   self.synapses.append(s)

	# activation function
	@staticmethod
	def f(x, response):
	   return 1/(1+exp(-x*response)) 

class Synapse:
	""" A synapse indicates the connection strength between two neurons (or itself) """	
	def __init__(self, weight, source, destination):
	   self.weight = weight
	   self.source = source
	   destination.append(self)

	def incoming(self):
	   return self.weight*self.source.activation

class Network:
	""" A neural network has a list of neurons linked by synapses """
	def __init__(self, neurons=[], synapses=[]):
	   self.neurons = neurons
	   self.synapses = synapses

	def setWeights(self, weights):
	    k=0
	    for s in self.synapses:
	        s.weight = weights[k]
	        k+=1

	# asynchronous network activation (serial)
	def aexecute(self, inputs):	   
	   # assign "input neurons'" activation values (actually a sensor)
           k=0
	   for n in self.neurons:
	       if(n.tipo == 'input'): 
                   n.activation = inputs[k]   
                   k+=1

	   # activate all neurons in the network (except for the inputs)
	   output = []		  
	   for n in self.neurons[k:]:	      
	       n.activation = n.activate()
               if(n.tipo == 'output'): output.append(n.activation)

	   return output

	# synchronous network activation (parallel)
	def sexecute(self, inputs): # ugly name for such an important method!
	   current_state = []
	   # assign "input neurons'" activation values (actually a sensor)
           k=0
	   for n in self.neurons:
	      if(n.tipo == 'input'): 
                 n.activation = inputs[k]   
		 current_state.append(n.activation)
                 k+=1
	      else:
		 current_state.append(n.activate())
    
	   output = []		     
	   for i, n in enumerate(self.neurons):
	      n.activation = current_state[i]
	      if(n.tipo == 'output'): output.append(n.activation)

	   return output

class FeedForward(Network):
	""" A feedforward network is a particular class of neural network """

	# only a hidden layer is considered for now
	def __init__(self, inputs, hidden, output, bias=False):
	    Network.__init__(self)
	    self.inputs = inputs
	    self.hidden = hidden
	    self.output = output
	    self.bias = bias

	    # is it slower than simply 'append' as commented out below?
	    self.neurons += [Neuron('input') for i in xrange(self.inputs)]
	    self.neurons += [Neuron('hidden') for i in xrange(self.hidden)]
	    self.neurons += [Neuron('output') for i in xrange(self.output)]

    	    # create NNs neurons
#    	    for i in xrange(self.inputs):
#	       self.neurons.append(Neuron('input'))

#	    for i in xrange(self.hidden):
#	       self.neurons.append(Neuron('hidden'))

#	    for i in xrange(self.output):
#	       self.neurons.append(Neuron('output'))

	    if self.bias: self.neurons.append(Neuron('bias')) # don't forget the bias

	    # link all neurons in each layer assigning random weights
	    # inputs -> hidden
	    for i in self.neurons[:self.inputs]:
	       for h in self.neurons[self.inputs:self.inputs+self.hidden]:
	         self.synapses.append(Synapse(random.random(), i, h))
	
	    # hidden > output
	    for h in self.neurons[self.inputs:self.inputs+self.hidden]:
	       for o in self.neurons[self.inputs+self.hidden:-1]:
	         self.synapses.append(Synapse(random.random(), h, o))

	    # bias -> all neurons (except inputs)
	    if self.bias:
               for n in self.neurons[self.inputs:-1]:
                   self.synapses.append(Synapse(random.random(), self.neurons[-1], n))

if __name__ == "__main__":

    # Example
    rna = FeedForward(2,1,2,True)	
    print 'Parallel activation method: '
    for t in range(3):
        print rna.sexecute([1,0])

    print 'Serial activation method: '
    for t in range(3):
        print rna.aexecute([1,0])
