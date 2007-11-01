import math, random
from config import Config
#random.seed(0)
#from psyco.classes import *

class Neuron(object):
    """ A simple artificial neuron """
    __id = 0
    def __init__(self, neurontype, id=None, bias_weight=0.0, response=4.924273):
        if id is None:
            self.__id = Neuron.__id
            Neuron.__id += 1            
        else:
            self.__id = id
            
        self.synapses = []
        self.__bias_weight = bias_weight
        self.__type = neurontype # input, hidden, output        
        assert(self.__type in ('INPUT', 'OUTPUT', 'HIDDEN'))
        
        self.__response = response # default = 4.924273 (Stanley, p. 146)
        self.activation = 0.0  # for recurrent networks all neurons must have an "initial state"
    
    type = property(lambda self: self.__type, "Returns neuron's type: INPUT, OUTPUT, or HIDDEN")
    id = property(lambda self: self.__id, "Returns neuron's id")
    
    def activate(self):
        """ Activates the neuron. """
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
        """ Sigmoidal activation function. Here you can define 
            any type of activation function. """
        try:
            if Config.nn_activation == 'exp':
                output = 1.0/(1.0 + math.exp(-x*response))
            elif Config.nn_activation == 'tanh':
                output = math.tanh(x*response)
            else:
                # raise exception
                print 'Invalid activation type selected'
                
        except OverflowError:
             print 'Overflow error: x = %s', x
             
        return output

class Synapse(object):
    """ A synapse indicates the connection strength between two neurons (or itself) """
    def __init__(self, source, dest, weight):        
        self.__weight = weight
        self.__source = source
        self.__dest = dest
        dest.append(self) # adds the synapse to the destination neuron
        
    source = property(lambda self: self.__source)
    dest = property(lambda self: self.__dest)

    def incoming(self):
        """ Receives the incoming signal from a sensor or another neuron
            and returns the value to the neuron it belongs to. """
        return self.__weight*self.__source.activation
    
    def __repr__(self):
        return '%s -> %s -> %s' %(self.__source.id, self.__weight, self.__dest.id)

class Network(object):
    """ A neural network has a list of neurons linked by synapses """
    def __init__(self, neurons=[], links=None):
        self.__neurons = neurons
        self.__synapses = []                
        
        if links is not None:        
            N = {} # a temporary dictionary to create the network connections
            for n in self.__neurons: 
                N[n.id] = n            
            for c in links: 
                self.__synapses.append(Synapse(N[c[0]], N[c[1]], c[2]))
                
    neurons = property(lambda self: self.__neurons)
    synapses = property(lambda self: self.__synapses)
            
    def addNeuron(self, neuron):
        self.__neurons.append(neuron)
        
    def addSynapse(self, synapse):
        self.__synapses.append(synapse)
            
    def __repr__(self):
        return '%d nodes and %d synapses' % (len(self.__neurons), len(self.__synapses))
    
    def activate(self, inputs):
        if Config.nn_allow_recurrence:
            return self.pactivate(inputs)
        else:
            return self.sactivate(inputs)

    def sactivate(self, inputs):	
        """ Serial network activation (asynchronous) method. Mostly
            used in classification tasks (supervised learning) in
            feedforward topologies """   
        # assign "input neurons'" activation values (actually a sensor)
        k=0
        for n in self.__neurons[:len(inputs)]:
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

    def pactivate(self, inputs):
        """ Parallel network activation (synchronous) method. Mostly 
            used for control and unsupervised learning (i.e., artificial 
            life) in recurrent networks.            
        """
        # the current state is like a "photograph" taken at each time step 
        # reresenting all neuron's state at that time (think of it as a clock)
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
    # only one hidden layer is considered for now
    def __init__(self, layers, bias=False):
        Network.__init__(self)    
        self.input_layer = layers[0]
        self.output_layer = layers[-1]
        self.hidden_layers = layers[1:-1]
        self.bias = bias
        
        # assign random weights for bias
        if bias:
            r = random.uniform
        else:
            r = lambda a,b: 0
        
        for i in xrange(self.input_layer):
            self.addNeuron(Neuron('INPUT'))                              
        
        for i in xrange(self.hidden_layers[0]):
            self.addNeuron(Neuron('HIDDEN', bias_weight = r(-1,1), response = 1))
            
        for i in xrange(self.output_layer):
            self.addNeuron(Neuron('OUTPUT', bias_weight = r(-1,1), response = 1))
           
        r = random.uniform  # assign random weights             
        # inputs -> hidden
        for i in self.neurons[:self.input_layer]:
                for h in self.neurons[self.input_layer:-self.output_layer]:
                        self.addSynapse(Synapse(i, h, r(-1,1)))       
        # hidden -> outputs
        for h in self.neurons[self.input_layer:-self.output_layer]:
                for o in self.neurons[-self.output_layer:]:
                        self.addSynapse(Synapse(h, o, r(-1,1)))


if __name__ == "__main__":
    # Example
    import visualize
    nn = FeedForward([2,2,1], False)
    #visualize.draw_ff(nn)
    print 'Parallel activation method: '
    for t in range(3):
        print nn.pactivate([1,0])
    print 'Serial activation method: '
    for t in range(3):
	    print nn.pactivate([1,0])
    print nn

    # defining a neural network manually
    neurons = [Neuron('INPUT', 0), Neuron('OUTPUT', 1), Neuron('OUTPUT', 2)]
    connections = [(0, 2, 0.5), (0, 1, 0.5), (1, 2, 0.5)]
    
    net = Network(neurons, connections) # constructs the neural network
    #visualize.draw_ff(net)
    print net.pactivate([0.04]) # parallel activation method
    print net # print how many neurons and synapses our network has 
