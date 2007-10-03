# -*- coding: UTF-8 -*-
import random

class ConnectionGene(object):
    __next_innovation_number = 1
    __innovations = {} # A list of innovations.
    # Should it be global? Reset at every generation? Who knows?
    def __init__(self, innode, outnode, weight, enabled):
        self.__in = innode
        self.__out = outnode
        self.__weight = weight
        self.__enabled = enabled
        key = (self.__in, self.__out)
        try:
            self.__innovation_number = self.__innovations[key]
        except KeyError:
            self.__innovation_number = self.__next_innovation_number
            self.__next_innovation_number += 1
            self.__innovations[key] = self.__innovation_number

class Chromosome(object):
    """ Testing chromosome - in the future it will be a list
        of node and link genes plus a fitness value """
    id = 1
    def __init__(self):
        self.__genes = [random.randrange(-5,5) for i in xrange(20)]
        self.fitness = max(self.__genes) # stupid fitness function
        self.species_id = None
        self.id = Chromosome.id
        Chromosome.id += 1
        
    def __iter__(self):
        return iter(self.__genes)
    
    def mutate(self):
        """ Mutates this chromosome """
        # this method must be overridden!
        return self
    
    # sort chromosomes by their fitness
    def __ge__(self, other):
        return self.fitness >= other.fitness
    
    def __gt__(self, other):
        return self.fitness > other.fitness
    
    def __le__(self, other):
        return self.fitness <= other.fitness
    
    def __lt__(self, other):
        return self.fitness < other.fitness
