import math
import neat
import visualize
#from psyco.classes import *

#config.load('parameters') 

INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

def eval_fitness(population):
    for chromosome in population:
        brain = neat.create_phenotype(chromosome)
        error = 0.0
        for i, input in enumerate(INPUTS):
            output = brain.sactivate(input) # serial activation
            error += (output[0] - OUTPUTS[i])**2
            #error += math.fabs(output[0] - OUTPUTS[i])
        
        #chromosome.fitness = (4.0 - error)**2 # (Stanley p. 43)
        chromosome.fitness = 1 - math.sqrt(error/len(OUTPUTS))
        
neat.Population.evaluate = eval_fitness
pop = neat.Population(150)
pop.epoch(16)

# Requires: PyDot -  http://code.google.com/p/pydot/downloads/list
# very, very, very draft solution for network visualizing
visualize.draw_net(pop.stats[0][-1]) # best chromosome
# visualize.draw_net(max(pop.stats)) # must be the same as pop.stats[-1]
# Requires: biggles - http://biggles.sourceforge.net/
visualize.plot_stats(pop.stats)
