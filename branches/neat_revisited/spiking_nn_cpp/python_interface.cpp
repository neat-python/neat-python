/*
 * Spiking Neural Networks
 * C++ Python module to be used with NEAT
 */

#include <Python.h>
#include "neuron_pyobject.hpp"
#include "synapse_pyobject.hpp"

namespace {

PyMethodDef SpikingNNMethods[] = {
		{0}
};

}

PyMODINIT_FUNC initspiking_nn_c(void)
{	
	/* Neuron */
	
	NeuronType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&NeuronType) < 0)
		return;
	
	/* Synapse */
		
	SynapseType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&SynapseType) < 0)
		return;
	
	/* Init module */
	
	PyObject* module = Py_InitModule("spiking_nn_c", SpikingNNMethods);
	Py_INCREF(&NeuronType);
	PyModule_AddObject(module, "Neuron", reinterpret_cast<PyObject*>(&NeuronType));
	Py_INCREF(&SynapseType);
	PyModule_AddObject(module, "Synapse", reinterpret_cast<PyObject*>(&SynapseType));
}
