GCC = g++
LD = $(GCC)

TARGET = build/test

SOURCES_LIB = $(wildcard src/*.cpp)
INLCUDE_LIB = include
OBJECTS_LIB = $(SOURCES_LIB:.cpp=.o)

SOURCES_TEST = $(wildcard test/*.cpp) $(SOURCES_LIB)
INLCUDE_TEST = test $(INLCUDE_LIB)
INLCUDE_TEST_ARG = $(foreach d, $(INLCUDE_TEST), -I$d)
OBJECTS_TEST = $(SOURCES_TEST:.cpp=.o)
all: CFLAGS = -c -std=c++11 -Wall -O3 $(INLCUDE_TEST_ARG)
print: CFLAGS = -c -std=c++11 -Wall -O3 $(INLCUDE_TEST_ARG) -D DOPRINT
LDFLAGS = -lstdc++


all: $(TARGET)
print: createDir $(TARGET)


%.o: %.cpp
	$(GCC) $(CFLAGS) $< -o $@

$(TARGET): $(OBJECTS_TEST)
	$(LD) -o $@ $^ $(LDFLAGS)

createDir:
	mkdir results

clean-all: clean
	-rm -r results/

clean:
	-rm $(TARGET) $(OBJECTS_TEST)

cl:
	-rm $(OBJECTS_TEST)
