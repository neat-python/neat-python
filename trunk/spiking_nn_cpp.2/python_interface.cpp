#include <Python.h>
#include "structmember.h"

/*
 * A spiking neuron model based on:
 * 
 * Izhikevich, E. M.
 * Simple Model of Spiking Neurons
 * IEEE TRANSACTIONS ON NEURAL NETWORKS, VOL. 14, NO. 6, NOVEMBER 2003
 */
struct NeuronObject {
	PyObject_HEAD
	double a;
	double b;
	double c;
	double d;
	double v; // membrane potential
	double u; // membrane recovery variable
	bool has_fired;
	double bias;
	double current;
};

namespace {

const double DEFAULT_BIAS = 0;
const double DEFAULT_A = 0.02;
const double DEFAULT_B = 0.2;
const double DEFAULT_C = -65.0;
const double DEFAULT_D = 8.0;

/*
 * Initialization
 * 
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
int Neuron_init(NeuronObject *self, PyObject *args, PyObject *kwds) {
	double bias = DEFAULT_BIAS;
	double a = DEFAULT_A;
	double b = DEFAULT_B;
	double c = DEFAULT_C;
	double d = DEFAULT_D;

    static char *kwlist[] = {"bias", "a", "b", "c", "d", 0};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ddddd", kwlist, 
    		&bias, &a, &b, &c, &d)) {
        return -1;
    }
    self->a = a;
    self->b = b;
    self->c = c;
    self->d = d;
    self->v = c;
    self->u = b * self->v;
    self->has_fired = false;
    self->bias = bias;
    self->current = bias;
    return 0;
}

PyObject* Neuron_get_potential(NeuronObject *self, void *closure)
{
    return Py_BuildValue("f", self->v);
}

PyObject* Neuron_get_has_fired(NeuronObject* self, void* closure)
{
	if (self->has_fired) {
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
	return Py_BuildValue("f", self->v);
}

int Neuron_set_current(NeuronObject *self, PyObject *value, void *closure)
{
	if (!PyFloat_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "current must be a float");
		return -1;
	}
	double c = PyFloat_AS_DOUBLE(value);
	self->current = c;
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
	self->v += 0.5 * (0.04 * self->v * self->v + 5 * self->v + 140 - self->u + self->current);
	self->v += 0.5 * (0.04 * self->v * self->v + 5 * self->v + 140 - self->u + self->current);
	self->u += self->a * (self->b * self->v - self->u);
	if (self->v > 30) {
		self->has_fired = true;
		self->v = self->c;
		self->u += self->d;
	}
	else {
		self->has_fired = false;
		self->current = self->bias;
	}
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
	
	/* Init module */
	
	PyObject* module = Py_InitModule("spiking_nn_c", SpikingNNMethods);
	Py_INCREF(&NeuronType);
	PyModule_AddObject(module, "Neuron", reinterpret_cast<PyObject*>(&NeuronType));
}
