import math
from neat import config, population, genome_feedforward, genome, visualize
#from psyco.classes import *

#config.load('parameters') 
config.Config.input_nodes = 2
config.Config.output_nodes = 1
config.Config.survival_threshold = 0.1
config.Config.max_fitness_threshold = 0.9
config.Config.compatibility_change = 0.0
config.Config.nn_allow_recurrence = False
config.Config.nn_activation = 'exp'

# Human reasoning
#config.Config.prob_addconn          = 0.03
#config.Config.prob_addnode          = 0.05
#config.Config.prob_mutatebias       = 0.2
#config.Config.bias_mutation_power   = 0.5
#config.Config.prob_mutate_weight    = 0.25
#config.Config.weight_mutation_power = 1.5
#config.Config.prob_togglelink       = 0.1

# Parameters obtained with a meta-SGA
config.Config.prob_addconn          = 0.32064768257848786
config.Config.prob_addnode          = 0.079877505580863845
config.Config.prob_mutatebias       = 0.26320591007566424
config.Config.bias_mutation_power   = 0.21543442675620872
config.Config.prob_mutate_weight    = 0.5
config.Config.weight_mutation_power = 0.45428647964797569
config.Config.prob_togglelink       = 0.024390995616214557

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
            output = brain.sactivate(input) # serial activation
            error += (output[0] - OUTPUTS[i])**2
            #error += math.fabs(output[0] - OUTPUTS[i])
        #chromosome.fitness = (4.0 - error)**2 # (Stanley p. 43)        
        chromosome.fitness = 1 - math.sqrt(error/len(OUTPUTS))
        
population.Population.evaluate = eval_fitness
pop = population.Population(150)
pop.epoch(200, stats=True, save_best=False)

# Draft solution for network visualizing
visualize.draw_net(pop.stats[0][-1]) # best chromosome
# Plots the evolution of the best/average fitness
visualize.plot_stats(pop.stats)
# Visualizes speciation
visualize.plot_species(pop.species_log)

# Let's check if it's really solved the problem
print 'Best network output'
for i, input in enumerate(INPUTS):
    brain = genome_feedforward.create_phenotype(pop.stats[0][-1])
    output = brain.activate(input) # serial activation
    print OUTPUTS[i], output[0]
