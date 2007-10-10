import math
import neat

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
        
        chromosome.fitness = (1.0 - math.sqrt(error/len(OUTPUTS)))
        
neat.Population.evaluate = eval_fitness
pop = neat.Population(150)
pop.epoch(30)
