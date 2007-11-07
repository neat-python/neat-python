#ifndef NETWORK_PYOBJECT_HPP
#define NETWORK_PYOBJECT_HPP

#include <Python.h>
#include "structmember.h"
#include "spiking_nn.hpp"

// Constructors won't be automatically called.
// Always define __init__ method.
struct NetworkObject {
	PyObject_HEAD
    Network network;
	PyObject* input;
	PyObject* output;
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
    if (neurons) {
    	for(Py_ssize_t i = 0; i < PyList_Size(neurons); i++) {
    	}
    }
    
    return 0;
}

}

#endif
