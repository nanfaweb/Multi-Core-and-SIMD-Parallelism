CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -I..
LDFLAGS = -pthread

SRCS = main.cpp axpbySerial.cpp axpbyThread.cpp
OBJS = $(SRCS:.cpp=.o)
TARGET = axpby

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET) *.ppm
