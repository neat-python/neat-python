# -*- coding: UTF-8 -*-
import random
import math

class NodeGene(object):    
    # Without bias from rev 22.
    def __init__(self, id, nodetype):
        '''nodetype should be "INPUT", "HIDDEN", or "OUTPUT"'''
        self.__id = id
        self.__type = nodetype
        assert(self.__type in ('INPUT', 'OUTPUT', 'HIDDEN'))
        
    def __str__(self):
        return "Node %d %s" % (self.__id, self.__type)
    
    id = property(lambda self: self.__id)
    type = property(lambda self: self.__type)

class ConnectionGene(object):
    __global_innov_number = 0
    __innovations = {} # A list of innovations.
    # Should it be global? Reset at every generation? Who knows?
    
    # Weight mutation parameters
    WEIGHT_MUTATION_POWER = 0.1
    MAX_WEIGHT = 3.0
    MIN_WEIGHT = -3.0
    
    def __init__(self, innodeid, outnodeid, weight, enabled, innov = None):
        self.__in = innodeid
        self.__out = outnodeid
        self.__weight = weight
        self.__enabled = enabled
        if innov is None:
            try:
                self.__innov_number = self.__innovations[self.key]
            except KeyError:
                self.__innov_number = self.__get_new_innov_number()
                self.__innovations[self.key] = self.__innov_number
        else:
            self.__innov_number = innov
    
    weight = property(lambda self: self.__weight)
    innodeid = property(lambda self: self.__in)
    outnodeid = property(lambda self: self.__out)
    enabled = property(lambda self: self.__enabled)
    
    def enable(self):
        '''For the "enable link" mutation'''
        self.__enabled = True
    
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
    
    def __cmp__(self, other):
        return cmp(self.__innov_number, other.__innov_number)
    
    def split(self, node_id):
        """Splits a connection, creating two new connections and disabling this one"""
        self.__enabled = False
        new_conn1 = ConnectionGene(self.__in, node_id, 1, True)
        new_conn2 = ConnectionGene(node_id, self.__out, self.__weight, True)
        return new_conn1, new_conn2
    
    def mutate_weight(self):
        self.__weight += random.uniform(-1, 1) * self.WEIGHT_MUTATION_POWER
        if self.__weight > self.MAX_WEIGHT:
            self.__weight = self.MAX_WEIGHT
        elif self.__weight < self.MIN_WEIGHT:
            self.__weight = self.MIN_WEIGHT
    
    def copy(self):
        return ConnectionGene(self.__in, self.__out, self.__weight,
                              self.__enabled, self.__innov_number)
    
    def is_same_innov(self, cg):
        return self.__innov_number == cg.__innov_number
    
    # Key for dictionaries, avoids two connections between the same nodes.
    key = property(lambda self: (self.__in, self.__out))

class Chromosome(object):
    id = 1
    def __init__(self):
        self.__connection_genes = {} # dictionary of connection genes
        self.__node_genes = [] # list of node genes
        self.__input_nodes = 0 # number of input nodes
        # Temporary, to calculate distance
        self.genes = [random.randrange(-5,5) for i in xrange(20)]
        self.sum_genes = sum(self.genes)
        self.fitness = None # now we have an evaluation method in the Population class
        self.species_id = None
        self.id = Chromosome.id
        Chromosome.id += 1
        
    # TO CHECK: is it right?
    node_genes = property(lambda self: self.__node_genes)
    conn_genes = property(lambda self: self.__connection_genes.values())
        
    def mutate(self):
        """ Mutates this chromosome """
        # TODO: mutate with a probability
        for cg in self.__connection_genes.values():
            cg.mutate_weight()
            cg.enable()
        self.__mutate_add_connection()
        self.__mutate_add_node()
        return self
    
    def crossover(self, other):
        ''' Applies the crossover operator. Returns a child '''
        child = Chromosome() # TODO: self.__crossover(other)
        if self.fitness > other.fitness:
            parent1 = self
            parent2 = other
        else:
            parent1 = other
            parent2 = self
        # Crossover node genes
        child.__node_genes = parent1.__node_genes[:]
        # Crossover connection genes
        for cg1 in parent1.__connection_genes.values():
            try:
                cg2 = parent2.__connection_genes[cg.key]
            except KeyError:
                child.__connection_genes[cg.key] = cg1.copy()
            else:
                if cg2.is_same_innov(cg2):
                    child.__connection_genes[cg.key] = random.choice((cg1, cg2)).copy()
                else:
                    child.__connection_genes[cg.key] = cg1.copy()
        child.mutate()
        return child
    
    def __mutate_add_node(self):
        # Choose a random connection to split
        try:
            conn_to_split = random.choice(self.__connection_genes.values())
        except IndexError: # Empty list of genes
            # TODO: this can't happen, do not fail silently
            return
        ng = NodeGene(len(self.__node_genes) + 1, 'HIDDEN')
        self.__node_genes.append(ng)
        new_conn1, new_conn2 = conn_to_split.split(ng.id)
        self.__connection_genes[new_conn1.key] = new_conn1
        self.__connection_genes[new_conn2.key] = new_conn2
    
    def __mutate_add_connection(self):
        # Only for recurrent networks
        # TODO: add support for feedforwad networks
        total_possible_conns = (len(self.__node_genes) - self.__input_nodes) \
            * len(self.__node_genes)
        remaining_conns = total_possible_conns - len(self.__connection_genes)
        # Check if new connection can be added:
        if remaining_conns > 0:
            n = random.randint(0, remaining_conns - 1)
            count = 0
            # Count connections
            for in_node in self.__node_genes:
                for out_node in self.__node_genes[self.__input_nodes:]:
                    if (in_node.id, out_node.id) not in self.__connection_genes.keys():
                        # Free connection
                        if count == n: # Connection to create
                            cg = ConnectionGene(in_node.id, out_node.id, 0, True)
                            self.__connection_genes[cg.key] = cg
                            return
                        else:
                            count += 1
    
    # compatibility function (for testing purposes)
    def dist(self, ind_b):
        # two chromosomes are similar if the difference between the sum of 
        # their 'float' genes is less than a compatibility threshold
        if math.fabs(self.sum_genes - ind_b.sum_genes) < 3.9: # compatibility threshold
            return True
        else:
            return False
    
    @staticmethod
    def create_fully_connected(num_input, num_output):
        '''
        Factory method
        Creates a chromosome for a fully connected network with no hidden nodes.
        '''
        c = Chromosome()
        id = 1
        # Create node genes
        for i in range(num_input):
            c.__node_genes.append(NodeGene(id, 'INPUT'))
            id += 1
        c.__input_nodes += num_input
        for i in range(num_output):
            node_gene = NodeGene(id, 'OUTPUT')
            c.__node_genes.append(node_gene)
            id += 1
            # Connect it to all input nodes
            for input_node in c.__node_genes[:num_input]:
                cg = ConnectionGene(input_node.id, node_gene.id, 0, True)
                c.__connection_genes[cg.key] = cg
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
        connections = self.__connection_genes.values()
        connections.sort()
        for c in connections:
            s += "\n\t" + str(c)
        return s
    
# work in progress
import nn
def create_phenotype(chromosome):
    """ Receives a chromosome and returns its phenotype (a neural network) """
    
    # bias parameter is missing (default=0)
    neurons_list = [nn.Neuron(ng.type, ng.id) \
                    for ng in chromosome.node_genes]
    
    conn_list = [(cg.innodeid, cg.outnodeid, cg.weight) \
                 for cg in chromosome.conn_genes if cg.enabled] 
    
    return nn.Network(neurons_list, conn_list)
    
        

if __name__ ==  '__main__':
    c = Chromosome.create_fully_connected(3, 2)
    print "Before mutation:"
    print c
    c.mutate()
    print
    print "After mutation:"
    print c
    brain = create_phenotype(c)
    # needs to verify consistency!
    print brain.sactivate([0.5, 0.5, 0.5])
    print brain
