CXX = g++
CXXFLAGS = -O2 -std=c++17 -Wall

all: altseries

altseries: main.cpp PDCvector.h
	$(CXX) $(CXXFLAGS) -o altseries main.cpp

clean:
	rm -f altseries
