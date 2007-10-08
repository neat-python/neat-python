from neat import nn

INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
OUTPUTS = (0, 1, 1, 0)

def calculate_fitness(chromosome):
    return