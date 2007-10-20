# sets the configuration parameters for NEAT
       
def load(file):
    try:
        parameters = open('file','r')
    except IOError:
        print 'Error: file %s not found!' %file
    #else:
        # set class attributes
        

class Config: # read from file
    # network type
    nn_allow_recurrence = False
    
    # phenotype config
    input_nodes = 2
    output_nodes = 1
    max_weight = 500
    min_weight = -500
    random_range = 1.5 # experimental
    
    # mutation probabilities
    prob_addconn = 0.05
    prob_addnode = 0.03    
    prob_mutatebias = 0.1
    bias_mutation_power = 0.5    
    prob_mutate_weight = 0.55 # dynamic mutation rate (future release)
    weight_mutation_power = 0.5    
    prob_togglelink = 0.05
    
    #prob_crossover = 0.7  # not implemented (always apply crossover)
    #prob_weightreplaced = 0.0 # not implemented
    
    # genetic algorithm parameters
    #pop_size = 50        # set when initializing population
    #number_epochs = 1000 # set when initializing population
    
    # genotype compatibility 
    compatibility_threshold = 3.0
    compatibility_change = 0.0
    excess_coeficient = 1.0
    disjoint_coeficient = 1.0
    weight_coeficient = 0.4
    
    # species
    species_size = 20
    survival_threshold = 0.1 # only the best 20% for each species is allowed to mate
    old_threshold = 80
    youth_threshold = 10
    old_penalty = 0.2    # always in (0,1)
    youth_boost = 1.7    # always in (1,2)
    max_stagnation = 15
    
    # for a future release
    #ele_event_time = 1000
    #ele_events = False            
                