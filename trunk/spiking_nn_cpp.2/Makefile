# Temporary Makefile just for testing

CFLAGS = -Wall -O2 -fPIC -fno-strict-aliasing

all: spiking_nn_c.so
	
spiking_nn_c.so: python_interface.o
	g++ -shared python_interface.o -o spiking_nn_c.so
python_interface.o: python_interface.cpp
	g++ -c $(CFLAGS) -I/usr/include/python2.5 python_interface.cpp -o python_interface.o
clean:
	rm *o
