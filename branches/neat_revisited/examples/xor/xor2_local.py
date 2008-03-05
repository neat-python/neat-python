from neat import config, single_population, chromosome, genome2, visualize
from neat import nn
import cPickle as pickle
import math, random
#import psyco; psyco.full()

#rstate = random.getstate()

#save = open('rstate','w')
#pickle.dump(rstate, save)
#save.close()

#dumped = open('rstate','r')
#rstate = pickle.load(dumped)
#random.setstate(rstate)
#dumped.close()


config.load('xor2_config') 

# Temporary workaround
chromosome.node_gene_type = genome2.NodeGene

config.Config.input_nodes = 2

config.Config.feedforward = 1

config.Config.pop_size = 150
config.Config.max_fitness_threshold = 14.9

config.Config.prob_addconn   = 0.05
config.Config.prob_addnode   = 0.03 

#config.Config.weight_mutation_power = 1.5
config.Config.survival_threshold = 0.3

# XOR-2
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

def eval_fitness(population):
    for chromo in population:
        brain = nn.create_ffphenotype(chromo)
        error = 0.0

        for i, input in enumerate(INPUTS):
            output = brain.sactivate(input) # serial activation
            
            error += abs(output[0] - OUTPUTS[i])
            #error += (output[0] - OUTPUTS[i])**2
            
        chromo.fitness = (4.0 - error)**2 # (Stanley p. 43)
        #chromo.fitness = 1.0 - math.sqrt(error/len(OUTPUTS))
        
        #print '%2d - %1.5s %1.5s' %(chromosome.id, error2, chromosome.fitness)
        
single_population.Population.evaluate = eval_fitness
pop = single_population.Population()
pop.epoch(500, stats=1, save_best=0)

## Draft solution for network visualizing
#visualize.draw_net(pop.stats[0][-1]) # best chromosome
## Plots the evolution of the best/average fitness
#visualize.plot_stats(pop.stats)
## Visualizes speciation
#visualize.plot_species(pop.species_log)
#
## Let's check if it's really solved the problem
print '\nBest network output'
brain = nn.create_ffphenotype(pop.stats[0][-1])
for i, input in enumerate(INPUTS):    
    output = brain.sactivate(input) # serial activation
    print OUTPUTS[i], output[0]
    
# saves the winner
#file = open('winner_chromosome', 'w')
#pickle.dump(pop.stats[0][-1], file)
#file.close()

