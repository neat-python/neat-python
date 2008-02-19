# -*- coding: UTF-8 -*-
from config import Config
import genome
import random

#random.seed(0)

class Chromosome(genome.Chromosome):
    def __init__(self, parent1_id, parent2_id):
        super(Chromosome, self).__init__(parent1_id, parent2_id)
        self.__node_order = [] # For feedforward networks
        #self.__node_order = [4, 5] # used only in fixed-topology experiments (using a pre-defined topology in genome.py)
        
    node_order = property(lambda self: self.__node_order)
    
    def __inherit_genes(child, parent1, parent2):
        super(Chromosome, child).__inherit_genes(parent1, parent2)
        child.__node_order = parent1.__node_order[:]
        assert(len(child.__node_order) == len([n for n in child.node_genes if n.type == 'HIDDEN']))
    
    def __mutate_add_node(self):
        ng, split_conn = super(Chromosome, self).__mutate_add_node()
        # Add node to node order list: after the presynaptic node of the split connection
        # and before the postsynaptic node of the split connection
        if self.__node_genes[split_conn.innodeid - 1].type == 'HIDDEN':
            mini = self.__node_order.index(split_conn.innodeid) + 1
        else:
            # Presynaptic node is an input node, not hidden node
            mini = 0
        if self.__node_genes[split_conn.outnodeid - 1].type == 'HIDDEN':
            maxi = self.__node_order.index(split_conn.outnodeid)
        else:
            # Postsynaptic node is an output node, not hidden node
            maxi = len(self.__node_order)
        self.__node_order.insert(random.randint(mini, maxi), ng.id)
        assert(len(self.__node_order) == len([n for n in self.node_genes if n.type == 'HIDDEN']))
        return (ng, split_conn)
    
    def __mutate_add_connection(self):
        # Only for feedforwad networks
        num_hidden = len(self.__node_order)
        num_output = len(self.__node_genes) - self.__input_nodes - num_hidden
        
        total_possible_conns = (num_hidden+num_output)*(self.__input_nodes+num_hidden) - \
            sum(range(num_hidden+1))
            
        remaining_conns = total_possible_conns - len(self.__connection_genes)
        # Check if new connection can be added:
        if remaining_conns > 0:
            n = random.randint(0, remaining_conns - 1)
            count = 0
            # Count connections
            for in_node in (self.__node_genes[:self.__input_nodes] + self.__node_genes[-num_hidden:]):
                for out_node in self.__node_genes[self.__input_nodes:]:
                    if (in_node.id, out_node.id) not in self.__connection_genes.keys() and \
                        self.__is_connection_feedforward(in_node, out_node):
                        # Free connection
                        if count == n: # Connection to create
                            weight = random.uniform(-Config.random_range, Config.random_range)
                            cg = genome.ConnectionGene(in_node.id, out_node.id, weight, True)
                            self.__connection_genes[cg.key] = cg
                            return
                        else:
                            count += 1
    
    def __is_connection_feedforward(self, in_node, out_node):
        return in_node.type == 'INPUT' or out_node.type == 'OUTPUT' or \
            self.__node_order.index(in_node.id) < self.__node_order.index(out_node.id)
    
    def __str__(self):
        s = super(Chromosome, self).__str__()
        s += '\nNode order: ' + str(self.node_order)
        return s
    
import nn

def create_phenotype(chromosome):
    """ Receives a chromosome and returns its phenotype (a neural network) """
    
    # first create inputs
    neurons_list = [nn.Neuron('INPUT', i.id, 0, 0) \
                    for i in chromosome.node_genes if i.type == 'INPUT']
    
    # Add hidden nodes in the right order
    for id in chromosome.node_order:
        neurons_list.append(nn.Neuron('HIDDEN', id, chromosome.node_genes[id - 1].bias, chromosome.node_genes[id - 1].response))
        
    # finally the output
    neurons_list.extend(nn.Neuron('OUTPUT', o.id, o.bias, o.response) \
                        for o in chromosome.node_genes if o.type == 'OUTPUT')
    
    assert(len(neurons_list) == len(chromosome.node_genes))
    
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
