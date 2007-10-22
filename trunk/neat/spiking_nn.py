# -*- coding: UTF-8 -*-

class SpikingNeuron(object):
    '''
    A spiking neuron model based on:
    
    Izhikevich, E. M.
    Simple Model of Spiking Neurons
    IEEE TRANSACTIONS ON NEURAL NETWORKS, VOL. 14, NO. 6, NOVEMBER 2003
    '''
    
    def __init__(self, bias = 0, a = 0.02, b = 0.2, c = -65.0, d = 2.0):
        '''
        a, b, c, d are the parameters of this model.
        a: the time scale of the recovery variable.
        b: the sensitivity of the recovery variable.
        c: the after-spike reset value of the membrane potential.
        d: after-spike reset of the recovery variable.
        '''
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d
        self.__v = self.__c # membrane potential
        self.__u = self.__b * self.__v # membrane recovery variable
        self.__fired = False
        self.__bias = bias
        self.current = self.__bias
    
    def advance(self):
        'Advances time in 1 ms.'
        self.__v += 0.5 * (0.04 * self.__v ** 2 + 5 * self.__v + 140 - self.__u + self.current)
        self.__v += 0.5 * (0.04 * self.__v ** 2 + 5 * self.__v + 140 - self.__u + self.current)
        self.__u += self.__a * (self.__b * self.__v - self.__u)
        if self.__v > 30:
            self.__fired = True
            self.__v = self.__c
            self.__u += self.__d
        else:
            self.__fired = False
        self.current = self.__bias
    
    potential = property(lambda self: self.__v, doc = 'membrane potential')
    fired = property(lambda self: self.__fired, doc = 'indicates whether the neuron has fired')

if __name__ == '__main__':
    n = SpikingNeuron(10)
    for i in range(1000):
        print '%d\t%f' % (i, n.potential)
        n.advance()
