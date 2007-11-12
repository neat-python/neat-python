# Temporary Makefile just for testing

CFLAGS = -Wall -O2 -fPIC -fno-strict-aliasing

all: spiking_nn_c.so
	
spiking_nn_c.so: python_interface.o spiking_nn.o
	g++ -shared python_interface.o spiking_nn.o -o spiking_nn_c.so
python_interface.o: python_interface.cpp spiking_nn.hpp neuron_pyobject.hpp synapse_pyobject.hpp
	g++ -c $(CFLAGS) -I/usr/include/python2.5 python_interface.cpp -o python_interface.o
spiking_nn.o: spiking_nn.cpp spiking_nn.hpp
	g++ -c $(CFLAGS) -I/usr/include/python2.5 spiking_nn.cpp -o spiking_nn.o
clean:
	rm *o
