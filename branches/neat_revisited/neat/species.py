# -*- coding: UTF-8 -*-
from neat import *
import random, math
from config import Config
#from psyco.classes import *

class Species:
    """ A subpopulation containing similar individiduals """
    id = 1 # species id
    
    def __init__(self, first_chromo):
        """ A species requires at least one individual to come to existence """
        self.id = Species.id                        # species's id 
        self.age = 0                                # species's age
        self.__chromosomes = []                     # species's individuals
        self.add(first_chromo)
        self.representative = self.__chromosomes[0] # species's representative (first added member)
        self.hasBest = False                        # Does this species has the best individual of the population?
        self.spawn_amount = 0
        self.no_improvement_age = 0                 # the age species has shown no improvements on average
        self.__last_avg_fitness = 0        
        Species.id += 1
        
    #representative = property(lambda self: self.__chromosomes[0])
    chromosomes = property(lambda self: self.__chromosomes)
        
    def add(self, chromosome):
        """ Add a new individual to the species """
        chromosome.species_id = self.id        # set member's species id
        self.__chromosomes.append(chromosome)        
        
    def __iter__(self):
        return iter(self.__chromosomes)
        
    def __len__(self):
        """ Returns the total number of individuals in this species """
        return len(self.__chromosomes)
    
    def __repr__(self):
        return repr([c.fitness for c in self.__chromosomes])
    
    def average_fitness(self):
        """ Returns the raw average fitness for this species """
        sum = 0.0
        for c in self.__chromosomes:
            sum += c.fitness
                        
        try:
            avg_fitness = sum/len(self.__chromosomes)
        except ZeroDivisionError:
            print "Species %d, with rep. %d is empty! But why? It's in species %s" \
                    %(self.id, self.representative.id, self.representative.species_id)   
        else:
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
        
        if self.spawn_amount > 0:
            
            self.__chromosomes.sort()     # sort species's members by their fitness
            self.__chromosomes.reverse()  # best members first
 
            # Couldn't come up with a better name! Ain't we killing them anyway?
            kill = int(round(len(self)*Config.survival_threshold)) # keep a % of the best individuals
   
            if kill > 0: # If we're going to kill, then do it.
                self.__chromosomes = self.__chromosomes[:kill]
                assert len(self.__chromosomes) > 0 
            
            self.representative = self.__chromosomes[0] # this is the same chromo from last gen.
            offspring.append(self.__chromosomes[0])
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
                random.shuffle(self.__chromosomes) # remove shuffle (always select best: give better results?)
                parent1, parent2 = self.__chromosomes[0], self.__chromosomes[1]
                assert parent1.species_id == parent2.species_id
                child = parent1.crossover(parent2)
                offspring.append(child.mutate())
                
            self.spawn_amount -= 1 

        # reset species (new members will be added when speciating)
        self.__chromosomes = []  # keep the best, only returns the offspring

        return offspring
