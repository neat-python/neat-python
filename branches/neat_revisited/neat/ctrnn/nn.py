from neat import nn

class CTNeuron(nn.Neuron):
    ''' Continuous-time neuron model based on:
    
        Beer, R. D. and Gallagher, J.C. (1992). 
        Evolving Dynamical Neural Networks for Adaptive Behavior. 
        Adaptive Behavior 1(1):91-122. 
    '''
    def __init__(self, neurontype, id = None, bias=0, response=1, state=0, tau=1):
        super(CTNeuron, self).__init__(neurontype, id, bias, response)

        # decay rate
        self.__decay  = 1.0/tau 
        # needs to set the initial state (initial condition for the ODE)
        self.__state = state
        # fist output
        self._output = nn.sigmoid(self.__state + self._bias, self._response)

    def activate(self):
        "Updates neuron's state for a single time-step"
        if(len(self._synapses) > 0):            
            self.__update_state()
            return nn.sigmoid(self.__state + self._bias, self._response)
        else:
            return self._output # in case it's a sensor

    def __update_state(self):
        ''' Returns neuron's next state using Forward-Euler method.
            Future: integrate using scipy.integrate.
        '''
        step_size = 0.01
        self.__state += (step_size*self.__decay)*(-self.__state + self._update_activation())

def create_phenotype(chromo):
    """ Receives a chromosome and returns its phenotype (a neural network) """ 
    return nn.create_phenotype(chromo, CTNeuron)
    
def create_ffphenotype(chromo):
    """ Receives a chromosome and returns its phenotype (a neural network) """
    return nn.create_ffphenotype(chromo, CTNeuron)
