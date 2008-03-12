#include <Python.h>
#include "nn.hpp"

namespace {

PyMethodDef methods[] = {
		{"set_nn_activation",  set_nn_activation, METH_VARARGS, ""},
		{"sigmoid",  sigmoid, METH_VARARGS, "Sigmoidal type of activation function"},
		{0}
};

}

PyMODINIT_FUNC initnn_cpp(void)
{	
	PyObject* module = Py_InitModule("nn_cpp", methods);
}
