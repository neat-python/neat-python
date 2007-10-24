import math
import neat
#from psyco.classes import *

#config.load('parameters') 
neat.Config.input_nodes = 3
neat.Config.output_nodes = 1
neat.Config.prob_addconn = 0.03
neat.Config.prob_addnode = 0.05
neat.Config.survival_threshold = 0.2
neat.Config.max_fitness_threshold = 0.9
neat.Config.compatibility_change = 0.0

# XOR-2
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

# XOR-3
INPUTS = ((0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1))
OUTPUTS = (0,1,1,0,1,0,0,1)

def eval_fitness(population):
    for chromosome in population:
        brain = neat.create_phenotype(chromosome)
        error = 0.0
        for i, input in enumerate(INPUTS):
            output = brain.activate(input) # serial activation
            error += (output[0] - OUTPUTS[i])**2
            #error += math.fabs(output[0] - OUTPUTS[i])
        #chromosome.fitness = (4.0 - error)**2 # (Stanley p. 43)        
        chromosome.fitness = 1 - math.sqrt(error/len(OUTPUTS))
        
neat.Population.evaluate = eval_fitness
pop = neat.Population(150)
pop.epoch(200, stats=True)

# Requires: PyDot -  http://code.google.com/p/pydot/downloads/list
# very, very, very draft solution for network visualizing
neat.draw_net(pop.stats[0][-1]) # best chromosome
# visualize.draw_net(max(pop.stats[0])) # must be the same as pop.stats[-1]
# Requires: biggles - http://biggles.sourceforge.net/
neat.plot_stats(pop.stats)
