# -*- coding: UTF-8 -*-
try:
    import matplotlib.pyplot as plt
    has_matplotlib = True
except ImportError:
    has_matplotlib = False

try:
    import pydot
    has_pydot = True
except ImportError:
    has_pydot = False

import random


def _write_dot(output, filename):
    if not has_pydot:
        print('You do not have the PyDot package.')
        return
    graphs = pydot.graph_from_dot_data(output)
    graph = graphs[0] if isinstance(graphs, list) else graphs
    graph.write(filename, prog='dot', format='svg')


def draw_net(chromosome, id=''):
    ''' Receives a chromosome and draws a neural network with arbitrary topology. '''
    output = 'digraph G {\n  node [shape=circle, fontsize=9, height=0.2, width=0.2]'

    # subgraph for inputs and outputs
    output += '\n  subgraph cluster_inputs { \n  node [style=filled, shape=box] \n    color=white'
    for ng in chromosome.node_genes:
        if ng.type == 'INPUT':
            output += '\n    ' + str(ng.id)
    output += '\n  }'

    output += '\n  subgraph cluster_outputs { \n    node [style=filled, color=lightblue] \n    color=white'
    for ng in chromosome.node_genes:
        if ng.type == 'OUTPUT':
            output += '\n    ' + str(ng.id)
    output += '\n  }'
    # topology
    for cg in chromosome.conn_genes:
        output += '\n  ' + str(cg.innodeid) + ' -> ' + str(cg.outnodeid)
        if cg.enabled is False:
            output += ' [style=dotted, color=cornflowerblue]'

    output += '\n }'

    _write_dot(output, 'phenotype' + id + '.svg')


def draw_ff(chromosome):
    ''' Draws a feedforward neural network '''

    output = 'digraph G {\n  node [shape=circle, fontsize=9, height=0.2, width=0.2]'

    # subgraph for inputs and outputs
    output += '\n  subgraph cluster_inputs { \n  node [style=filled, shape=box] \n    color=white'
    for ng in chromosome.node_genes:
        if ng.type == 'INPUT':
            output += '\n    ' + str(ng.id)
    output += '\n  }'

    output += '\n  subgraph cluster_outputs { \n    node [style=filled, color=lightblue] \n    color=white'
    for ng in chromosome.node_genes:
        if ng.type == 'OUTPUT':
            output += '\n    ' + str(ng.id)
    output += '\n  }'
    # topology
    for cg in chromosome.conn_genes:
        output += '\n  ' + str(cg.innodeid) + ' -> ' + str(cg.outnodeid)
        if cg.enabled is False:
            output += ' [style=dotted, color=cornflowerblue]'

    output += '\n }'

    _write_dot(output, 'feedforward.svg')


def plot_stats(stats):
    ''' Plots the population's average and best fitness. '''
    if not has_matplotlib:
        print('You do not have the matplotlib package.')
        return

    generation = list(range(len(stats[0])))
    fitness = [c.fitness for c in stats[0]]
    avg_pop = [avg for avg in stats[1]]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_title("Population's average and best fitness")
    ax.set_xlabel("Generations")
    ax.set_ylabel("Fitness")
    ax.plot(generation, fitness, color="red", label="best")
    ax.plot(generation, avg_pop, color="blue", label="average")
    ax.legend()
    fig.savefig('avg_fitness.svg')
    plt.close(fig)


def plot_spikes(spikes):
    ''' Plots the trains for a single spiking neuron. '''
    if not has_matplotlib:
        print('You do not have the matplotlib package.')
        return

    time = list(range(len(spikes)))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_title("Izhikevich's spiking neuron model")
    ax.set_ylabel("Membrane Potential")
    ax.set_xlabel("Time (in ms)")
    ax.plot(time, spikes, color="green")
    fig.savefig('spiking_neuron.svg')
    plt.close(fig)


def plot_species(species_log):
    ''' Visualizes speciation throughout evolution. '''
    if not has_matplotlib:
        print('You do not have the matplotlib package.')
        return

    generation = list(range(len(species_log)))
    species = []
    curves = []

    for gen in range(len(generation)):
        for j in range(len(species_log), 0, -1):
            try:
                species.append(species_log[-j][gen] + sum(species_log[-j][:gen]))
            except IndexError:
                species.append(sum(species_log[-j][:gen]))
        curves.append(species)
        species = []

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title("Speciation")
    ax.set_ylabel("Size per Species")
    ax.set_xlabel("Generations")

    colors = [plt.cm.tab20(random.random()) for _ in curves]
    baseline = [0] * len(generation)
    ax.fill_between(generation, baseline, curves[0], color=colors[0])
    for i in range(1, len(curves)):
        ax.fill_between(generation, curves[i - 1], curves[i], color=colors[i])

    fig.savefig('speciation.svg')
    plt.close(fig)
