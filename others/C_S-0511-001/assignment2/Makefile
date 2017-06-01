# # # # # # #
# Makefile for assignment 2
#
# created 24 Apr 2017
# Matt Farrugia <matt.farrugia@unimelb.edu.au>
#

CC     = gcc
CFLAGS = -Wall -Wno-format -std=c99
EXE    = a2
OBJ    = main.o inthash.o hashtbl.o tables/linear.o tables/cuckoo.o \
		 tables/xtndbl1.o tables/xtndbln.o tables/xuckoo.o
#									add any new files here ^

# MAIN PROGRAM

$(EXE): $(OBJ)
	$(CC) $(CFLAGS) -o $(EXE) $(OBJ)

main.o: inthash.h hashtbl.h
hashtbl.o: inthash.h tables/linear.h tables/cuckoo.h tables/xtndbl1.h \
 tables/xtndbln.h tables/xuckoo.h
tables/linear.o: inthash.h
tables/cuckoo.o: inthash.h
tables/xtndbl1.o: inthash.h
tables/xtndbln.o: inthash.h
tables/xuckoo.o: inthash.h


# COMMAND GENERATOR TARGETS

cmdgen: cmdgen.o
	$(CC) $(CFLAGS) -o cmdgen cmdgen.o
cmdgen.o: inthash.h


# CLEANING TARGETS

clean:
	rm -f $(OBJ) cmdgen.o
clobber: clean
	rm -f $(EXE) 
cleanly: $(EXE) clean


# SUBMISSION TARGET

STUDENTNUM = STUDENT-NUMBER
SUBMISSION = Makefile report.pdf main.c hashtbl.c hashtbl.h inthash.c inthash.h\
	tables/linear.h  tables/linear.c  tables/cuckoo.h  tables/cuckoo.c  \
	tables/xtndbl1.h tables/xtndbl1.c tables/xtndbln.h tables/xtndbln.c \
	tables/xuckoo.h  tables/xuckoo.c
#				add any new files here ^

submission: $(SUBMISSION)
	tar -czvf $(STUDENTNUM).tar.gz $(SUBMISSION)
