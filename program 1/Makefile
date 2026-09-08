CXX=g++
CXXFLAGS=-O2 -std=c++11 -Wall -Wextra -pthread
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

clean:
	rm -rf $(OBJDIR) $(APP) *.ppm
