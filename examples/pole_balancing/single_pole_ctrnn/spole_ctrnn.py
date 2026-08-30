# ******************************** #
# Single pole balancing experiment #
# ******************************** #

from neat import config, population, chromosome, genome, visualize
from neat import ctrnn
import math
import random
import pickle

rstate = random.getstate()

save = open('rstate', 'wb')
pickle.dump(rstate, save)
save.close()


def cart_pole(net_output, x, x_dot, theta, theta_dot):
    ''' Directly copied from Stanley's C++ source code '''

    GRAVITY = 9.8
    MASSCART = 1.0
    MASSPOLE = 0.1
    TOTAL_MASS = (MASSPOLE + MASSCART)
    LENGTH = 0.5    # actually half the pole's length
    POLEMASS_LENGTH = (MASSPOLE * LENGTH)
    FORCE_MAG = 10.0
    TAU = 0.02  # seconds between state updates
    FOURTHIRDS = 1.3333333333333

    if net_output > 0.5:
        force = FORCE_MAG
    else:
        force = -FORCE_MAG

    costheta = math.cos(theta)
    sintheta = math.sin(theta)

    temp = (force + POLEMASS_LENGTH * theta_dot * theta_dot * sintheta) / TOTAL_MASS

    thetaacc = (GRAVITY * sintheta - costheta * temp) \
               / (LENGTH * (FOURTHIRDS - MASSPOLE * costheta * costheta / TOTAL_MASS))

    xacc = temp - POLEMASS_LENGTH * thetaacc * costheta / TOTAL_MASS

    # Update the four state variables, using Euler's method
    x += TAU * x_dot
    x_dot += TAU * xacc
    theta += TAU * theta_dot
    theta_dot += TAU * thetaacc

    return x, x_dot, theta, theta_dot


def evaluate_population(population):

    twelve_degrees = 0.2094384  # radians
    num_steps = 10 ** 5

    for chromo in population:

        net = ctrnn.create_phenotype(chromo)

        # initial conditions (as used by Stanley)
        x = (random.randint(0, 2 ** 31) % 4800) / 1000.0 - 2.4
        x_dot = (random.randint(0, 2 ** 31) % 2000) / 1000.0 - 1
        theta = (random.randint(0, 2 ** 31) % 400) / 1000.0 - .2
        theta_dot = (random.randint(0, 2 ** 31) % 3000) / 1000.0 - 1.5

        fitness = 0

        for trials in range(num_steps):
            # maps into [0,1]
            inputs = [(x + 2.4) / 4.8,
                      (x_dot + 0.75) / 1.5,
                      (theta + twelve_degrees) / 0.41,
                      (theta_dot + 1.0) / 2.0]

            action = net.pactivate(inputs)

            # Apply action to the simulated cart-pole
            x, x_dot, theta, theta_dot = cart_pole(action[0], x, x_dot, theta, theta_dot)

            # Check for failure.  If so, return steps
            # the number of steps indicates the fitness: higher = better
            fitness += 1
            if (abs(x) >= 2.5 or abs(theta) >= twelve_degrees):
                break

        chromo.fitness = fitness


if __name__ == "__main__":

    config.load('spole_ctrnn_config')

    # Temporary workaround
    chromosome.node_gene_type = genome.CTNodeGene

    population.Population.evaluate = evaluate_population
    pop = population.Population()
    pop.epoch(2000, report=1, save_best=0)

    print('Number of evaluations: %d' % (pop.stats[0][-1]).id)

    # saves the winner
    fp = open('winner_chromosome', 'wb')
    pickle.dump(pop.stats[0][-1], fp)
    fp.close()

    print(pop.stats[0][-1])
