#include "spiking_nn.hpp"

Neuron::Neuron(double bias, double a, double b,	double c, double d)
	: __a(a), __b(b), __c(c), __d(d), __v(c), __u(b * __v), __has_fired(false),
	__bias(bias), __current(__bias)
{
}

void Neuron::advance()
{
	__v += 0.5 * (0.04 * __v * __v + 5 * __v + 140 - __u + __current);
	__v += 0.5 * (0.04 * __v * __v + 5 * __v + 140 - __u + __current);
	__u += __a * (__b * __v - __u);
	if (__v > 30) {
            __has_fired = true;
            __v = __c;
            __u += __d;
	}
	else {
		__has_fired = false;
	}
	__current = __bias;
}

void Synapse::advance()
{
	 if (__source->has_fired()) {
		 __dest->set_current(__dest->get_current() + __weight); 
	 }
}
