# NEAT-Python: How It Works

NEAT-Python is a 2007 academic implementation of
**NeuroEvolution of Augmenting Topologies**.
It evolves both network structure (nodes and connections)
and parameters (weights, biases).
It is Python 2.7 only.

This document describes how the repository is organized,
how the classes relate, and how data moves from input to output.

---

## How it works

You do not train a fixed network with backpropagation.
You evolve a **population of chromosomes**.
Each chromosome is a genotype (node genes + connection genes with
innovation numbers).
That genotype is decoded into a phenotype (a runnable network).
You score each network with a fitness function you write.
The genetic algorithm then speciates, crosses over, and mutates
until fitness is high enough.

Four phenotype backends exist:

| Backend     | Model                                 | Typical use                         |
|-------------|---------------------------------------|-------------------------------------|
| `neat.nn`   | Discrete sigmoid / tanh               | Classification (XOR), control       |
| `neat.ctrnn`| Continuous-time RNN (Euler / RK4)     | Dynamical control, artificial life  |
| `neat.iznn` | Izhikevich spiking                    | Spike-based tasks                   |
| `neat.ifnn` | Integrate-and-fire                    | Simpler spiking                     |

Each has a pure-Python path and an optional C++ extension for speed.

---

## How you use it

The XOR example is the intended starting point:

1. Write an INI config (`xor2_config`) for phenotype, GA, compatibility, and species.
2. Load it with `config.load(...)`.
3. Set `chromosome.node_gene_type` (`NodeGene` or `CTNodeGene`).
4. Write `eval_fitness(population)`: for each chromosome, `create_phenotype` / `create_ffphenotype`, activate the net, assign `chromo.fitness`.
5. Hook it: `population.Population.evaluate = eval_fitness`.
6. Run `pop = Population(); pop.epoch(n)`.
7. Read the winner from `pop.stats`, visualize, or pickle it.

Shipped experiments:

- **XOR** — feedforward, parallel (Parallel Python), and spiking variants
- **Single-pole / double-pole balancing** — recurrent / CTRNN control
- **`run.py`** — repeat an experiment and average generations, nodes, connections, evaluations
- **`single_population.py`** — a simpler GA without speciation (rank / roulette / tournament)

You can also resume from gzipped checkpoints, save the best chromosome
each generation, and plot fitness, speciation, and network topology
(`visualize.py`).

---

## 1. Script-level diagram — Component (module) diagram

In UML this is a **component diagram**
(also called a **module** or **package diagram**).
Boxes are files/packages; arrows are imports / “uses”.

```mermaid
flowchart TB
    subgraph packaging["Packaging"]
        setup["setup.py<br/>builds C++ extensions"]
    end

    subgraph examples["examples/"]
        xor["xor/xor2.py<br/>xor2-spiking.py<br/>xor2_parallel.py"]
        run["xor/run.py"]
        pole["pole_balancing/<br/>single_pole, double_pole,<br/>single_pole_ctrnn"]
        cfg["*_config INI files"]
    end

    subgraph core["neat/ — evolution core"]
        config["config.py<br/>load() + Config"]
        genome["genome.py<br/>NodeGene, CTNodeGene,<br/>ConnectionGene"]
        chromo["chromosome.py<br/>Chromosome, FFChromosome"]
        species["species.py<br/>Species"]
        pop["population.py<br/>Population.epoch()"]
        single["single_population.py<br/>GA without speciation"]
        vis["visualize.py<br/>draw_net, plot_stats"]
    end

    subgraph pheno["Phenotype backends"]
        nn["nn/nn_pure.py + nn_cpp.py<br/>sigmoid Network"]
        ctrnn["ctrnn/ctrnn_pure.py + ctrnn_cpp.py<br/>CTNeuron / CTRNN"]
        iznn["iznn/<br/>Izhikevich spikes"]
        ifnn["ifnn/<br/>integrate-and-fire"]
    end

    xor --> config
    xor --> pop
    xor --> chromo
    xor --> genome
    xor --> vis
    xor --> nn
    xor --> iznn
    pole --> config
    pole --> pop
    pole --> chromo
    pole --> nn
    pole --> ctrnn
    run --> xor
    cfg --> config

    pop --> species
    pop --> chromo
    pop --> config
    single --> chromo
    single --> config
    chromo --> genome
    chromo --> config
    species --> config
    genome --> config

    nn --> chromo
    ctrnn --> nn
    ctrnn --> chromo
    iznn --> chromo
    ifnn --> iznn
    ifnn --> chromo

    vis --> chromo
    setup --> nn
    setup --> iznn
    setup --> ifnn
```

---

## 2. Class-level diagram — Class diagram

In UML this is a **class diagram**:
types, inheritance, and “has-a” relationships.

```mermaid
classDiagram
    class Config {
        +input_nodes
        +output_nodes
        +pop_size
        +prob_addnode
        +prob_addconn
        +compatibility_threshold
        +max_fitness_threshold
    }

    class NodeGene {
        +id
        +type
        +bias
        +response
        +activation_type
        +mutate()
        +get_child(other)
        +copy()
    }

    class CTNodeGene {
        +time_constant
        +mutate()
    }

    class ConnectionGene {
        +innodeid
        +outnodeid
        +weight
        +enabled
        +innov_number
        +mutate()
        +split(node_id)
        +get_child(cg)
    }

    class Chromosome {
        +fitness
        +species_id
        +node_genes
        +connection_genes
        +mutate()
        +crossover(other)
        +distance(other)
        +size()
        +create_fully_connected()
        +create_minimally_connected()
    }

    class FFChromosome {
        +node_order
        +_mutate_add_connection()
    }

    class Species {
        +id
        +age
        +representant
        +spawn_amount
        +add(individual)
        +reproduce()
        +TournamentSelection()
        +average_fitness()
    }

    class Population {
        +evaluate()*
        +epoch(n)
        +stats
        +species_log
    }

    class Neuron {
        +type
        +bias
        +response
        +activate()
    }

    class CTNeuron {
        +tau
        +activate()
    }

    class Synapse {
        +weight
        +incoming()
    }

    class Network {
        +sactivate(inputs)
        +pactivate(inputs)
        +flush()
    }

    class FeedForward {
        +__create_net()
    }

    class IzNeuron {
        +advance()
        +has_fired
    }

    class IFNeuron {
        +advance()
        +has_fired
    }

    class IzNetwork {
        +advance(inputs)
        +reset()
    }

    NodeGene <|-- CTNodeGene
    Chromosome <|-- FFChromosome
    Chromosome "1" *-- "many" NodeGene
    Chromosome "1" *-- "many" ConnectionGene
    Species "1" *-- "many" Chromosome : members
    Population "1" *-- "many" Species
    Population "1" *-- "many" Chromosome
    Neuron <|-- CTNeuron
    Network <|-- FeedForward
    Network "1" *-- "many" Neuron
    Network "1" *-- "many" Synapse
    Synapse --> Neuron : source / dest
    IzNetwork "1" *-- "many" IzNeuron
    Config <.. Chromosome
    Config <.. Population
    Config <.. Species
    Chromosome ..> Network : create_phenotype
    Chromosome ..> IzNetwork : create_phenotype
```

`Population.evaluate` is a hook you override.
`single_population.Population` is a separate class with the same name:
no species, plus `SelecaoTorneio` / `SelecaoRoleta` / `SelecaoRank`.

---

## 3. Main input → output flow — Activity diagram

This is an **activity diagram** (UML process flow).
If you only track data moving through stages,
the same picture is a **data-flow diagram (DFD)**.
If you emphasize object calls over time, it would be a **sequence diagram**.
Here the process is the important part.

```mermaid
flowchart TD
    A["INPUT<br/>config INI + your fitness function"] --> B["config.load()<br/>fills Config"]
    B --> C["Population.__init__<br/>create N chromosomes<br/>fully or minimally connected"]
    C --> D["Population.epoch(n)"]

    D --> E["For each generation"]
    E --> F["evaluate()<br/>you implement this"]
    F --> G["create_phenotype(chromo)<br/>genes → Neuron + Synapse"]
    G --> H["Activate network<br/>sactivate / pactivate / advance"]
    H --> I["Task I/O<br/>XOR pairs, cart-pole state, …"]
    I --> J["Assign chromo.fitness"]

    J --> K["Speciate<br/>distance vs representant"]
    K --> L{"best.fitness > threshold?"}
    L -->|yes| W["OUTPUT<br/>winner chromosome + stats"]
    L -->|no| M["Drop stagnant species"]
    M --> N["Compute spawn levels"]
    N --> O["Species.reproduce<br/>elitism → crossover → mutate"]
    O --> E

    W --> P["Optional<br/>visualize / pickle / checkpoint"]
    W --> Q["Winner phenotype<br/>activate on new inputs"]
    Q --> R["OUTPUT<br/>network answers"]
```

Inside one evaluation (the actual input → output of a network):

```mermaid
flowchart LR
    IN["Sensor inputs"] --> NG["INPUT NodeGenes"]
    NG --> CG["enabled ConnectionGenes<br/>weighted synapses"]
    CG --> HN["HIDDEN + OUTPUT neurons<br/>bias, response, activation"]
    HN --> OUT["Phenotype outputs"]
```

- Feedforward XOR uses `sactivate` (neurons in topological order).
- Control / recurrent / CTRNN uses `pactivate` (all neurons update together).
- Spiking nets use `advance` until a spike, timeout, or ambiguous answer.

---

## Diagram names

| What you asked for        | Standard name                                              | What it shows                                      |
|---------------------------|------------------------------------------------------------|----------------------------------------------------|
| Script level              | **Component diagram** (UML), also **module / package diagram** | Files and packages and how they depend on each other |
| Class level               | **Class diagram** (UML)                                    | Types, inheritance, composition                    |
| Input → output process    | **Activity diagram** (UML); same idea as a **data-flow diagram** | Steps from config + fitness to a winner network and its answers |

A **sequence diagram** would be the fourth common UML view:
objects calling each other over time
(`Population.epoch` → `evaluate` → `create_phenotype` → `sactivate` →
`Species.reproduce` → `crossover` / `mutate`).
The activity diagram above is the better match for
“process between input and output.”
