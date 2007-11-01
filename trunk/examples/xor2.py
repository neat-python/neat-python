import math
from neat import config, population, genome_feedforward, genome, visualize
#from psyco.classes import *

#config.load('parameters') 
config.Config.input_nodes = 2
config.Config.output_nodes = 1
config.Config.prob_addconn = 0.03
config.Config.prob_addnode = 0.05
config.Config.survival_threshold = 0.1
config.Config.max_fitness_threshold = 0.9
config.Config.compatibility_change = 0.0
config.Config.nn_allow_recurrence = False
config.Config.nn_activation = 'exp'

# XOR-2
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

# XOR-3
#INPUTS = ((0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1))
#OUTPUTS = (0,1,1,0,1,0,0,1)

def eval_fitness(population):
    for chromosome in population:
        brain = genome_feedforward.create_phenotype(chromosome)
        error = 0.0
        for i, input in enumerate(INPUTS):
            output = brain.activate(input) # serial activation
            error += (output[0] - OUTPUTS[i])**2
            #error += math.fabs(output[0] - OUTPUTS[i])
        #chromosome.fitness = (4.0 - error)**2 # (Stanley p. 43)        
        chromosome.fitness = 1 - math.sqrt(error/len(OUTPUTS))
        
population.Population.evaluate = eval_fitness
pop = population.Population(150)
pop.epoch(200, stats=True)

# Requires: PyDot -  http://code.google.com/p/pydot/downloads/list
# very, very, very draft solution for network visualizing
visualize.draw_net(pop.stats[0][-1]) # best chromosome
# visualize.draw_net(max(pop.stats[0])) # must be the same as pop.stats[-1]
# Requires: biggles - http://biggles.sourceforge.net/
visualize.plot_stats(pop.stats)
