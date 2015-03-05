GCC = g++
LD = $(GCC)

TARGET = test

SOURCES_TEST = $(wildcard *.cpp)
INLCUDE_TEST = ./
INLCUDE_TEST_ARG = $(foreach d, $(INLCUDE_TEST), -I$d)
OBJECTS_TEST = $(SOURCES_TEST:.cpp=.o)
all: CFLAGS = -c -std=c++11 -Wall -O3 $(INLCUDE_TEST_ARG)
print: CFLAGS = -c -std=c++11 -Wall -O3 $(INLCUDE_TEST_ARG) -D DOPRINT
LDFLAGS = -lstdc++


all: $(TARGET)
print: $(TARGET)


%.o: %.cpp
	$(GCC) $(CFLAGS) $< -o $@

$(TARGET): $(OBJECTS_TEST)
	$(LD) -o $@ $^ $(LDFLAGS)


clean-all: clean
	-rm dijkstra*.txt
	-rm bf*.txt
	-rm fw.txt

clean:
	-rm $(TARGET) $(OBJECTS_TEST)

cl:
	-rm $(OBJECTS_TEST)
