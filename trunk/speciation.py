# -*- coding: UTF-8 -*-
import random, math
from genome import Chromosome

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
        self.spawn_amount = None
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
    
#    def shareFitness(self):
#        """ Share the fitness among individuals for this species """
#        for c in self.__chromosomes:
#            c.fitness = c.fitness/len(self)
#        # in Mat Buckland's code: (1) boost if young and penalize if old, (2) share fitness!
#        # the FAQ says that for fitness sharing to work all fitnesses must be > 0
            
    def best(self):
        """ Returns the best individual (the one with highest fitness) for this species """
        return max(self.__chromosomes)
    
    def keeBest(self):
        """ Remove all individuals except for the best """
        # it does nothing for the time being
        pass 
    
    def crossover(self):
        """ Selects two parents from the remaining species and produces a single individual """
        # NEAT uses a random selection method: pick up two different parents - we could use tournament selection...
        # apply crossover operator (this method must be overridden!)
        return Chromosome() # returning a dummy chromo
    
    def average_fitness(self):
        """ Returns the raw average fitness for this species """
        sum = 0.0
        for c in self.__chromosomes:
            sum += c.fitness
            
        return sum/len(self.__chromosomes)
    
    def reproduce(self):
        """ Returns a list of 'spawn_amount' new individuals """
        
        self.__chromosomes.sort()     # sort species's members by their fitness
        self.__chromosomes.reverse()  # best members first

        offspring = [] # new babies for this species
        
        self.age += 1 # increment species's age
        
        if self.spawn_amount == 0:
            print 'Species %d (age %s) will be removed (produced no offspring)' %(self.id, self.age)
            # mark this species to be removed
        
        if self.spawn_amount > 0: 
            # couldn't come up with a better name! Ain't we killing them anyway?
            kill = int(len(self)*0.3) # keep the best 30% individuals - round() or not?       
            # if len(self) = 1, 2 or 3 -> kill = 0
            # if len(self) = 4 -> kill = 1 and so on...    
            if kill > 0: # if we're going to kill, then do it.
                self.__chromosomes = self.__chromosomes[:-kill] # is it pythonic? 
                
            print 'Species %d with %d members - %d were killed' %(self.id,len(self.__chromosomes),kill)
            
            offspring.append(self.best()) # copy best chromo
            # the best individual is in the first position, so we don't really need to use best()
        
        while(self.spawn_amount-1 > 0):          
            
            # make sure our offspring will have the same parent's species_id number
            # this is going to help us when speciating again
            if(len(self) == 1):
                baby = self.__chromosomes[0] # is it really copying or just referencing?
                offspring.append(baby.mutate())
                
            if(len(self) > 1):
                baby = self.crossover() # where should this method be placed?                
                offspring.append(baby.mutate())
                
            self.spawn_amount -= 1
        
        return offspring
      
class Population:
    ''' Manages all the species  '''
    def __init__(self, popsize):
        self.__popsize = popsize
        self.__population = [Chromosome() for i in xrange(popsize)]
        self.__bestchromo = max(self.__population)
        self.__species = []
    
    def __len__(self):
        return len(self.__population)
    
    def __iter__(self):
        return iter(self.__population)
        
    def __speciate(self):
        """ Group chromosomes into species by similarity """
        
        for c in self:
            found = False
            for s in self.__species:
                if c.dist(s.representative):
                    c.species_id = s.id # the species chromo belongs to
                    s.add(c)                
                    #print 'chromo %s added to species %s' %(chromo.id, s.id)
                    found = True
                    break # we found a compatible species, so let's skip to the next
                
            if not found: # create a new species for this lone chromosome
                self.__species.append(Species(c)) 
                c.species_id = self.__species[-1].id
                print 'Creating new species %s and adding chromo %s' %(self.__species[-1].id, c.id)
                
    def average_fitness(self):
        ''' Returns the average raw fitness of population '''
        sum = 0.0
        for c in self:
            sum += c.fitness
            
        return sum/len(self)

    def __compute_spawn_levels(self):
        """ Compute each species' spawn amount (Stanley, p. 40) """
        
        # 1. boost if young and penalize if old (on raw fitness!)
        # 2. Share fitness
        # 3. Compute spawn
        # More about it on: http://tech.groups.yahoo.com/group/neat/message/2203
        
        # the FAQ says that for fitness sharing to work all fitnesses must be > 0
        # I don't know why (yet!)
        
        # Sharing the fitness is only meaningful here  
        # we don't have to change each individual's fitness 
        total_average = 0.0
        for s in self.__species:
                total_average += s.average_fitness()
      
        # average_fitness is being computed twice! optimize!        
        for s in self.__species:
            # is it the best way to round?
            s.spawn_amount = int(round((s.average_fitness()*len(self)/total_average)))
                    
    def epoch(self, n):
        ''' Runs NEAT's genetic algorithm for n epochs. All the speciation methods are handled here '''
        
        for generation in xrange(n):
            print 'Running generation',generation
            
            self.__speciate() # speciates the population
            self.__compute_spawn_levels() # compute spawn levels for each species
            
            # print some "debugging" information
            print 'Species length:', len(self.__species)
            print 'Species size:', [len(s) for s in self.__species]
            print 'Amount to spawn:',[s.spawn_amount for s in self.__species]
            print 'Species age:',[s.age for s in self.__species]
            
            # weird behavior - now fixed!
            # [26, 20, 5, 10, 7,  3, 25, 7, 7, 21, 14,  2,  2,  1]
            # [ 2,  2, 8,  5, 6, 16,  2, 7, 7,  2,  3, 24, 22, 44] 150
            # the last species which contains 1 individual will spawn 44 !
            
            new_population = [] # next generation's population
            
            # spawning new population
            for s in self.__species:
                if len(new_population) < len(self):
                    new_population += s.reproduce() # add a certain amount of individuals to the new pop
                    
            # an overflow will never occour!
            # if there was an underflow of new individuals we need to fill up new_population
            fill = len(self) - len(new_population)
            if fill > 0:
                print 'Selecting %d more individual(s) to fill up the new population' %fill
                # apply tournament selection in the whole population (allow inter-species mating?)
                # or select a random species to reproduce?
                for i in range(fill):
                    new_population.append(Chromosome()); # just a temporary hack!
                    
            # updates current population
            self.__population = new_population
        
if __name__ ==  '__main__' :
    
    pop = Population(300)
    pop.epoch(20)
    print pop.average_fitness()
        

# Things left to check:
# a) I'm not tracking best member's species yet!
# b) boost and penalize is done inside Species.shareFitness() method (as in Buckland's code)
# c) Remove species that shows no improvements after some generations (except if it has the best individual of pop.)

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
#           Stanley does not apply tournament selection, but we can test this!

# Questions: If a species spawn level is below < 1, what to do? Remove it?
#            When should a species be removed? Before fitness sharing?

# FAQ: http://www.cs.ucf.edu/~kstanley/neat.html#neatref
# A simple ideia to optimize speciation:
# "If you add a species hint to your individuals, speciation runs much faster. When a child is created, copy the species of the mother into the species_hint of the child. When it's time to place the child in a species, first try the species hint. If the child belongs there, then we're ready. If it doesn't test all species and pick the first species that's compatible. Since the speciating events are few and far between, each individual will be tested against 1 species instead of maybe 13-30 species. If the number of species is great, the saving can be great too." 
