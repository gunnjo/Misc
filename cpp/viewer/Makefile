# Makefile for Basler Pylon sample program
.PHONY			: all clean

# The program to build
NAMES			:= viewer

DEPS			:= 

# Build tools and flags
CXX				?= g++
LD				:= $(CXX)
CPPFLAGS		:= 
CXXFLAGS		:= -g -O3 #e.g., CXXFLAGS=-g -O0 for debugging
LDFLAGS			:= -Wl,-E
LIBS			:= -lopencv_core -lopencv_highgui \
					-lopencv_imgproc -lopencv_imgcodecs -lopencv_objdetect -lopencv_video -lopencv_videoio

# Rules for building
all				: $(NAMES)
	$(foreach name,$(NAMES),make $(name) NAME=$(name);)

$(NAME)			: $(NAME).o
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

$(NAME).o: $(NAME).cpp $(DEPS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<



clean			:
	$(RM) $(NAME).o $(NAME)
