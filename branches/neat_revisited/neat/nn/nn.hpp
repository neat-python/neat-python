#ifndef NN_HPP
#define NN_HPP

#include <cmath>
#include <cstring>

namespace {

const char* nn_activation;

PyObject* set_nn_activation(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "s", &nn_activation))
        return 0;
    return Py_BuildValue("");
}

// Sigmoidal type of activation function
PyObject* sigmoid(PyObject *self, PyObject *args) {
	double x, response;
	if (!PyArg_ParseTuple(args, "dd", &x, &response)) {
		return 0;
	}
	if (std::strcmp(nn_activation, "exp") == 0) {
		return Py_BuildValue("d", 1.0 / (1.0 + std::exp(-x * response)));
	}
    else {
    	return Py_BuildValue("d", std::tanh(x * response));
    }
}

}

#endif