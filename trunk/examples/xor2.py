import math
import neat

#config.load('parameters') 

# why tuples and not lists?
INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

def calculate_fitness(chromosome):
    brain = neat.create_phenotype(chromosome)
    
    error = 0.0
    for i, input in enumerate(INPUTS):
        output = brain.sactivate(input) # serial activation
        error += (output - OUTPUTS[i])**2
        
    return (1.0 - math.sqrt(error/len(OUTPUTS)))

pop = neat.Population(30)
pop.epoch(3)

