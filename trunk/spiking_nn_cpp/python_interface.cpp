/*
 * Spiking Neural Networks
 * C++ Python module to be used with NEAT
 */

#include <Python.h>
#include "neuron_pyobject.hpp"


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
