# ******************************** #
# Double pole balancing experiment #
# ******************************** #
from neat import config, population, chromosome, genome2, visualize
import math, random
import cPickle as pickle
from cart_pole import CartPole

def evaluate_population(population):
       
    simulation = CartPole(population, markov = False)
    simulation.run()
   

if __name__ == "__main__":
    
    config.load('dpole_config') 
    
    # change the number of inputs accordingly to the type
    # of experiment: markov (6) or non-markov (3)
    # you can also set the configs in dpole_config as long
    # as you have two config files for each type of experiment
    config.Config.input_nodes = 3
    config.Config.pop_size = 100

    # Temporary workaround
    chromosome.node_gene_type = genome2.NodeGene
    
    population.Population.evaluate = evaluate_population
    pop = population.Population()
    pop.epoch(200, report=1, save_best=0)
    
    # visualize the best topology
    visualize.draw_net(pop.stats[0][-1]) # best chromosome
    # Plots the evolution of the best/average fitness
    visualize.plot_stats(pop.stats)
    
    print 'Number of evaluations: %d' %(pop.stats[0][-1]).id
    
    # saves the winner
    file = open('winner_chromosome', 'w')
    pickle.dump(pop.stats[0][-1], file)
    file.close()
