import math


from neat import config, population, genome_feedforward, visualize, spiking_nn
config.Config.output_nodes = 2
config.Config.prob_addconn = 0.01
config.Config.prob_addnode = 0.005

# XOR-2
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

# For how long are we going to wait for an answer from the network?
MAX_TIME = 500 # in miliseconds of simulation time

def eval_fitness(population):
    for chromosome in population:
        brain = spiking_nn.create_phenotype(chromosome)
        error = 0.0
        for i, input in enumerate(INPUTS):
            for j in range(MAX_TIME):
                output = brain.advance([i * 10 for i in input])
                if output != [False, False]:
                    break
            if output[0] and not output[1]: # Network answered 1
                error += (1 - OUTPUTS[i])**2
            elif not output[0] and output[1]: # Network answered 0
                error += (0 - OUTPUTS[i])**2
            else: # No answer or ambiguous
                error += 1
        chromosome.fitness = 1 - math.sqrt(error/len(OUTPUTS))
        if not chromosome.fitness:
            chromosome.fitness = 0.00001

population.Population.evaluate = eval_fitness
pop = population.Population(30)
pop.epoch(1500)

# Requires: PyDot -  http://code.google.com/p/pydot/downloads/list
# very, very, very draft solution for network visualizing
visualize.draw_net(pop.stats[0][-1]) # best chromosome
# visualize.draw_net(max(pop.stats[0])) # must be the same as pop.stats[-1]
# Requires: biggles - http://biggles.sourceforge.net/
visualize.plot_stats(pop.stats)
