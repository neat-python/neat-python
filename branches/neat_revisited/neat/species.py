# -*- coding: UTF-8 -*-
from neat import *
import random, math
from config import Config
#from psyco.classes import *

class Species:
    """ A subpopulation containing similar individiduals """
    __id = 0 # global species id counter
    
    def __init__(self, first_individual, previous_id=None):
        """ A species requires at least one individual to come to existence """
        self.__id = self.__get_new_id(previous_id)              # species's id 
        self.__age = 0                                # species's age
        self.__subpopulation = []                   # species's individuals
        self.add(first_individual)
        self.hasBest = False                        # Does this species has the best individual of the population?
        self.spawn_amount = 0
        self.no_improvement_age = 0                 # the age species has shown no improvements on average
        self.__last_avg_fitness = 0     
        
        self.representant = first_individual
        
    #representative = property(lambda self: self.__subpopulation[0])
    members = property(lambda self: self.__subpopulation)
    age = property(lambda self: self.__age)
    id  = property(lambda self: self.__id)
      
    @classmethod
    def __get_new_id(cls, previous_id):
        if previous_id is None:
            cls.__id += 1
            return cls.__id
        else:
            return previous_id
        
    def add(self, individual):
        """ Add a new individual to the species """
        individual.species_id = self.__id        # set member's species id
        self.__subpopulation.append(individual)        
        
    def __iter__(self):
        return iter(self.__subpopulation)
        
    def __len__(self):
        """ Returns the total number of individuals in this species """
        return len(self.__subpopulation)
    
    def __repr__(self):
        return repr([c.fitness for c in self.__subpopulation])
    
    def average_fitness(self):
        """ Returns the raw average fitness for this species """
        sum = 0.0
        for c in self.__subpopulation:
            sum += c.fitness
                        
        try:
            avg_fitness = sum/len(self)
        except ZeroDivisionError:
            print "Species %d, with length %d is empty! Why? " % (self.__id, len(self))
        else:
            return avg_fitness
    
    def reproduce(self):
        """ Returns a list of 'spawn_amount' new individuals """
        
        offspring = [] # new offspring for this species        
        self.__age += 1  # increment species age
        
        #print "Reproducing species %d with %d members" %(self.id, len(self.__subpopulation))
        
        # controls species no improvement age
        avg = self.average_fitness()
        # if no_improvement_age > threshold, species will be removed
        if avg > self.__last_avg_fitness:
            self.__last_avg_fitness = avg
            self.no_improvement_age = 0
        else:
            self.no_improvement_age += 1 
        
        # this condition is useless since no species with spawn_amount < 0 will
        # reach this point - at least it shouldn't happen.
        if self.spawn_amount > 0:
            
            self.__subpopulation.sort()     # sort species's members by their fitness
            self.__subpopulation.reverse()  # best members first
            
            # keep the best               
            offspring.append(self.__subpopulation[0])
            self.spawn_amount -= 1
 
            survivors = int(round(len(self)*Config.survival_threshold)) # keep a % of the best individuals
   
            if survivors > 0:
                self.__subpopulation = self.__subpopulation[:survivors]
            else:
                # ensure that we have at least one individual 
                self.__subpopulation = self.__subpopulation[:1]                  
       
        while(self.spawn_amount > 0):         
        
            if len(self) > 1:
                
                # Selects two parents from the remaining species and produces a single individual 
                random.shuffle(self.__subpopulation) # remove shuffle (always select best: give better results?)
                parent1, parent2 = self.__subpopulation[0], self.__subpopulation[1]
                assert parent1.species_id == parent2.species_id
                child = parent1.crossover(parent2)
                offspring.append(child.mutate())
                    
                self.spawn_amount -= 1 
                
            else:                
                # mutate only
                parent1 = self.__subpopulation[0]
                # TODO: temporary hack - the child needs a new id (not the father's)
                child = parent1.crossover(parent1)
                offspring.append(child.mutate())
                
                self.spawn_amount -= 1

        # reset species (new members will be added again when speciating)
        self.__subpopulation = []
        
        # select a new random representant member
        self.representant = random.choice(offspring)

        return offspring
