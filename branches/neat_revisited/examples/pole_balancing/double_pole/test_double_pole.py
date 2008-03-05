# test single pole performance

from neat import config, chromosome, genome2
from neat import nn
import random
import cPickle as pickle
from cart_pole import CartPole

chromosome.node_gene_type = genome2.NodeGene

# load the winner
file = open('winner_chromosome', 'r')
c = pickle.load(file)
file.close()


config.load('dpole_config')
net = nn.create_phenotype(c)


cart = CartPole(net, markov=True)
                
print cart.evaluate(10**5, test=True)
    
