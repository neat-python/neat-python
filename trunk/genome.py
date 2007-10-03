# -*- coding: UTF-8 -*-
import random
import math

class NodeGene(object):
    def __init__(self, id, nodetype):
        '''nodetype should be "INPUT", "HIDDEN", or "OUTPUT"'''
        self.__id = id
        self.__type = nodetype
        assert(self.__type in ('INPUT', 'OUTPUT', 'HIDDEN'))
        
    def __str__(self):
        return "Node %d %s" % (self.__id, self.__type)
    
    id = property(lambda self: self.__id)

class ConnectionGene(object):
    __global_innov_number = 0
    __innovations = {} # A list of innovations.
    # Should it be global? Reset at every generation? Who knows?
    
    def __init__(self, innode, outnode, weight, enabled):
        self.__in = innode
        self.__out = outnode
        self.__weight = weight
        self.__enabled = enabled
        try:
            self.__innov_number = self.__innovations[self.key]
        except KeyError:
            self.__innov_number = self.__get_new_innov_number()
            self.__innovations[self.key] = self.__innov_number
    
    @classmethod
    def __get_new_innov_number(cls):
        cls.__global_innov_number += 1
        return cls.__global_innov_number
    
    def __str__(self):
        s = "In %d, Out %d, Weight %f, " % (self.__in, self.__out, self.__weight)
        if self.__enabled:
            s += "Enabled, "
        else:
            s += "Disabled, "
        return s + "Innov %d" % (self.__innov_number,)
            
    key = property(lambda self: (self.__in, self.__out))

class Chromosome(object):
    """ Testing chromosome - in the future it will be a list
        of node and link genes plus a fitness value """
    id = 1
    def __init__(self):
        self.__connection_genes = {} # dictionary of connection genes
        self.__node_genes = [] # list of node genes
        # Temporary, to calculate distance
        self.__genes = [random.randrange(-5,5) for i in xrange(20)]
        self.fitness = max(self.__genes) # stupid fitness function
        self.species_id = None
        self.id = Chromosome.id
        Chromosome.id += 1
        
    def mutate(self):
        """ Mutates this chromosome """
        # this method must be overridden!
        return self
    
    # compatibility function (for testing purposes)
    def dist(self, ind_b):
        # two chromosomes are similar if the difference between the sum of 
        # their 'float' genes is less than a compatibility threshold
        if math.fabs(sum(self.__genes) - sum(ind_b.__genes)) < 3.9: # compatibility threshold
            return True
        else:
            return False
    
    @staticmethod
    def create_fully_connected(num_input, num_output):
        '''
        Creates a chromosome for a fully connected network with no hidden nodes.
        '''
        c = Chromosome()
        id = 1
        # Create node genes
        for i in range(num_input):
            c.__node_genes.append(NodeGene(id, 'INPUT'))
            id += 1
        for i in range(num_output):
            c.__node_genes.append(NodeGene(id, 'OUTPUT'))
            # Connect it to all input nodes
            for input_node in c.__node_genes[:num_input]:
                cg = ConnectionGene(input_node.id, id, 0, True)
                c.__connection_genes[cg.key] = cg
            id += 1
        return c
    
    # sort chromosomes by their fitness
    def __ge__(self, other):
        return self.fitness >= other.fitness
    
    def __gt__(self, other):
        return self.fitness > other.fitness
    
    def __le__(self, other):
        return self.fitness <= other.fitness
    
    def __lt__(self, other):
        return self.fitness < other.fitness
    
    def __str__(self):
        s = "Nodes:"
        for ng in self.__node_genes:
            s += "\n\t" + str(ng)
        s += "\nConnections:"
        for cg in self.__connection_genes.values():
            s += "\n\t" + str(cg)
        return s

if __name__ ==  '__main__' :
    c = Chromosome.create_fully_connected(3, 2)
    print c
