#ifndef NETWORK_PYOBJECT_HPP
#define NETWORK_PYOBJECT_HPP

#include <Python.h>
#include "structmember.h"
#include "spiking_nn.hpp"
#include "neuron_pyobject.hpp"
#include <list>

// Constructors won't be automatically called.
// Always define __init__ method.
struct NetworkObject {
	PyObject_HEAD
    Network network;
	std::list<Network::iterator> inputs;
	std::list<Network::iterator> outputs;
};

namespace {

int Network_init(NetworkObject *self, PyObject *args, PyObject *kwds) {
	PyObject* neurons = 0;
	PyObject* input_neurons = 0;
	PyObject* output_neurons = 0;
	PyObject* synapses = 0;

    static char *kwlist[] = {"neurons", "input_neurons", "output_neurons",
    		"synapses", 0};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O!O!O!O!", kwlist, 
    		&PyList_Type, &neurons, &PyList_Type, &input_neurons, &PyList_Type,
    		&output_neurons, &PyList_Type, &synapses)) {
        return -1;
    }
    self->network = Network();
    self->inputs = std::list<Network::iterator>();
    self->outputs = std::list<Network::iterator>();
    if (neurons) {
    	for(Py_ssize_t i = 0; i < PyList_Size(neurons); i++) {
    		if (!PyObject_IsInstance(PyList_GetItem(neurons, i),
    				reinterpret_cast<PyObject*>(&NeuronType))) {
    			return -1;
    		}
    		NeuronObject* no = reinterpret_cast<NeuronObject*>(PyList_GetItem(neurons, i));
    		self->network.push_back(no->neuron);
    	}
    }
    
    return 0;
}

PyObject* Network_advance(NetworkObject* self, PyObject *args, PyObject *kwds) {
	static char *kwlist[] = {"inputs", 0};
	PyObject* inputs = 0;
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O!", kwlist, &PyList_Type, &inputs)) {
	        return 0;
	}
	
	for(Py_ssize_t i = 0; i < PyList_Size(inputs); i++) {
		
	}
	            self.__input_neurons[i].current += input
	        for s in self.__synapses:
	            s.advance()
	        for n in self.__neurons.values():
	            n.advance()
	        return [n.has_fired for n in self.__output_neurons]
	
}

}

#endif
