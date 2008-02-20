# Temporary Makefile just for testing

CFLAGS = -Wall -O2 -fPIC -fno-strict-aliasing

all: iznn_cpp.so
	
iznn_cpp.so: iznn.o
	g++ -shared iznn_cpp.o -o iznn_cpp.so
iznn.o: iznn.cpp neuron.hpp synapse.hpp
	g++ -c $(CFLAGS) -I/usr/include/python2.5 iznn.cpp -o iznn_cpp.o
clean:
	rm *o
