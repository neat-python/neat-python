# -*- coding: UTF-8 -*-
from neat import *
import random, math
from config import Config
from genome_feedforward import *
#from psyco.classes import *

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
        self.representative = first_chromo          # species's representative (first added member)
        self.hasBest = False                        # Does this species has the best individual of the population?
        self.spawn_amount = 0
        self.no_improvement_age = 0                 # the age species has shown no improvements on average
        self.__last_avg_fitness = 0        
        Species.id += 1
        
    #representative = property(lambda self: self.__chromosomes[0])
    chromosomes = property(lambda self: self.__chromosomes)
        
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
    
    def boost(self):
        for c in self.__chromosomes:
            c.fitness *= Config.youth_boost
    
    def penalize(self):
         for c in self.__chromosomes:
            c.fitness /= Config.old_penalty
    
    def average_fitness(self):
        """ Returns the raw average fitness for this species """
        sum = 0.0
        for c in self.__chromosomes:
            sum += c.fitness
            
        avg_fitness = sum/len(self.__chromosomes)
            
        return avg_fitness
    
    def reproduce(self):
        """ Returns a list of 'spawn_amount' new individuals """
        
        offspring = [] # new babies for this species        
        self.age += 1  # increment species's age
        
        # controls species' no improvement age
        avg = self.average_fitness()
        # if no_improvement_age > threshold, species will be removed
        if avg > self.__last_avg_fitness:
            self.__last_avg_fitness = avg
            self.no_improvement_age = 0
        else:
            self.no_improvement_age += 1 
        
        if self.spawn_amount == 0:
            # TODO: remove useless condition
            print 'Species %d (age %s) will be removed (produced no offspring)' %(self.id, self.age)
        
        if self.spawn_amount > 0:
            # remove condition since we're always reproducing species with spawn_amount > 0
            
            self.__chromosomes.sort()     # sort species's members by their fitness
            self.__chromosomes.reverse()  # best members first
 
            # Couldn't come up with a better name! Ain't we killing them anyway?
            kill = int(round(len(self)*Config.survival_threshold)) # keep a % of the best individuals - round() or not?       
   
            if kill > 0: # If we're going to kill, then do it.
                self.__chromosomes = self.__chromosomes[:-kill]
                
            assert len(self.__chromosomes) > 0
                
            # print 'Species %d with %d members - %d were killed' %(self.id, len(self), kill)   
            
            offspring.append(self.__chromosomes[0]) # keep the best member
            self.representative = self.__chromosomes[0] # this is the same chromo from last gen.

            self.spawn_amount -= 1 # The best member will be kept for the next generation
                                   # so we have one less individual to spawn
               
        while(self.spawn_amount > 0):          
            
            # make sure our offspring will have the same parent's species_id number
            # this is going to help us when speciating again
            if(len(self) == 1):
                # temporary hack - the child needs a new id (not the father's)
                child = self.__chromosomes[0].crossover(self.__chromosomes[0])                
                offspring.append(child.mutate())
                
            if(len(self) > 1):
                # Selects two parents from the remaining species and produces a single individual 
                random.shuffle(self.__chromosomes)
                parent1, parent2 = self.__chromosomes[0], self.__chromosomes[1]
                child = parent1.crossover(parent2)                          
                offspring.append(child.mutate())
                
            self.spawn_amount -= 1 

        # reset species (new members will be added when speciating)
        self.__chromosomes = []  
        
        assert len(offspring) > 0

        return offspring
