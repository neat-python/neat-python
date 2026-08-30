# ******************************** #
# Double pole balancing experiment #
# ******************************** #
import pickle
from time import strftime

from neat import config, population, chromosome, genome
from cart_pole import CartPole


def evaluate_population(population):

    simulation = CartPole(population, markov=False)
    # comment this line to print the status
    simulation.print_status = False
    simulation.run()


if __name__ == "__main__":

    config.load('cpExp_config')

    # change the number of inputs accordingly to the type
    # of experiment: markov (6) or non-markov (3)
    # you can also set the configs in dpole_config as long
    # as you have two config files for each type of experiment
    config.Config.input_nodes = 3

    # neuron model type
    chromosome.node_gene_type = genome.NodeGene

    population.Population.evaluate = evaluate_population
    pop = population.Population()
    pop.epoch(500, report=1, save_best=0)

    winner = pop.stats[0][-1]

    print('Number of evaluations: %d' % winner.id)
    print('Winner score: %d' % winner.score)
    date = strftime("%Y_%m_%d_%Hh%Mm%Ss")
    # saves the winner
    fp = open('winner_' + date, 'wb')
    pickle.dump(winner, fp)
    fp.close()
