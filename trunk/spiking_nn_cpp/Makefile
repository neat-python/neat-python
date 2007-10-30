# Temporary Makefile just for testing

CFLAGS = -Wall -march=k8 -O2 -fPIC -fomit-frame-pointer -pipe -fno-strict-aliasing

all: spiking_nn.so
	
spiking_nn.so: spiking_nn.o neuron.o
	g++ -shared spiking_nn.o neuron.o -o spiking_nn.so
spiking_nn.o: spiking_nn.cpp neuron.hpp
	g++ -c $(CFLAGS) -I/usr/include/python2.5 spiking_nn.cpp -o spiking_nn.o
neuron.o: neuron.cpp neuron.hpp
	g++ -c $(CFLAGS) -I/usr/include/python2.5 neuron.cpp -o neuron.o
clean:
	rm *o
