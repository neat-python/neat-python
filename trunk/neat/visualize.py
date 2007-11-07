# Receives a chromosome and returns a graphical representation of its phenotype
# This is a draft solution
try:
    import pydot   # Requires PyDot: http://code.google.com/p/pydot/downloads/list
    import biggles # Requires biggles: http://biggles.sourceforge.net/
except ImportError:
    print "You do not have the required packages: PyDot and/or Biggles"
    
def draw_net(chromosome, id=''):
    ''' Draws a neural network with arbitrary topology. '''
    output = 'digraph G {\n  node [shape=circle, fontsize=9, height=0.2, width=0.2]'
    
    # subgraph for inputs and outputs
    output += '\n  subgraph cluster_inputs { \n  node [style=filled, shape=box] \n    color=white'    
    for ng in chromosome.node_genes:
        if ng.type== 'INPUT':
            output += '\n    '+str(ng.id)
    output += '\n  }'
        
    output += '\n  subgraph cluster_outputs { \n    node [style=filled, color=lightblue] \n    color=white'    
    for ng in chromosome.node_genes:        
        if ng.type== 'OUTPUT':
            output += '\n    '+str(ng.id)       
    output += '\n  }'
    # topology
    for cg in chromosome.conn_genes:
        output += '\n  '+str(cg.innodeid)+' -> '+str(cg.outnodeid)
        if cg.enabled is False:
            output += ' [style=dotted, color=cornflowerblue]'
        
    output += '\n }'
    
    g = pydot.graph_from_dot_data(output)
    g.write('phenotype'+id+'.svg', prog='dot', format='svg') 

def draw_ff(net):
    ''' Draws a feedforward neural network '''
    
    output = 'digraph G {\n  node [shape=circle, fontsize=9, height=0.2, width=0.2]'
    
    # subgraph for inputs and outputs
    output += '\n  subgraph cluster_inputs { \n  node [style=filled, shape=box] \n    color=white'    
    for neuron in net.neurons:
        if neuron.type== 'INPUT':
            output += '\n    '+str(neuron.id)
    output += '\n  }'
        
    output += '\n  subgraph cluster_outputs { \n    node [style=filled, color=lightblue] \n    color=white'    
    for neuron in net.neurons:        
        if neuron.type== 'OUTPUT':
            output += '\n    '+str(neuron.id)       
    output += '\n  }'
    # topology
    for synapse in net.synapses:
        output += '\n  '+str(synapse.source.id)+' -> '+str(synapse.dest.id)
                
    output += '\n }'
    
    g = pydot.graph_from_dot_data(output)
    g.write('feedforward.svg', prog='dot', format='svg') 
    
def plot_stats(stats): 
    ''' Plots the population's average and best fitness. '''
    generation = [i for i in xrange(len(stats[0]))]
    
    fitness = [c.fitness for c in stats[0]]
    avg_pop = [avg for avg in stats[1]]
    
    plot = biggles.FramedPlot()
    plot.title = "Population's average and best fitness"
    plot.xlabel = r"Fitness"
    plot.ylabel = r"Generations"

    plot.add(biggles.Curve(generation, fitness, color="red"))
    plot.add(biggles.Curve(generation, avg_pop, color="blue"))
         
    #plot.show() # X11
    plot.write_img(600, 300, 'avg_fitness.svg')
    # width and height doesn't seem to affect the output! 
    
def plot_spikes(spikes):
    ''' Plots the trains for a single spiking neuron. '''
    time = [i for i in xrange(len(spikes))]
    
    plot = biggles.FramedPlot()
    plot.title = "Izhikevich's spiking neuron model"
    plot.ylabel = r"Membrane Potential"
    plot.xlabel = r"Time (in ms)"
    
    plot.add(biggles.Curve(time, spikes, color="green"))
    plot.write_img(600, 300, 'spiking_neuron.svg')
    # width and height doesn't seem to affect the output! 