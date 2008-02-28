from neat import config, population, chromosome, genome2, visualize
from neat import nn
import math, random

def cart_pole(action, x, x_dot, theta, theta_dot):
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

    #force = (action>0)? FORCE_MAG : -FORCE_MAG
    force = FORCE_MAG if action > 0.5 else -FORCE_MAG
      
    costheta = math.cos(theta)
    sintheta = math.sin(theta)
      
    temp = (force + POLEMASS_LENGTH * theta_dot * theta_dot * sintheta)/ TOTAL_MASS
     
    thetaacc = (GRAVITY*sintheta - costheta*temp)\
               /(LENGTH * (FOURTHIRDS - MASSPOLE * costheta * costheta/TOTAL_MASS))
      
    xacc  = temp - POLEMASS_LENGTH * thetaacc * costheta / TOTAL_MASS
      
    #Update the four state variables, using Euler's method      
    x         += TAU * x_dot
    x_dot     += TAU * xacc
    theta     += TAU * theta_dot
    theta_dot += TAU * thetaacc
      
    return x, x_dot, theta, theta_dot
    
def evaluate_population(population):
    
    twelve_degrees=0.2094384
    num_steps = 100000
    
    for chromo in population:
        
        net = nn.create_phenotype(chromo)
        
        r = random.randint
        # initial conditions
        x         = (r(0, 2**31)%4800)/1000.0 -2.4  # cart position, meters 
        x_dot     = (r(0, 2**31)%2000)/1000.0 - 1   # cart velocity
        theta     = (r(0, 2**31)%400)/1000.0 - .2   # pole angle, radians
        theta_dot = (r(0, 2**31)%3000)/1000.0 - 1.5 # pole angular velocity
        
        fitness = 0
        
        for trials in xrange(num_steps):
        
            # map inputs into [0,1]
            inputs = [(x + 2.4)/4.8, 
                      (x_dot + .75)/1.5,
                      (theta + twelve_degrees)/0.41,
                      (theta_dot + 1.0) / 2.0]
                      
            action = net.sactivate(inputs)
            
            # Apply action to the simulated cart-pole
            x, x_dot, theta, theta_dot = cart_pole(action[0], x, x_dot, theta, theta_dot)
            
            # Check for failure.  If so, return steps
            # the number of steps indicates the fitness: higher = better
            fitness += 1
            if (x < -2.4 or x > 2.4 or theta < -twelve_degrees or theta > twelve_degrees):
                # the cart/pole has run/inclined out of the limits
                break;
            
        chromo.fitness = fitness

if __name__ == "__main__":
    
    config.load('spole_config') 

    # Temporary workaround
    chromosome.node_gene_type = genome2.NodeGene
    
    population.Population.evaluate = evaluate_population
    pop = population.Population()
    pop.epoch(200, stats=1, save_best=0)
    
    # visualize the best topology
    visualize.draw_net(pop.stats[0][-1]) # best chromosome
    # Plots the evolution of the best/average fitness
    visualize.plot_stats(pop.stats)
