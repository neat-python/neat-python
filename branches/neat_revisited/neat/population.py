from config import Config
import species
import chromosome
import cPickle as pickle
import visualize
import random, math
#from psyco.classes import *

class Population:
    ''' Manages all the species  '''
    evaluate = None # Evaluates the entire population. You need to override 
                    # this method in your experiments    

    def __init__(self):
        # total population size
        self.__popsize = Config.pop_size
        # currently living species
        self.__species = []
        # species history
        self.__species_log = []
                
        # Statistics
        self.__avg_fitness = []
        self.__best_fitness = []
        
        self.__create_population()
        
    stats = property(lambda self: (self.__best_fitness, self.__avg_fitness))   
    species_log = property(lambda self: self.__species_log)
    
    def __create_population(self):
        
        if Config.feedforward:
            genotypes = chromosome.FFChromosome.create_fully_connected
        else:
            genotypes = chromosome.Chromosome.create_fully_connected
            
        self.__population = [genotypes(Config.input_nodes, Config.output_nodes) \
                             for i in xrange(self.__popsize)]
                            
    def __len__(self):
        return len(self.__population)
      
    def __iter__(self):
        return iter(self.__population)

    def __getitem__(self, key):
        return self.__population[key]
    
    def remove(self, chromo):
        ''' Removes a chromosome from the population '''
        self.__population.remove(chromo)      
        
    def __speciate(self, report):
        """ Group chromosomes into species by similarity """ 
        # Speciate the population
        for individual in self:
            found = False    
            for s in self.__species:
                if individual.distance(s.representant) < Config.compatibility_threshold:    
                    s.add(individual)
                    found = True
                    break
                
            if not found: # create a new species for this lone chromosome
                self.__species.append(species.Species(individual)) 
                
        
        for s in self.__species:
            # this happens when no chromosomes are compatible with the species
            if len(s) == 0: 
                if report: print "Removing species %d for being empty" % s.id
                # remove empty species    
                self.__species.remove(s)
                
        self.__set_compatibility_threshold()  
                
    def __set_compatibility_threshold(self):
        ''' Controls compatibility threshold '''
        if len(self.__species) > Config.species_size:
            Config.compatibility_threshold += Config.compatibility_change
        elif len(self.__species) < Config.species_size:
            if Config.compatibility_threshold > Config.compatibility_change:
                Config.compatibility_threshold -= Config.compatibility_change
            else:
                print 'Compatibility threshold cannot be changed (minimum value has been reached)'
                
    def average_fitness(self):
        ''' Returns the average raw fitness of population '''
        sum = 0.0
        for c in self:
            sum += c.fitness
            
        return sum/len(self)
    
    def stdeviation(self):
        ''' Returns the population standard deviation '''
        # first compute the average
        u = self.average_fitness()
        error = 0.0
        # now compute the distance from average
        for c in self:
            error += (u - c.fitness)**2
        return math.sqrt(error/len(self))
    
    def TournamentSelection(self):
        ''' Tournament selection with k = 2 '''
        random.shuffle(self.__population)        
        p1, p2 = self.__population[0], self.__population[1]
        if p1.fitness >= p2.fitness:
            return p1
        else:
            return p2   
    
    def __compute_spawn_levels(self):
        """ Compute each species' spawn amount (Stanley, p. 40) """
        
        # 1. Boost if young and penalize if old
        # TODO: does it really increase the overall performance?
        species_stats = []
        for s in self.__species:
            if s.age < Config.youth_threshold:
                species_stats.append(s.average_fitness()*Config.youth_boost)
                # once in a while it happens:
                # TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'
            elif s.age > Config.old_threshold:
                species_stats.append(s.average_fitness()*Config.old_penalty)                       
            else:
                species_stats.append(s.average_fitness())

                
        # 2. Share fitness (only usefull for computing spawn amounts)       
        # More info: http://tech.groups.yahoo.com/group/neat/message/2203        
        # Sharing the fitness is only meaningful here  
        # we don't really have to change each individual's raw fitness 
        total_average = 0.0
        for s in species_stats:
                total_average += s
                
         # 3. Compute spawn
        for i, s in enumerate(self.__species):
            s.spawn_amount = int(round((species_stats[i]*self.__popsize/total_average)))
            if s.spawn_amount == 0:
                # This rarely happens
                print 'Species %d (age %s) will be removed (produced no offspring)' %(s.id, s.age)
                
    def __log_species(self):
        ''' Logging species data for visualizing speciation '''
        higher = max([s.id for s in self.__species])
        temp = []
        for i in xrange(1, higher+1):
            found_specie = False
            for s in self.__species:
                if i == s.id:
                    temp.append(len(s))
                    found_specie = True
                    break                            
            if not found_specie:                     
                temp.append(0)                            
        self.__species_log.append(temp)
                    
    def epoch(self, n, report=True, save_best=False):
        ''' Runs NEAT's genetic algorithm for n epochs '''
        
        for generation in xrange(n):
            if report: print '\n ****** Running generation %d ****** \n' %generation
            
            # Evaluate individuals
            self.evaluate()     
            
            # Speciates the population
            self.__speciate(report)       
            # Compute spawn levels for each remaining species
            self.__compute_spawn_levels()                   
            
                                    
            # Current generation's best chromosome 
            self.__best_fitness.append(max(self.__population))
            # Current population's average fitness
            self.__avg_fitness.append(self.average_fitness()) 
            # Logging speciation stats    
            self.__log_species()
            # Print some statistics
            best = self.__best_fitness[-1] 
            # Which species has the best chromosome?
            for s in self.__species:
                s.hasBest = False
                if best.species_id == s.id:
                    s.hasBest = True
          
            # saves the best chromo from current generation
            if save_best:
                file = open('best_chromo_'+str(generation),'w')
                pickle.dump(best, file)
                file.close()
                               
            # saves all phenotypes - debugging!
            #for chromosome in self.__population:
            #    visualize.draw_net(chromosome, str(generation)+'_'+str(chromosome.id))
            #    pass

            #-----------------------------------------   
            # Prints chromosome's parents id:  {dad_id, mon_id} -> child_id      
            #for chromosome in self.__population:  
            #    print '{%3d; %3d} -> %3d' %(chromosome.parent1_id, chromosome.parent2_id, chromosome.id)
            #-----------------------------------------
            if report:
                print 'Population\'s average fitness: %3.10f stdev: %3.10f' %(self.__avg_fitness[-1], self.stdeviation())
                print 'Best fitness: %2.12s - size: %s - species %s - id %s' \
                    %(best.fitness, best.size(), best.species_id, best.id)
                
#                # print some "debugging" information
#                print 'Species length: %d totalizing %d individuals' \
#                        %(len(self.__species), sum([len(s) for s in self.__species]))
#                print 'Species ID       : %s' % [s.id for s in self.__species]
#                print 'Each species size: %s' % [len(s) for s in self.__species]
#                print 'Amount to spawn  : %s' % [s.spawn_amount for s in self.__species]
#                print 'Species age      : %s' % [s.age for s in self.__species]
#                print 'Species no improv: %s' % [s.no_improvement_age for s in self.__species] # species no improvement age
            
                for s in self.__species:
                    print s
             
            #for c in self.__population:
            #    print "%3d    %2d    %4d - %4d   %1.5f" %(c.id,c.species_id,c.parent1_id, c.parent2_id,c.fitness)   
            # Stops the simulation
            if best.fitness > Config.max_fitness_threshold:
                print '\nBest individual found in epoch %s - complexity: %s' %(generation, best.size())
                break            
                
            # Removing species with spawn amount = 0
            self.__species = [s for s in self.__species if s.spawn_amount > 0]
            
            # -------------------------- Producing new offspring -------------------------- #
            new_population = [] # next generation's population
            
            # Spawning new population
            for s in self.__species:
                new_population.extend(s.reproduce())
                                        
#            # Controls under or overflow
#            # This is unnecessary since the population size is stable
#            # due to the computed spawn levels for each species. No
#            # performance gain is noticed whether we use it or not.
#
#            fill = (self.__popsize) - len(new_population)
#            if fill < 0: # overflow
#                print 'Removing %d excess individual(s) from the new population' %-fill
#                # This is dangerous! I can't remove a species' representative!
#                new_population = new_population[:fill] # Removing the last added members
#                
#            if fill > 0: # underflow
#                print 'Selecting %d more individual(s) to fill up the new population' %fill
#                # Apply tournament selection in the whole population
#                # or select a random species to reproduce?
#                for i in range(fill):
##                    parent1 = self.TournamentSelection() 
##                    parent2 = self.TournamentSelection()
##                    child = parent1.crossover(parent2)
##                    # child = max(self.__population) - only apply mutations (give better results?)
##                    new_population.append(child.mutate())                    
#
#                    # Selects a random chromosome from population                    
#                    parent1 = random.choice(self.__population)                    
#                    # Search for a mate within the same species
#                    found = False
#                    for c in self.__population:
#                        if c.species_id == parent1.species_id:
#                            child = parent1.crossover(c)
#                            new_population.append(child.mutate())
#                            found = True
#                            break
#                    # If found no mate, just mutate it.
#                    if not found:
#                        new_population.append(parent1.mutate())
#                    
#            # Updates current population
#            assert self.__popsize == len(new_population), 'Different population sizes!'
            self.__population = new_population[:]
                    
            # Remove stagnated species and its members (except if it has the best chromosome)
            #self.__species = [s for s in self.__species if \
            #                  s.no_improvement_age <= Config.max_stagnation or \
            #                  s.no_improvement_age > Config.max_stagnation and s.hasBest == True] 
            
            for s in self.__species:
                if s.no_improvement_age > Config.max_stagnation:
                    if s.hasBest == False:
                        if report: print "\n   Species %2d is stagnated: removing it" % s.id                        
                        # removing species
                        self.__species.remove(s)
                        # removing all the species' members
                        #TODO: can be optimized!
                        for c in self.__population:
                            if c.species_id == s.id:
                                self.remove(c)
                                
                 
            # Does it help in avoiding local minima?
            #for s in self.__species:
                #if s.no_improvement_age > 50:
                    #print 'Species %d is super-stagnated, removing it' %(s.id)
            
            ## Remove "super-stagnated" species (even if it has the best chromosome)
            #self.__species = [s for s in self.__species if \
                              #s.no_improvement_age < 50]

if __name__ ==  '__main__' :
    
    # sample fitness function
    def eval_fitness(population):
        for individual in population:
            individual.fitness = 1.0
            
    # set fitness function 
    Population.evaluate = eval_fitness
    
    # creates the population
    pop = Population(50)
    # runs the simulation for 250 epochs
    pop.epoch(250)       

# Things left to check:
# b) boost and penalize is done inside Species.shareFitness() method (as in Buckland's code)
# d) ELE (Extinct Life Events) - something to be implemented as described in the NEAT4J version 
