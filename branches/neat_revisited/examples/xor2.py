import math
from neat import config, population, chromosome, genome2, visualize
from neat import nn
#from psyco.classes import *

config.load('xor2_config') 

# Temporary workaround
chromosome.node_gene_type = genome2.NodeGene

# XOR-2
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

def eval_fitness(population):
    for chromo in population:
        brain = nn.create_ffphenotype(chromo)
        error = 0.0
        for i, input in enumerate(INPUTS):
            output = brain.activate(input) # serial activation
            error += (output[0] - OUTPUTS[i])**2
            #error += math.fabs(output[0] - OUTPUTS[i])
        #chromosome.fitness = (4.0 - error)**2 # (Stanley p. 43)        
        chromo.fitness = 1 - math.sqrt(error/len(OUTPUTS))
        
population.Population.evaluate = eval_fitness
pop = population.Population()
pop.epoch(200, stats=1, save_best=0)

# Draft solution for network visualizing
visualize.draw_net(pop.stats[0][-1]) # best chromosome
# Plots the evolution of the best/average fitness
visualize.plot_stats(pop.stats)
# Visualizes speciation
#visualize.plot_species(pop.species_log)

# Let's check if it's really solved the problem
print 'Best network output'
brain = nn.create_ffphenotype(pop.stats[0][-1])
for i, input in enumerate(INPUTS):
    output = brain.activate(input) # serial activation
    print OUTPUTS[i], output[0]
    

# saves the winner
#file = open('winner_chromosome', 'w')
#pickle.dump(pop.stats[0][-1], file)
#file.close()
