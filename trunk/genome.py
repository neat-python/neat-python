# -*- coding: UTF-8 -*-
import random
import math

class NodeGene(object):
    def __init__(self, id, nodetype, bias = 0):
        '''nodetype should be "INPUT", "HIDDEN", or "OUTPUT"'''
        self.__id = id
        self.__type = nodetype
        self.__bias = bias
        assert(self.__type in ('INPUT', 'OUTPUT', 'HIDDEN'))
        
    def __str__(self):
        return "Node %d %s" % (self.__id, self.__type)
    
    id = property(lambda self: self.__id)

class ConnectionGene(object):
    __global_innov_number = 0
    __innovations = {} # A list of innovations.
    # Should it be global? Reset at every generation? Who knows?
    
    def __init__(self, innodeid, outnodeid, weight, enabled):
        self.__in = innodeid
        self.__out = outnodeid
        self.__weight = weight
        self.__enabled = enabled
        try:
            self.__innov_number = self.__innovations[self.key]
        except KeyError:
            self.__innov_number = self.__get_new_innov_number()
            self.__innovations[self.key] = self.__innov_number
    
    def enable(self):
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
        
    def mutate(self):
        """ Mutates this chromosome """
        # TODO: mutate with a probability
        self.__mutate_add_connection()
        self.__mutate_add_node()
        return self
    
    def crossover(self, other):
        ''' Applies the crossover operator. Returns a child '''
        child = Chromosome() # TODO: self.__crossover(other)
        return child.mutate()
    
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

if __name__ ==  '__main__':
    c = Chromosome.create_fully_connected(3, 2)
    print "Before mutation:"
    print c
    c.mutate()
    print
    print "After mutation:"
    print c
