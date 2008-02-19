from config import Config
import chromosomes
import cPickle as pickle
import visualize
import random
#from psyco.classes import *

class SelecaoTorneio:
    """Sorteia dois individuos, retorna aquele com o maior fitness."""
    def __init__(self, pop):
        self._pop = pop
    def __call__(self):
        s1, s2 = random.choice(self._pop), random.choice(self._pop)
        if s1.fitness >= s2.fitness:
            return s1
        else:
            return s2
        
class SelecaoRank:
    """A probabilidade de selecao e proporcial ao ranking por fitness na populacao."""
    def __init__(self, pop):
        self._pop = pop
        self._total_fitness = 0
        rank = 1
        for i in self._pop:
            self._total_fitness += rank
            rank += 1
    def __call__(self):
        n = random.uniform(0, self._total_fitness)
        s = 0
        rank = 1
        for i in self._pop:
            s += rank
            if n <= s:
                break
            rank += 1
        return i

class Population:
    ''' Manages all the species  '''
    evaluate = None # Evaluates the entire population. You need to override 
                    # this method in your experiments    
    selecao = SelecaoRank

    def __init__(self):
        self.__popsize = Config.pop_size
               
        # Statistics
        self.__avg_fitness = []
        self.__best_fitness = []
        
        self.__create_population()
        
    stats = property(lambda self: (self.__best_fitness, self.__avg_fitness))   
    
    def __create_population(self):
        self.__population = [chromosomes.FFSigmoidChromosome.create_fully_connected(Config.input_nodes, Config.output_nodes) \
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
                
    def average_fitness(self):
        ''' Returns the average raw fitness of population '''
        sum = 0.0
        for c in self:
            sum += c.fitness
            
        return sum/len(self)
    
    def epoch(self, n, stats=True, save_best=False):
        ''' Runs NEAT's genetic algorithm for n epochs. All the speciation methods are handled here '''
        
        for generation in xrange(n):
            if stats: print 'Running generation',generation
            
            # Evaluate individuals
            self.evaluate()                      
            # Current generation's best chromosome 
            self.__best_fitness.append(max(self.__population))
            # Current population's average fitness
            self.__avg_fitness.append(self.average_fitness()) 
            # Print some statistics
            best = self.__best_fitness[-1] 

            if save_best:
                file = open('best_chromo_'+str(generation),'w')
                pickle.dump(best, file)
                file.close()
                
            if stats:
                print 'Population\'s average fitness', self.__avg_fitness[-1]
                print 'Best fitness: %2.12s - size: %s - species %s - id %s' \
                    %(best.fitness, best.size(), best.species_id, best.id)
                
            # Stops the simulation
            if best.fitness > Config.max_fitness_threshold:
                print 'Best individual found in epoch %s - complexity: %s' %(generation, best.size())
                break            
                
            # -------------------------- Producing new offspring -------------------------- #
            offspring = []
            
            # new reproduction model
            # keeps the best (survival_threshold)%, replace the rest
            self.__population.sort()     # sort species's members by their fitness
            self.__population.reverse()  # best members first
            
            #print [c.fitness for c in self.__population]
                          
            kill = int(round(len(self)*Config.survival_threshold)) # keep a % of the best individuals
            #print "Killing %d individuals out of %d" % (len(self.__population) - kill, len(self.__population))
   
            if kill > 0: # If we're going to kill, then do it.
                self.__population = self.__population[:kill]
                assert len(self.__population) > 0 
                
            # selects two parents from the remaining population:
            selecionar = self.selecao(self)
            
            while (len(offspring) < Config.pop_size  - kill):
                #print "Creating new individual"
                #random.shuffle(self.__population) # remove shuffle (always select best: give better results?)
                #parent1, parent2 = self.__population[0], self.__population[1]
                
                parent1 = selecionar()
                parent2 = selecionar()
                
                child = parent1.crossover(parent2)
                offspring.append(child.mutate())
                

            #print "Population size %d - offspring size %d" %(len(self.__population), len(offspring))
            self.__population.extend(offspring)
            