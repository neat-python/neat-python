/*
 * Spiking Neural Networks
 * C++ Python module to be used with NEAT
 */

#include <Python.h>
#include "neuron.hpp"

typedef struct {
    PyObject_HEAD
    Neuron neuron;
} NeuronObject;

namespace {

PyMethodDef SpikingNNMethods[] = {
    {0}
};

PyTypeObject NeuronType = {
    PyObject_HEAD_INIT(0)
    0,
    "spiking_nn.Neuron",
    sizeof(NeuronObject),
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    Py_TPFLAGS_DEFAULT,
    "A spiking neuron model based on:\n\n"
    "Izhikevich, E. M.\n"
    "Simple Model of Spiking Neurons\n"
    "IEEE TRANSACTIONS ON NEURAL NETWORKS, VOL. 14, NO. 6, NOVEMBER 2003",
};

}

PyMODINIT_FUNC initspiking_nn(void)
{	
	/* Neuron */
	
	NeuronType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&NeuronType) < 0)
		return;
	
	/* Init module */
	
	PyObject* module = Py_InitModule("spiking_nn", SpikingNNMethods);
	Py_INCREF(&NeuronType);
	PyModule_AddObject(module, "Neuron", reinterpret_cast<PyObject*>(&NeuronType));
}
