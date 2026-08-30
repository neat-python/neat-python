# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------#
# A parallel version of XOR using concurrent.futures.                   #
#                                                                       #
# Since XOR is a simple experiment, a parallel version won't actually   #
# take any advantages of it due to overhead and transfer-communication. #
# The example below is only a general idea of how to implement a        #
# parallel experiment in neat-python.                                   #
# ----------------------------------------------------------------------#
import math
import os
from concurrent.futures import ProcessPoolExecutor

from neat import config, population, chromosome, genome

config.load('xor2_config')

config.Config.max_fitness_threshold = 0.9
config.Config.pop_size = 150
# Temporary workaround
chromosome.node_gene_type = genome.NodeGene

NUM_CHUNKS = 2


def eval_fitness(population):
    size = config.Config.pop_size // NUM_CHUNKS
    assert config.Config.pop_size % NUM_CHUNKS == 0, "Population size is not multiple of num_chunks"

    chunks = []
    for k in range(NUM_CHUNKS):
        print('Chunk %d:  [%3d:%3d]' % (k, size * k, size * (k + 1)))
        chunks.append(list(population[size * k:size * (k + 1)]))

    with ProcessPoolExecutor(max_workers=NUM_CHUNKS) as executor:
        results = list(executor.map(parallel_evaluation, chunks, range(NUM_CHUNKS)))

    all_jobs = []
    for chunk_fitness in results:
        all_jobs += chunk_fitness
    for i, fitness in enumerate(all_jobs):
        population[i].fitness = fitness


def parallel_evaluation(sub_pop, chunk):
    from neat.nn import nn_pure as nn

    print("Evaluating chunk %d at %s" % (chunk, os.popen("hostname").read().strip()))

    INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
    OUTPUTS = (0, 1, 1, 0)

    fitness = []
    for c in sub_pop:
        net = nn.create_ffphenotype(c)

        error = 0.0
        for i, input in enumerate(INPUTS):
            output = net.sactivate(input)  # serial activation
            error += (output[0] - OUTPUTS[i]) ** 2

        fitness.append(1 - math.sqrt(error / len(OUTPUTS)))

    return fitness


if __name__ == '__main__':
    population.Population.evaluate = eval_fitness
    pop = population.Population()
    pop.epoch(400, report=1, save_best=False)
