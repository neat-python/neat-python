# -*- coding: UTF-8 -*-
import random, math
from genome import Chromosome
from config import Config

species_size = Config.species_size
compatibility_change = Config.compatibility_change
max_stagnation = Config.max_stagnation

class Species: # extend list?
    """ A subpopulation containing similar individiduals """
    id = 1 # species id
    
    def __init__(self, first_chromo):
        """ A species requires at least one individual to come to existence """
        self.id = Species.id                        # species's id 
        self.age = 0                                # species's age
        self.__chromosomes = [first_chromo]         # species's individuals
        self.representative = self.__chromosomes[0] # species's representative - random or first member?
        self.hasBest = False                        # Does this species has the best individual of the population?
        self.spawn_amount = 0
        self.no_improvement_age = 0                 # the age species has shown no improvements on average
        self.last_avg_fitness = 0        
        Species.id += 1
        
    def add(self, ind):
        """ Add a new individual to the species """
        self.__chromosomes.append(ind)
        
    def __iter__(self):
        return iter(self.__chromosomes)
        
    def __len__(self):
        """ Returns the total number of individuals in this species """
        return len(self.__chromosomes)
    
    def __repr__(self):
        return repr([c.fitness for c in self.__chromosomes])
    
    def best(self):
        """ Returns the best individual (the one with highest fitness) for this species """
        return max(self.__chromosomes)
    
    def average_fitness(self):
        """ Returns the raw average fitness for this species """
        sum = 0.0
        for c in self.__chromosomes:
            sum += c.fitness
            
        avg_fitness = sum/len(self.__chromosomes)
            
        # controls species' no improvement age
        # if no_improvement_age > threshold, remove it
        if avg_fitness > self.last_avg_fitness:
            self.last_avg_fitness = avg_fitness
            self.no_improvement_age = 0
        else:
            self.no_improvement_age += 1 
            
        return avg_fitness
    
    def reproduce(self):
        """ Returns a list of 'spawn_amount' new individuals """
        
        offspring = [] # new babies for this species        
        self.age += 1  # increment species's age
        
        if self.spawn_amount == 0:
            print 'Species %d (age %s) will be removed (produced no offspring)' %(self.id, self.age)
        
        if self.spawn_amount > 0:
            
            self.__chromosomes.sort()     # sort species's members by their fitness
            self.__chromosomes.reverse()  # best members first
 
            # couldn't come up with a better name! Ain't we killing them anyway?
            kill = int(len(self)*Config.survival_threshold) # keep a % of the best individuals - round() or not?       
            # if len(self) = 1, 2 or 3 -> kill = 0
            # if len(self) = 4 -> kill = 1 and so on...    
            if kill > 0: # if we're going to kill, then do it.
                self.__chromosomes = self.__chromosomes[:-kill] # is it pythonic? 
                
            # print 'Species %d with %d members - %d were killed' %(self.id, len(self), kill)
            
            offspring.append(self.best()) # copy best chromo
            # the best individual is in the first position, so we don't really need to use best()
        
        while(self.spawn_amount > 1):          
            
            # make sure our offspring will have the same parent's species_id number
            # this is going to help us when speciating again
            if(len(self) == 2):
                child = self.__chromosomes[1] # is it really copying or just referencing?
                offspring.append(child.mutate())
                
            if(len(self) > 2):
                # random.choice is a good choice! But we need to assert both parents are not the same 
                # parent_1 = random.choice(self.__chromosomes)
                # parent_2 = random.choice(self.__chromosomes)
                # Instead a shuffle solves the problem:
                
                # Selects two parents from the remaining species and produces a single individual 
                random.shuffle(self.__chromosomes)
                parent1, parent2 = self.__chromosomes[0], self.__chromosomes[1]
                child = parent1.crossover(parent2)                          
                offspring.append(child.mutate())
                
            self.spawn_amount -= 1
        
        self.__chromosomes = [] # reset species (new members will be added when speciating)
        return offspring
    
class TournamentSelection:
    ''' Tournament selection with k = 2 '''
    def __init__(self, pop):
        self._pop = pop
    def __call__(self):
        s1, s2 = random.choice(self._pop), random.choice(self._pop)
        if s1.fitness >= s2.fitness:
            return s1
        else:
            return s2
      
class Population:
    ''' Manages all the species  '''
    selection = TournamentSelection
    evaluate = None # Evaluates the entire population. You need to override 
                    # this method in your experiments
    
    def __init__(self, popsize):
        self.__popsize = popsize
        #self.__population = [Chromosome() for i in xrange(popsize)]
        self.__population = [Chromosome.create_fully_connected(Config.input_nodes, Config.output_nodes) \
                             for i in xrange(self.__popsize)]
        self.__bestchromo = max(self.__population)
        self.__species = []
        self.compatibility_threshold = Config.compatibility_threshold
    
    def __len__(self):
        return len(self.__population)
    
    def __iter__(self):
        return iter(self.__population)
        
    def __speciate(self):
        """ Group chromosomes into species by similarity """        
        for c in self:
            found = False
            # TODO: if c.species_id is not None try this species first                
            for s in self.__species:
                if c.distance(s.representative) < self.compatibility_threshold:
                    c.species_id = s.id # the species chromo belongs to
                    s.add(c)                
                    #print 'chromo %s added to species %s' %(chromo.id, s.id)
                    found = True
                    break # we found a compatible species, so let's skip to the next
                
            if not found: # create a new species for this lone chromosome
                self.__species.append(Species(c)) 
                c.species_id = self.__species[-1].id                
                print 'Creating new species %s and adding chromo %s' %(self.__species[-1].id, c.id)
                
            # TODO: requires some fixing!
            #if c.fitness == self.__bestchromo.fitness:
            #        self.__species[-1].hasBest = True
                    #print 'Specie %d has best individual %d' %(self.__species[-1].id, c.id)
        
        # controls compatibility threshold
        if len(self.__species) > species_size:
            self.compatibility_threshold += compatibility_change
        elif len(self.__species) < species_size:
            if self.compatibility_threshold > compatibility_change:
                self.compatibility_threshold -= compatibility_change
            else:
                print 'Compatibility threshold cannot be changed (minimum value has been reached)'
                
        # there are two bests: from the current pop and the overall            
                
    def average_fitness(self):
        ''' Returns the average raw fitness of population '''
        sum = 0.0
        for c in self:
            sum += c.fitness
            
        return sum/len(self)
    
    def __compute_spawn_levels(self):
        """ Compute each species' spawn amount (Stanley, p. 40) """
        
        # 1. boost if young and penalize if old (on raw fitness!)
        # 2. Share fitness (only usefull for computing spawn amounts)
        # 3. Compute spawn
        # More about it on: http://tech.groups.yahoo.com/group/neat/message/2203
        
        # the FAQ says that for fitness sharing to work all fitnesses must be > 0
        # I don't know why (yet!)
        
        # Sharing the fitness is only meaningful here  
        # we don't really have to change each individual's raw fitness 
        total_average = 0.0
        for s in self.__species:
                total_average += s.average_fitness()
      
        # average_fitness is being computed twice! optimize!        
        for s in self.__species:
            s.spawn_amount = int(round((s.average_fitness()*len(self)/total_average)))
            #assert(s.spawn_amount > 0) # at least one individual to spawn
                    
    def epoch(self, n):
        ''' Runs NEAT's genetic algorithm for n epochs. All the speciation methods are handled here '''
        
        for generation in xrange(n):
            print 'Running generation',generation
            
            # evaluate individuals
            self.evaluate()
            
            self.__speciate() # speciates the population
            
            self.__compute_spawn_levels() # compute spawn levels for each species            

            #print 'Best belongs to specie', self.__bestchromo.species_id
            
            # print some "debugging" information
            print 'Species length:', len(self.__species)
            print 'Species size:', [len(s) for s in self.__species]
            print 'Amount to spawn:',[s.spawn_amount for s in self.__species]
            print 'Species age:',[s.age for s in self.__species]
            print 'Species imp:',[s.no_improvement_age for s in self.__species] # species no improvement age
            
            new_population = [] # next generation's population
            
            # spawning new population
            for s in self.__species:
                if len(new_population) < len(self):
                    new_population += s.reproduce() # add a certain amount of individuals to the new pop
                    
            # remove species that won't spawn
            # what happens if the best chromo is in a non-spawning species?
            self.__species = [s for s in self.__species if s.spawn_amount > 0] 
            # remove stagnated species
            self.__species = [s for s in self.__species if \
                              s.no_improvement_age > max_stagnation and s.hasBest == False]
                    
                    
            # controls under or overflow
            fill = len(self) - len(new_population)
            if fill < 0: #overflow
                print 'Removing %d excess individual(s) from the new population' %-fill
                new_population = new_population[:fill] # remove at random or only the last members?
                
            if fill > 0: #underflow
                print 'Selecting %d more individual(s) to fill up the new population' %fill
                select = self.selection(self.__population)
                # apply tournament selection in the whole population (allow inter-species mating?)
                # or select a random species to reproduce?
                for i in range(fill):
                    parent1 = select()
                    parent2 = select() 
                    child = parent1.crossover(parent2)
                    new_population.append(child);
                    
            print 'Best: ', max(self.__population)
            #print 'Population average fitness', self.average_fitness()
                    
            # updates current population
            assert len(self) == len(new_population), 'Different population sizes!'
            self.__population = new_population
            # The new pop hasn't been evaluated at this point! Don't call average_fitness() !
        
if __name__ ==  '__main__' :
    
    # sample fitness function
    def eval_fitness(population):
        for chromosome in population:
            chromosome.fitness = 1.0
            
    # set fitness function 
    Population.evaluate = eval_fitness
    
    # creates the population
    pop = Population(150)
    # runs the simulation for 250 epochs
    pop.epoch(250)       

# Things left to check:
# a) I'm not tracking best member's species yet!
# b) boost and penalize is done inside Species.shareFitness() method (as in Buckland's code)
# c) Remove species that shows no improvements after some generations (except if it has the best individual of pop.)
# d) ELE (Extinct Life Events) - something to be implemented as described in NEAT4J version
# e) Do we really need a representative member for each species? 

# Algorithm:
# 1. Apply fitness sharing in each species
# 2. Compute spawn levels for each species (need to round up or down to an integer value)
# 3. Keep the best performing individual of each species (per species elitism) - if spawn amount >= 1
# 4. Reserve some % members of each species to produce next gen.
#    4.1 Parents are chosen randomly (uniform distribuition with replacement) - this is much like tournament selection with k = len(parents_chosen)
#    4.2 Create offspring based on species's spawn amount:
#        a) If the species has only one member we keep it to the next gen.
#        b) If the species has only one member besides the best we only apply mutation
#        c) Select two parents from the remaining individuals (make sure we do not select the same individuals to mate!)
#           Stanley does not apply tournament selection, but we could try!

# Questions: If a species spawn level is below < 1, what to do? Remove it?
#            When should a species be removed? Before fitness sharing?

# NEAT FAQ: http://www.cs.ucf.edu/~kstanley/neat.html#neatref
