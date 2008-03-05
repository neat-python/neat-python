import math
import cPickle as pickle
from neat import config, single_population, chromosome, genome2, visualize
#from psyco.classes import *
import random

#rstate = random.getstate()

#save = open('rstate','w')
#pickle.dump(rstate, save)
#save.close()

#dumped = open('rstate','r')
#rstate = pickle.load(dumped)
#random.setstate(rstate)
#dumped.close()

chromosome.node_gene_type = genome2.CTNodeGene
chromosome.conn_gene_type = genome2.ConnectionGene

config.load('xor2_config') 

config.Config.input_nodes = 2

config.Config.feedforward = 0

config.Config.pop_size = 100
config.Config.compatibility_threshold = 3
config.Config.max_fitness_threshold = 0.9

config.Config.prob_addconn   = 0.05
config.Config.prob_addnode   = 0.03 
#config.Config.random_range   = 3
#config.Config.weight_mutation_power = 1.5
config.Config.survival_threshold = 0.1

# XOR-2
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

#INPUTS = ((0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1))
#OUTPUTS = (0,1,1,0,1,0,0,1)

MAX_TIME = 50

def eval_fitness(population):
    for chromo in population:
        brain = chromosome.create_phenotype(chromo)
        error = 0.0

        for i, input in enumerate(INPUTS):
            # compute MAX_TIME number of steps before returning the result
            for k in xrange(MAX_TIME):                
                output = brain.pactivate(input)
            
            #error += abs(output[0] - OUTPUTS[i])
            error += (output[0] - OUTPUTS[i])**2
            
        #chromo.fitness = (4.0 - error)**2 # (Stanley p. 43)
        chromo.fitness = 1.0 - math.sqrt(error/len(OUTPUTS))
        
        #print '%2d - %1.5s %1.5s' %(chromosome.id, error2, chromosome.fitness)
        
single_population.Population.evaluate = eval_fitness
pop = single_population.Population()
pop.epoch(2000, stats=1, save_best=0)

## Draft solution for network visualizing
visualize.draw_net(pop.stats[0][-1]) # best chromosome
## Plots the evolution of the best/average fitness
visualize.plot_stats(pop.stats)
## Visualizes speciation
#visualize.plot_species(pop.species_log)
#
## Let's check if it's really solved the problem
print 'Best network output'
brain = chromosome.create_phenotype(pop.stats[0][-1])
for i, input in enumerate(INPUTS):    
    for k in xrange(MAX_TIME):                
                output = brain.pactivate(input)
    print OUTPUTS[i], output[0]
    
# saves the winner
file = open('winner_chromosome', 'w')
pickle.dump(pop.stats[0][-1], file)
file.close()

