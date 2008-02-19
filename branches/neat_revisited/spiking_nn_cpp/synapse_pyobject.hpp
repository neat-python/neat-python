#ifndef SYNAPSE_PYOBJECT_HPP
#define SYNAPSE_PYOBJECT_HPP

#include <Python.h>
#include "structmember.h"
#include "spiking_nn.hpp"
#include "neuron_pyobject.hpp"

// Constructors won't be automatically called.
// Always define __init__ method.
struct SynapseObject {
	PyObject_HEAD
    Synapse synapse;
	NeuronObject* source;
	NeuronObject* dest;
};

namespace {

int Synapse_init(SynapseObject *self, PyObject *args, PyObject *kwds) {
	PyObject* source = 0;
	PyObject* dest = 0;
	double weight;

    static char *kwlist[] = {"source", "dest", "weight", 0};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O!O!d", kwlist, 
    		&NeuronType, &source, &NeuronType, &dest, &weight)) {
        return -1;
    }
    Py_INCREF(source);
    self->source = reinterpret_cast<NeuronObject*>(source);
    Py_INCREF(dest);
    self->dest = reinterpret_cast<NeuronObject*>(dest);
    self->synapse = Synapse(&self->source->neuron, &self->dest->neuron, weight);
    return 0;
}

void Synapse_dealloc(SynapseObject* self)
{
    Py_XDECREF(self->source);
    Py_XDECREF(self->dest);
    self->ob_type->tp_free(reinterpret_cast<PyObject*>(self));
}

PyObject* Synapse_advance(SynapseObject* self) {
	self->synapse.advance();
	return Py_BuildValue("");
}

PyMethodDef Synapse_methods[] = {
    {"advance", reinterpret_cast<PyCFunction>(Synapse_advance), METH_NOARGS,
     "Advances time in 1 ms."
    },
    {0}
};

PyTypeObject SynapseType = {
		PyObject_HEAD_INIT(0)
		0,							/* ob_size */
		"spiking_nn.Synapse",		/* tp_name */
		sizeof(SynapseObject),		/* tp_basicsize */
		0,							/* tp_itemsize */
		reinterpret_cast<destructor>(Synapse_dealloc),	/* tp_dealloc */
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
		"A synapse indicates the connection strength between two neurons (or itself)",
		0,		               		/* tp_traverse */
		0,		               		/* tp_clear */
		0,		               		/* tp_richcompare */
		0,		               		/* tp_weaklistoffset */
		0,		               		/* tp_iter */
		0,		               		/* tp_iternext */
		Synapse_methods,			/* tp_methods */
		0,             				/* tp_members */
		0, 							/* tp_getset */
		0,                         /* tp_base */
		0,                         /* tp_dict */
		0,                         /* tp_descr_get */
		0,                         /* tp_descr_set */
		0,                         /* tp_dictoffset */
		reinterpret_cast<initproc>(Synapse_init),	/* tp_init */
};

}

#endif
