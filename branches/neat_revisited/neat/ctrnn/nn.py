from neat import nn
#from scipy import integrate

class CTNeuron(nn.Neuron):
    ''' Continuous-time neuron model based on:
    
        Beer, R. D. and Gallagher, J.C. (1992). 
        Evolving Dynamical Neural Networks for Adaptive Behavior. 
        Adaptive Behavior 1(1):91-122. 
    '''
    def __init__(self, neurontype, id = None, bias=0, response=1, tau=1):
        super(CTNeuron, self).__init__(neurontype, id, bias, response)

        # decay rate
        self.__decay  = 1.0/tau 
        # needs to set the initial state (initial condition for the ODE)
        self.__state = 0.4 #TODO: Verify what's the "best" initial state?
        # fist output
        self._output = nn.sigmoid(self.__state + self._bias, self._response)
        
        #self.__r = integrate.ode(self.neuron_state)
        #self.__r.set_initial_value([0.4],0)
        
#    def neuron_state(self, Y, t):     
#        return self.__decay*(-Y + self._update_activation())

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
        dt = 0.01
        self.__state += (dt*self.__decay)*(-self.__state + self._update_activation())
        
        #self.__state = self.__r.integrate(self.__r.t+dt)[0]
               

def create_phenotype(chromo):
    """ Receives a chromosome and returns its phenotype (a CTRNN) """ 
    neurons_list = [CTNeuron(ng._type, ng._id, ng._bias, ng._response, ng._time_constant) \
                    for ng in chromo._node_genes]
        
    conn_list = [(cg.innodeid, cg.outnodeid, cg.weight) \
                  for cg in chromo.conn_genes if cg.enabled] 
                  
    return nn.Network(neurons_list, conn_list)
