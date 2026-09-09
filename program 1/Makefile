CXX=g++
# FRACTAL_INTERLEAVE=0 → naive contiguous blocks; 1 → interleaved rows (default)
FRACTAL_INTERLEAVE ?= 1
CXXFLAGS=-O2 -std=c++11 -Wall -Wextra -pthread -DFRACTAL_INTERLEAVE=$(FRACTAL_INTERLEAVE)
APP=fractal
OBJDIR=objs

default: $(APP)

$(OBJDIR):
	mkdir -p $(OBJDIR)

$(APP): $(OBJDIR) $(OBJDIR)/main.o $(OBJDIR)/fractalSerial.o $(OBJDIR)/fractalThread.o
	$(CXX) $(CXXFLAGS) -o $@ $(OBJDIR)/main.o $(OBJDIR)/fractalSerial.o $(OBJDIR)/fractalThread.o

$(OBJDIR)/main.o: main.cpp CycleTimer.h
	$(CXX) $(CXXFLAGS) -c main.cpp -o $@

$(OBJDIR)/fractalSerial.o: fractalSerial.cpp
	$(CXX) $(CXXFLAGS) -c fractalSerial.cpp -o $@

$(OBJDIR)/fractalThread.o: fractalThread.cpp CycleTimer.h
	$(CXX) $(CXXFLAGS) -c fractalThread.cpp -o $@

naive:
	$(MAKE) clean
	$(MAKE) FRACTAL_INTERLEAVE=0

improved:
	$(MAKE) clean
	$(MAKE) FRACTAL_INTERLEAVE=1

clean:
	rm -rf $(OBJDIR) $(APP) *.ppm
