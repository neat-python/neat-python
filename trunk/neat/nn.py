# -*- coding: UTF-8 -*-
from math import exp
import random
#random.seed(0)
#from psyco.classes import *

class Neuron: # using properties without extending object? Is it possible?
    """ A simple artificial neuron """
    __id = 0
    def __init__(self, neurontype, id=None, bias_weight=0.0, response=4.9):
        if id is None:
            self.__id = Neuron.__id
            Neuron.__id += 1            
        else:
            self.__id = id
            
        self.synapses = []
        self.__bias_weight = bias_weight
        self.__type = neurontype # input, hidden, output        
        assert(self.__type in ('INPUT', 'OUTPUT', 'HIDDEN'))
        
        self.__response = response # default = 4.9 (Stanley, p. 146)
        self.activation = 0.0  # for recurrent networks all neurons must have an "initial state"
    
    type = property(lambda self: self.__type)
    id = property(lambda self: self.__id)
    
    def activate(self):
        if(len(self.synapses) > 0):
            soma = 0.0
            for s in self.synapses:
                soma += s.incoming()
            return self.f(soma - self.__bias_weight, self.__response)
        else:
            return self.activation # for input neurons (sensors)

    def append(self, s):
        self.synapses.append(s)
        
    def __repr__(self):
        return '%d %s' %(self.__id, self.__type)

    # activation function
    @staticmethod
    def f(x, response):
	return 1.0/(1.0 + exp(-x*response)) 

class Synapse:
    """ A synapse indicates the connection strength between two neurons (or itself) """
    def __init__(self, source, dest, weight):        
        self.weight = weight
        self.source = source
        dest.append(self)

    def incoming(self):
        return self.weight*self.source.activation

class Network(object):
    """ A neural network has a list of neurons linked by synapses """
    def __init__(self, neurons=[], links=None):
        self.__neurons = neurons
        self.__synapses = []                
        
        if links is not None:        
            N = {} # a temporary dictionary to create the network connections
            for n in self.__neurons: N[n.id] = n            
            for c in links: self.__synapses.append(Synapse(N[c[0]], N[c[1]], c[2]))
            
    def addNeuron(self, neuron):
        self.__neurons += neuron
        
    def getNeuron(self):
        return self.__neurons
        
    def addSynapse(self, synapse):
        self.__synapses.append(synapse)
            
    #neurons = property(lambda self: self.__neurons, addNeuron)
    #synapses = property(lambda self: self.__synapses, addSynapse)
        
                    
    def __repr__(self):
        return '%d nodes and %d synapses' % (len(self.__neurons), len(self.__synapses))
                    
    # preciso repensar como os pesos serão atribuídos de volta!
    # como os bias evoluem no próprio neurônio agora, preciso
    # decidir como eles serão alterados (e.g. as N primeiras
    # posições da lista de pesos corresponde aos bias dos N
    # neurônios, o que vier depois é conexão - mas a lista pode
    # estar desordenada! Então seria melhor usar um dict.
    def setWeights(self, weights):
        k=0
        for s in self.synapses:
            s.weight = weights[k]
            k+=1

    # serial network activation (asynchronous)
    def sactivate(self, inputs):	   
        # assign "input neurons'" activation values (actually a sensor)
        k=0
        #for n in self.__neurons[:len(inputs)]:
        for n in self.__neurons:
            if(n.type == 'INPUT'):
                n.activation = inputs[k]   
                k+=1
		
        # activate all neurons in the network (except for the inputs)
        output = []		  
        for n in self.__neurons[k:]:	      
            n.activation = n.activate()
            if(n.type == 'OUTPUT'): 
                output.append(n.activation)
			
        return output

    # parallel network activation (synchronous)
    def pactivate(self, inputs): # ugly name for such an important method!
        current_state = []
        # assign "input neurons'" activation values (actually a sensor)
        k=0	   
        for n in self.__neurons:
            if(n.type == 'INPUT'): 
                n.activation = inputs[k]   
                current_state.append(n.activation)
                k+=1
            else:
                current_state.append(n.activate())
	    
        output = []		     
        for i, n in enumerate(self.__neurons):
            n.activation = current_state[i]
            if(n.type == 'OUTPUT'): 
                output.append(n.activation)
	    
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
        
        self.addNeuron([Neuron('INPUT')  for i in xrange(self.inputs)])
        self.addNeuron([Neuron('HIDDEN') for i in xrange(self.hidden)])
        self.addNeuron([Neuron('OUTPUT') for i in xrange(self.output)])
        
        print self.getNeuron()
               
        # inputs -> hidden
        for i in self.getNeuron()[:inputs]: # percorre só os inputs
            if i.type == 'INPUT': # nem preciso testar pq só será do tipo input mesmo!
                for h in self.getNeuron()[inputs:-output]: # percorre só os hidden
                    if h.type == 'HIDDEN': # aqui só tem hidden, nem preciso testar
                        self.addSynapse(Synapse(i, h, random.random()))                        
                        
        # hidden -> outputs
        for h in self.getNeuron()[inputs:-output]:
            if h.type == 'HIDDEN':
                for o in self.getNeuron()[-output:]:
                    if o.type == 'OUTPUTS':
                        self.addSynapse(Synapse(h, o, random.random()))



if __name__ == "__main__":
#    # Example
#    nn = FeedForward(2,1,2,True)
#    print 'Parallel activation method: '
#    for t in range(3):
#        print nn.sactivate([1,0])
#    print nn
#		
#    print 'Serial activation method: '
#    for t in range(3):
#	    print nn.pactivate([1,0])

    # defining a neural network manually
    neurons = [Neuron('INPUT', 0), Neuron('OUTPUT', 1), Neuron('OUTPUT', 2)]
    connections = [(0, 2, 0.5), (0, 1, 0.5), (1, 2, 0.5)]
    
    net = Network(neurons, connections) # constructs the neural network
    print net.pactivate([0.04]) # parallel activation method
    print net # print how many neurons and synapses our network has 
