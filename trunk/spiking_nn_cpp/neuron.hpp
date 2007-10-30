#ifndef NEURON_HPP
#define NEURON_HPP

/*
 * A spiking neuron model based on:
 * 
 * Izhikevich, E. M.
 * Simple Model of Spiking Neurons
 * IEEE TRANSACTIONS ON NEURAL NETWORKS, VOL. 14, NO. 6, NOVEMBER 2003
 */

class Neuron {
public:
	/*
	 * a, b, c, d are the parameters of this model.
	 * a: the time scale of the recovery variable.
	 * b: the sensitivity of the recovery variable.
	 * c: the after-spike reset value of the membrane potential.
	 * d: after-spike reset of the recovery variable.
	 * 
	 * The following parameters produce some known spiking behavior:
	 * 
	 * Regular spiking: a = 0.02, b = 0.2, c = -65.0, d = 8.0
	 * Intrinsically bursting: a = 0.02, b = 0.2, c = -55.0, d = 4.0
	 * Chattering: a = 0.02, b = 0.2, c = -50.0, d = 2.0
	 * Fast spiking: a = 0.1, b = 0.2, c = -65.0, d = 2.0
	 * Thalamo-cortical: a = 0.02, b = 0.25, c = -65.0, d = 0.05
	 * Resonator: a = 0.1, b = 0.25, c = -65.0, d = 2.0
	 * Low-threshold spiking: a = 0.02, b = 0.25, c = -65, d = 2.0
     */
	Neuron(double bias = 0, double a = 0.02, double b = 0.2, double c = -65.0,
			double d = 8.0);
	// Advances time in 1 ms.
    void advance();
    // Membrane potential
    double get_potential();
    // Indicates whether the neuron has fired
    bool has_fired();
};

#endif
