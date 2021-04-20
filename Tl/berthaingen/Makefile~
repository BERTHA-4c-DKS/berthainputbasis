#!gmake
##################################################
#
# Makefile for berthaingen
#
# $Id$
#
###################################################

include ./config.mk

PROG_NAME1 = berthaingen
PROG_NAME2 = generatemin
PROG_NAME3 = mergeatdist
PROG_NAME3 = mergeatdist_dbl

OBJ1 = berthaingen.o \
      molecule.o \
      utility.o \
      ptable.o \
      writefiles.o

OBJ2 = generatemin.o \
      molecule.o \
      utility.o \
      ptable.o \
      writefiles.o

OBJ3 = mergeatdist.o \
      molecule.o \
      utility.o \
      ptable.o 

OBJ3 = mergeatdist_dbl.o \
      molecule.o \
      utility.o \
      ptable.o 


CFLAGS+= $(BASINC) 
LIB+= #-lboost_regex

all: $(PROG_NAME1) $(PROG_NAME2) $(PROG_NAME3) $(PROG_NAME4)

$(PROG_NAME1): $(OBJ1)
	$(CXX) -o $(@) $(OBJ1) $(LIB) 

$(PROG_NAME2): $(OBJ2)
	$(CXX) -o $(@) $(OBJ2) $(LIB) 

$(PROG_NAME3): $(OBJ3)
	$(CXX) -o $(@) $(OBJ3) $(LIB) 

$(PROG_NAME4): $(OBJ4)
	$(CXX) -o $(@) $(OBJ4) $(LIB) 

clean:
	rm -rf $(OBJ1) $(PROG_NAME1) $(OBJ2) $(PROG_NAME2) $(OBJ3) $(PROG_NAME3) $(OBJ4) $(PROG_NAME4)

mergeatdist_dbl.o: molecule.hpp utility.hpp ptable.hpp
mergeatdist.o: molecule.hpp utility.hpp ptable.hpp
generatemin.o: molecule.hpp utility.hpp ptable.hpp
berthaingen.o: molecule.hpp utility.hpp ptable.hpp
molecule.o: molecule.hpp utility.hpp ptable.hpp
utility.o: utility.hpp
ptables.o: ptable.hpp
