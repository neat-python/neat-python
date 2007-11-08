#ifndef SPIKING_NN_HPP
#define SPIKING_NN_HPP

#include <list>

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
	 * The following parameters produce some known spiking behaviors:
	 * 
	 * Regular spiking: a = 0.02, b = 0.2, c = -65.0, d = 8.0
	 * Intrinsically bursting: a = 0.02, b = 0.2, c = -55.0, d = 4.0
	 * Chattering: a = 0.02, b = 0.2, c = -50.0, d = 2.0
	 * Fast spiking: a = 0.1, b = 0.2, c = -65.0, d = 2.0
	 * Thalamo-cortical: a = 0.02, b = 0.25, c = -65.0, d = 0.05
	 * Resonator: a = 0.1, b = 0.25, c = -65.0, d = 2.0
	 * Low-threshold spiking: a = 0.02, b = 0.25, c = -65, d = 2.0
     */
	static const double DEFAULT_BIAS = 0;
	static const double DEFAULT_A = 0.02;
	static const double DEFAULT_B = 0.2;
	static const double DEFAULT_C = -65.0;
	static const double DEFAULT_D = 8.0;
	Neuron(double bias = DEFAULT_BIAS, double a = DEFAULT_A, double b = DEFAULT_B,
		double c = DEFAULT_C, double d = DEFAULT_D);
	// Advances time in 1 ms.
    void advance();
    // Membrane potential
    double get_potential() const { return __v; }
    // Indicates whether the neuron has fired
    bool has_fired() const { return __has_fired; }
    double get_current() const { return __current; }
    void set_current(double current) { __current = current; }
private:
	double __a;
	double __b;
	double __c;
	double __d;
	long double __v; // membrane potential
	long double __u; // membrane recovery variable
	bool __has_fired;
	double __bias;
	long double __current;
};

/*
 * A synapse indicates the connection strength between two neurons (or itself)
 */
class Synapse
{
public:
	Synapse(Neuron* source = 0, Neuron* dest = 0, double weight = 0)
		: __source(source), __dest(dest), __weight(weight) {}
	// Advances time in 1 ms.
    void advance();
private:
	Neuron* __source;
	Neuron* __dest;
	double __weight;
};

#endif
