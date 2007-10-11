# -*- coding: UTF-8 -*-
import random
import math
from config import Config

excess_coeficient = Config.excess_coeficient
disjoint_coeficient = Config.disjoint_coeficient
weight_coeficient = Config.weight_coeficient

prob_mutatebias = Config.prob_mutatebias
prob_mutate_weight = Config.prob_mutate_weight
prob_togglelink = Config.prob_togglelink
prob_addconn = Config.prob_addconn
prob_addnode = Config.prob_addnode

prob_crossover = Config.prob_crossover # always perform crossingover?

# Weight mutation parameters
weight_mutation_power = Config.weight_mutation_power
max_weight = Config.max_weight
min_weight = Config.min_weight

class NodeGene(object):    
    def __init__(self, id, nodetype, bias=0):
        '''nodetype should be "INPUT", "HIDDEN", or "OUTPUT"'''
        self.__id = id
        self.__type = nodetype
        self.__bias = bias
        assert(self.__type in ('INPUT', 'OUTPUT', 'HIDDEN'))
        
    def __str__(self):
        return "Node %d %s, bias %s"% (self.__id, self.__type, self.__bias)
    
    def get_child(self, other):
        assert(self.__id == other.__id)
        ng = NodeGene(self.__id, self.__type,
                      random.choice((self.__bias, other.__bias)))
        return ng
    
    def mutate_bias(self):
        self.__bias += random.uniform(-1, 1) * weight_mutation_power
        if self.__bias > max_weight:
            self.__bias = max_weight
        elif self.__bias < min_weight:
            self.__bias = min_weight
    
    def copy(self):
        return NodeGene(self.__id, self.__type, self.__bias)
    
    id = property(lambda self: self.__id)
    type = property(lambda self: self.__type)
    bias = property(lambda self: self.__bias)

class ConnectionGene(object):
    __global_innov_number = 0
    __innovations = {} # A list of innovations.
    # Should it be global? Reset at every generation? Who knows?
    
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
        self.__weight += random.uniform(-1, 1) * weight_mutation_power
        if self.__weight > max_weight:
            self.__weight = max_weight
        elif self.__weight < min_weight:
            self.__weight = min_weight
    
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
        self.__node_order = [] # For feedforward networks
        self.__input_nodes = 0
        self.fitness = None
        self.species_id = None
        self.id = Chromosome.id
        Chromosome.id += 1
        
    node_genes = property(lambda self: self.__node_genes)
    conn_genes = property(lambda self: self.__connection_genes.values())
    node_order = property(lambda self: self.__node_order)
        
    def mutate(self):
        """ Mutates this chromosome """
        # TODO: review the probabilities
        r = random.random
        # Mutate weights and/or toggle connection genes
        for cg in self.__connection_genes.values():
            if r() < prob_mutate_weight:
                cg.mutate_weight()
            if r() < prob_togglelink:
                cg.enable()
        # Mutate bias (disabled by default)
        for ng in self.__node_genes[self.__input_nodes:]:
            if r() < prob_mutatebias:
                ng.mutate_bias()
                
        # Mutate adding nodes and/or connection genes
        if r() < prob_addconn:    
            self.__mutate_add_connection()
        if r() < prob_addnode:
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
        # child.__node_genes = [] # child already has this attribute
        for i, ng1 in enumerate(parent1.__node_genes):
            try:
                child.__node_genes.append(ng1.get_child(parent2.__node_genes[i]))
            except IndexError:
                child.__node_genes.append(ng1.copy())
        child.__input_nodes = parent1.__input_nodes
        child.__node_order = parent1.__node_order[:]
        # Crossover connection genes
        for cg1 in parent1.__connection_genes.values():
            try:
                cg2 = parent2.__connection_genes[cg1.key]
            except KeyError: 
                # Copy excess or disjoint genes from the fittest parent
                child.__connection_genes[cg1.key] = cg1.copy()
            else:
                if cg2.is_same_innov(cg1): # Always true for *global* INs
                    # Homologous gene found
                    # TODO: average both weights (Stanley, p. 38)
                    new_gene = random.choice((cg1, cg2)).copy()
                else:
                    new_gene = child.__connection_genes[cg1.key] = cg1.copy()
                    
                child.__connection_genes[cg1.key] = new_gene
        #child.mutate()
        #mutate the child later
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
        # Add node to node order list: after the presynaptic node of the split connection
        # and before the postsynaptic node of the split connection
        if self.__node_genes[conn_to_split.innodeid - 1].type == 'HIDDEN':
            mini = self.__node_order.index(conn_to_split.innodeid) + 1
        else:
            # Presynaptic node is an input node, not hidden node
            mini = 0
        if self.__node_genes[conn_to_split.outnodeid - 1].type == 'HIDDEN':
            maxi = self.__node_order.index(conn_to_split.outnodeid)
        else:
            # Postsynaptic node is an output node, not hidden node
            maxi = len(self.__node_order)
        self.__node_order.insert(random.randint(mini, maxi), ng.id)
    
    def __mutate_add_connection(self):
        # Only for feedforwad networks
        num_hidden = len(self.__node_order)
        num_output = len(self.__node_genes) - self.__input_nodes - num_hidden
        
        #total_possible_conns = self.__input_nodes * (num_hidden + num_output) + \
        #    num_hidden * num_output + sum(range(num_hidden))
            
        total_possible_conns = (num_hidden+num_output)*(self.__input_nodes+num_hidden) - \
            sum(range(num_hidden+1))
            
        remaining_conns = total_possible_conns - len(self.__connection_genes)
        # Check if new connection can be added:
        if remaining_conns > 0:
            n = random.randint(0, remaining_conns - 1)
            count = 0
            # Count connections
            for in_node in self.__node_genes[:-num_output]:
                for out_node in self.__node_genes[self.__input_nodes:]:
                    if (in_node.id, out_node.id) not in self.__connection_genes.keys() and \
                        self.__is_connection_feedforward(in_node, out_node):
                        # Free connection
                        if count == n: # Connection to create
                            cg = ConnectionGene(in_node.id, out_node.id, random.random(), True)
                            self.__connection_genes[cg.key] = cg
                            return
                        else:
                            count += 1
    
    def __is_connection_feedforward(self, in_node, out_node):
        return in_node.type == 'INPUT' or out_node.type == 'OUTPUT' or \
            self.__node_order.index(in_node.id) < self.__node_order.index(out_node.id)
    
# compatibility function        
    def distance(self, other):
        ''' Returns the distance between this chromosome and the other '''
        if len(self.__connection_genes) > len(other.__connection_genes):
            chromo1 = self
            chromo2 = other
        else:
            chromo1 = other
            chromo2 = self
            
        weight_diff = matching = disjoint = excess = 0
        
        max_cg_chromo2 = max(chromo2.__connection_genes.values())
            
        for cg1 in chromo1.__connection_genes.values():
            try:
                cg2 = chromo2.__connection_genes[cg1.key]
            except KeyError:
                if cg1 > max_cg_chromo2:
                    excess += 1
                else:
                    disjoint += 1
            else:
                # Homologous genes
                weight_diff += (cg1.weight - cg2.weight)
                matching += 1
        
        assert(matching > 0) # this can't happen
        distance = excess_coeficient * excess + \
                   disjoint_coeficient * disjoint + \
                   weight_coeficient * (weight_diff/matching)
                
        return distance
    
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
                cg = ConnectionGene(input_node.id, node_gene.id, random.random(), True)
                c.__connection_genes[cg.key] = cg
        return c
    
    # sort chromosomes by their fitness
    def __cmp__(self, other):
        return cmp(self.fitness, other.fitness)
    
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
    
    def size(self):
        ''' Defines chromosome 'complexity': number of hidden nodes plus
            number of enabled connections '''
            # Neuron's bias is not considered
           
        # number of hidden nodes
        num_hidden = len(self.__node_order)
        # number of enabled connections
        conns_enabled = sum([1 for cg in self.conn_genes if cg.enabled is True])
        
        return (num_hidden, conns_enabled)
    
import nn
# TODO: verify consistency!
def create_phenotype_feedforward(chromosome):
    """ Receives a chromosome and returns its phenotype (a neural network) """
    
    # bias parameter is missing (default=0)
    neurons_list = [nn.Neuron(ng.type, ng.id, ng.bias) \
                    for ng in chromosome.node_genes]
    
#    # first create inputs
#    neurons_list = [nn.Neuron(ng.type, ng.id, ng.bias) \
#                    for ng in chromosome.node_genes if ng.type == 'INPUT']
#    
#    # Add hidden nodes in the right order
#    for h in chromosome.node_order:
#        neurons_list.append(nn.Neuron(h.type, h.id, h.bias))
#        
#    # finally the output
#    neurons_list.extend([nn.Neuron(ng.type, ng.id, ng.bias) \
#                    for ng in chromosome.node_genes if ng.type == 'OUTPUT'])
    
    conn_list = [(cg.innodeid, cg.outnodeid, cg.weight) \
                 for cg in chromosome.conn_genes if cg.enabled] 
    
    return nn.Network(neurons_list, conn_list)        

if __name__ ==  '__main__':
    c1 = Chromosome.create_fully_connected(3, 2)
    print "Before mutation"
    print c1
    print
    c1.mutate()
    print "After mutation"
    print c1
    print
    c2 = Chromosome.create_fully_connected(3, 2)
    c2.mutate()
    print "A second chromosome"
    print c2
    print
    child = c2.crossover(c1)
    print "Child"
    print child
    print
    brain = create_phenotype(c1)
    print brain.sactivate([0.5, 0.5, 0.5])
    print brain
