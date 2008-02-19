# -*- coding: UTF-8 -*-
import random
import math
from config import Config
import copy

class NodeGene(object):    
    def __init__(self, id, nodetype, bias=0, response=4.924273):
        '''nodetype should be "INPUT", "HIDDEN", or "OUTPUT"'''
        self.__id = id
        self.__type = nodetype
        self.__bias = bias
        self.__response = response
        assert(self.__type in ('INPUT', 'OUTPUT', 'HIDDEN'))
        
    def __str__(self):
        return "Node %2d %6s, bias %+2.5s, response %+2.5s"% (self.__id, self.__type, self.__bias, self.__response)
    
    def get_child(self, other):
        ''' Creates a new NodeGene ramdonly inheriting its attributes from parents '''
        assert(self.__id == other.__id)
        
        ng = NodeGene(self.__id, self.__type,
                      random.choice((self.__bias, other.__bias)), 
                      random.choice((self.response, other.response)))
        return ng
    
    def mutate_bias(self):
        self.__bias += random.uniform(-1, 1) * Config.bias_mutation_power
        if self.__bias > Config.max_weight:
            self.__bias = Config.max_weight
        elif self.__bias < Config.min_weight:
            self.__bias = Config.min_weight
        return self
    
    def mutate_response(self):
    	''' Mutates the neuron's firing response. '''
        self.__response += random.uniform(-0.5, 0.5)
        return self
    
    def copy(self):
        return NodeGene(self.__id, self.__type, self.__bias, self.response)
    
    id = property(lambda self: self.__id)
    type = property(lambda self: self.__type)
    bias = property(lambda self: self.__bias)
    response = property(lambda self: self.__response)

class ConnectionGene(object):
    __global_innov_number = 0
    __innovations = {} # A list of innovations.
    # Should it be global? Reset at every generation? Who knows?
    
    @classmethod
    def reset_innovations(cls):
        cls.__innovations = {}
    
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
    
    weight    = property(lambda self: self.__weight)
    innodeid  = property(lambda self: self.__in)
    outnodeid = property(lambda self: self.__out)
    enabled   = property(lambda self: self.__enabled)
    # Key for dictionaries, avoids two connections between the same nodes.
    key = property(lambda self: (self.__in, self.__out))
    
    def enable(self):
        '''For the "enable link" mutation'''
        self.__enabled = True
    
    @classmethod
    def __get_new_innov_number(cls):
        cls.__global_innov_number += 1
        return cls.__global_innov_number
    
    def __str__(self):
        s = "In %2d, Out %2d, Weight %+3.5f, " % (self.__in, self.__out, self.__weight)
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
        self.__weight += random.uniform(-1, 1) * Config.weight_mutation_power
        
        if self.__weight > Config.max_weight:
            self.__weight = Config.max_weight
        elif self.__weight < Config.min_weight:
            self.__weight = Config.min_weight
    
    def copy(self):
        return ConnectionGene(self.__in, self.__out, self.__weight,
                              self.__enabled, self.__innov_number)
    
    def is_same_innov(self, cg):
        return self.__innov_number == cg.__innov_number


class Chromosome(object):
    __id = 0
    def __init__(self, parent1_id, parent2_id):
        self.__connection_genes = {} # dictionary of connection genes
        self.__node_genes = [] # list of node genes
        self.__input_nodes = 0
        
        self.fitness = None
        self.species_id = None
        
        self.__id = self.__get_new_id()
        
        self.parent1_id = parent1_id
        self.parent2_id = parent2_id
        
    node_genes = property(lambda self: self.__node_genes)
    conn_genes = property(lambda self: self.__connection_genes.values())
    
    id = property(lambda self: self.__id)
    
    @classmethod
    def __get_new_id(cls):
        cls.__id += 1
        return cls.__id
    
    def mutate(self):
        """ Mutates this chromosome """
        
        # Stanley's way...
        r = random.random
        if r() < Config.prob_addnode:
            self.__mutate_add_node()
        elif r() < Config.prob_addconn:
            self.__mutate_add_connection()
        else: # if no structural mutation occured
            for cg in self.__connection_genes.values():
                if r() < Config.prob_mutate_weight:
                    cg.mutate_weight()
                if r() < Config.prob_togglelink:
                    cg.enable()
            for ng in self.__node_genes[self.__input_nodes:]:
                if r() < Config.prob_mutatebias:
                    ng.mutate_bias()
                    
        # Simmerson's way... behaves as good (or bad?) as Stanley's!
#        for cg in self.__connection_genes.values():
#            if r() < Config.prob_mutate_weight:
#                cg.mutate_weight()
#            if r() < Config.prob_togglelink:
#                cg.enable()
#                
#        for ng in self.__node_genes[self.__input_nodes:]:
#            if r() < Config.prob_mutatebias:
#                ng.mutate_bias()
#                ng.mutate_response()
#        
#        if r() < Config.prob_addconn:
#            self.__mutate_add_connection()
#            
#        if r() < Config.prob_addnode:
#            self.__mutate_add_node()
        
#        for cg in self.__connection_genes.values():
#            if r() < Config.prob_mutate_weight:
#                cg.mutate_weight()
#            if r() < Config.prob_togglelink:
#                cg.enable()
#        for ng in self.__node_genes[self.__input_nodes:]:
#            if r() < Config.prob_mutatebias:
#                ng.mutate_bias()
#        if r() < Config.prob_addconn:    
#            self.__mutate_add_connection()
#        if r() < Config.prob_addnode:
#            self.__mutate_add_node()

        return self

    
    def crossover(self, other):
        ''' Applies the crossover operator. Returns a child '''
        child = self.__class__(self.id, other.id)
        # TODO: if they're of equal fitnesses, choose the shortest 
        if self.fitness > other.fitness:
            parent1 = self
            parent2 = other
        else:
            parent1 = other
            parent2 = self
            
        child.__inherit_genes(parent1, parent2)        
        assert parent1.species_id == parent2.species_id, 'Different parents species ID: %d vs %d' \
                                                            % (parent1.species_id, parent2.species_id)
        child.species_id = parent1.species_id
        
        return child
    
    def __inherit_genes(child, parent1, parent2):
        assert(parent1.fitness >= parent2.fitness)
        
    def __inherit_genes(child, parent1, parent2):
        assert(parent1.fitness >= parent2.fitness)
        
        # Crossover node genes
        for i, ng1 in enumerate(parent1.__node_genes):
            try:
                # matching node genes: randomly selects the neuron's bias and response 
                child.__node_genes.append(ng1.get_child(parent2.__node_genes[i]))
            except IndexError:
                # copies extra genes from the fittest parent
                child.__node_genes.append(ng1.copy())
                
        child.__input_nodes = parent1.__input_nodes
        
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
                    new_gene.enable() # avoids disconnected neurons
                else:
                    new_gene = child.__connection_genes[cg1.key] = cg1.copy()
                child.__connection_genes[cg1.key] = new_gene
   
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
        return (ng, conn_to_split)
    
    def __mutate_add_connection(self):
        # Only for recurrent networks
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
                            weight = random.uniform(-Config.random_range, Config.random_range)
                            cg = ConnectionGene(in_node.id, out_node.id, weight, True)
                            self.__connection_genes[cg.key] = cg
                            return
                        else:
                            count += 1
    
# compatibility function        
    def distance(self, other):
        ''' Returns the distance between this chromosome and the other '''
        if len(self.__connection_genes) > len(other.__connection_genes):
            chromo1 = self
            chromo2 = other
        else:
            chromo1 = other
            chromo2 = self
            
        weight_diff = 0
        matching = 0
        disjoint = 0
        excess = 0
        
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
                weight_diff += math.fabs(cg1.weight - cg2.weight)
                matching += 1

        disjoint += len(chromo2.__connection_genes) - matching
        
        assert(matching > 0) # this can't happen
        distance = Config.excess_coeficient * excess + \
                   Config.disjoint_coeficient * disjoint + \
                   Config.weight_coeficient * (weight_diff/matching)
                
        return distance
    
    def size(self):
        ''' Defines chromosome 'complexity': number of hidden nodes plus
            number of enabled connections '''
            # Neuron's bias is not considered
           
        # number of hidden nodes
        num_hidden = len(self.__node_genes) - Config.input_nodes - Config.output_nodes
        # number of enabled connections
        conns_enabled = sum([1 for cg in self.conn_genes if cg.enabled is True])
        
        return (num_hidden, conns_enabled)
    
    @classmethod
    def create_fully_connected(cls, num_input, num_output):
        '''
        Factory method
        Creates a chromosome for a fully connected network with no hidden nodes.
        '''
        c = cls(0,0)
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
                weight = random.uniform(-Config.random_range, Config.random_range)
                cg = ConnectionGene(input_node.id, node_gene.id, weight, True)
                c.__connection_genes[cg.key] = cg
        return c

#   For fixed-topology experiments
#	Specifies a pre-defined topology for the XOR experiment
#    @classmethod
#    def create_fully_connected(cls, num_input, num_output):
#        '''
#        Factory method
#        Creates a chromosome for a fully connected network with no hidden nodes.
#        '''
#        c = cls()
#        id = 1
#        # Create node genes
#        for i in range(num_input):
#            c.__node_genes.append(NodeGene(id, 'INPUT'))
#            id += 1
#        c.__input_nodes += num_input
#        
#        for i in range(num_output):
#            node_gene = NodeGene(id, 'OUTPUT')
#            c.__node_genes.append(node_gene)
#            id += 1
#            
#        # hidden node
#        node_gene = NodeGene(id, 'HIDDEN')   
#        c.__node_genes.append(node_gene)
#        id += 1
#        
#        node_gene = NodeGene(id, 'HIDDEN')   
#        c.__node_genes.append(node_gene)
#        id += 1
#        
#        # A network setting that solves 2-XOR
#        weight = random.uniform(-Config.random_range, Config.random_range)    
#        #weight = 2.751764    
#        cg = ConnectionGene(1, 4, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        weight = random.uniform(-Config.random_range, Config.random_range)    
#        #weight = -2.29486
#        cg = ConnectionGene(1, 5, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        weight = random.uniform(-Config.random_range, Config.random_range)
#        #weight = -0.60735
#        cg = ConnectionGene(1, 3, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        weight = random.uniform(-Config.random_range, Config.random_range)
#        #weight = 3.124543
#        cg = ConnectionGene(2, 4, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        weight = random.uniform(-Config.random_range, Config.random_range)   
#        #weight = 3.883385     
#        cg = ConnectionGene(2, 5, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        weight = random.uniform(-Config.random_range, Config.random_range)
#        #weight = 1.178918
#        cg = ConnectionGene(2, 3, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        weight = random.uniform(-Config.random_range, Config.random_range)
#        #weight = 0.868042
#        cg = ConnectionGene(4, 3, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        weight = random.uniform(-Config.random_range, Config.random_range)
#        #weight = -1.820959        
#        cg = ConnectionGene(5, 3, weight, True)
#        c.__connection_genes[cg.key] = cg
#        
#        return c

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
    
#    def __deepcopy__(self):
#        c = self.__class__()
#        c.fitness = self.fitness
#        c.species_id = self.species_id
#        #assert c.id == self.id, 'Different ids'
#        for k, v in self.__connection_genes.items():
#            c.__connection_genes[k] = v
#        c.__node_genes = self.__node_genes[:]
#        c.__input_nodes = self.__input_nodes
#        return c
    
def create_phenotype(chromosome):
    """ Receives a chromosome and returns its phenotype (a neural network) """
    import nn
    # bias parameter is missing (default=0)
    neurons_list = [nn.Neuron(ng.type, ng.id, ng.bias, ng.response) \
                    for ng in chromosome.node_genes]
    
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
