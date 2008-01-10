#ifndef NEURON_PYOBJECT_HPP
#define NEURON_PYOBJECT_HPP

#include <Python.h>
#include "structmember.h"
#include "spiking_nn.hpp"

// Constructors won't be automatically called.
// Always define __init__ method.
struct NeuronObject {
	PyObject_HEAD
    Neuron neuron;
};

namespace {

int Neuron_init(NeuronObject *self, PyObject *args, PyObject *kwds) {
	double bias = Neuron::DEFAULT_BIAS;
	double a = Neuron::DEFAULT_A;
	double b = Neuron::DEFAULT_B;
	double c = Neuron::DEFAULT_C;
	double d = Neuron::DEFAULT_D;

    static char *kwlist[] = {"bias", "a", "b", "c", "d", 0};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ddddd", kwlist, 
    		&bias, &a, &b, &c, &d)) {
        return -1;
    }
    self->neuron = Neuron(bias, a, b, c, d);
    return 0;
}

PyObject* Neuron_get_potential(NeuronObject *self, void *closure)
{
    return Py_BuildValue("d", self->neuron.get_potential());
}

PyObject* Neuron_get_has_fired(NeuronObject* self, void* closure)
{
	if (self->neuron.has_fired()) {
		Py_INCREF(Py_True);
		return Py_True;
	}
	else {
		Py_INCREF (Py_False);
		return Py_False;
	}
}

PyObject* Neuron_get_current(NeuronObject* self, void* closure)
{
	return Py_BuildValue("d", self->neuron.get_current());
}

int Neuron_set_current(NeuronObject *self, PyObject *value, void *closure)
{
	if (!PyFloat_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "current must be a float");
		return -1;
	}
	double c = PyFloat_AS_DOUBLE(value);
	self->neuron.set_current(c);
	return 0;
}


PyGetSetDef Neuron_getseters[] = {
		{"potential", reinterpret_cast<getter>(Neuron_get_potential), 0,
			"Membrane potential", 0},
		{"has_fired", reinterpret_cast<getter>(Neuron_get_has_fired), 0,
			"Indicates whether the neuron has fired", 0},
		{"current", reinterpret_cast<getter>(Neuron_get_current),
			reinterpret_cast<setter>(Neuron_set_current), "current", 0},
     	{0}
};

PyObject* Neuron_advance(NeuronObject* self) {
	self->neuron.advance();
	return Py_BuildValue("");
}

PyMethodDef Neuron_methods[] = {
    {"advance", reinterpret_cast<PyCFunction>(Neuron_advance), METH_NOARGS,
     "Advances time in 1 ms."
    },
    {0}
};

PyTypeObject NeuronType = {
		PyObject_HEAD_INIT(0)
		0,							/* ob_size */
		"spiking_nn.Neuron",		/* tp_name */
		sizeof(NeuronObject),		/* tp_basicsize */
		0,							/* tp_itemsize */
		0,							/* tp_dealloc */
		0,							/* tp_print */
		0,							/* tp_getattr */
		0,							/* tp_setattr */
		0,							/* tp_compare */
		0,							/* tp_repr */
		0,							/* tp_as_number */
		0,							/* tp_as_sequence */
		0,							/* tp_as_mapping */
		0,							/* tp_hash */
		0,							/* tp_call */
		0,							/* tp_str */
		0,							/* tp_getattro */
		0,							/* tp_setattro */
		0,							/* tp_as_buffer */
		Py_TPFLAGS_DEFAULT,			/* tp_flags */
		"A spiking neuron model based on:\n\n"
		"Izhikevich, E. M.\n"
		"Simple Model of Spiking Neurons\n"
		"IEEE TRANSACTIONS ON NEURAL NETWORKS, VOL. 14, NO. 6, NOVEMBER 2003",
		0,		               		/* tp_traverse */
		0,		               		/* tp_clear */
		0,		               		/* tp_richcompare */
		0,		               		/* tp_weaklistoffset */
		0,		               		/* tp_iter */
		0,		               		/* tp_iternext */
		Neuron_methods,				/* tp_methods */
		0,             				/* tp_members */
		Neuron_getseters,           /* tp_getset */
		0,                         /* tp_base */
		0,                         /* tp_dict */
		0,                         /* tp_descr_get */
		0,                         /* tp_descr_set */
		0,                         /* tp_dictoffset */
		reinterpret_cast<initproc>(Neuron_init),	/* tp_init */
};

}

#endif
