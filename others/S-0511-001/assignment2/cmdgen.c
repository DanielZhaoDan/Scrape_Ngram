/* * * * * * * * *
 * Utility program that generates random input and lookup commands for
 * the hash table interpreter program
 * 
 * usage:
 *   make cmdgen
 *   ./cmdgen ninserts nlookups > commandfilename
 *       ninserts: number of insert commands to generate
 *       nlookups: number of lookup commands to generate
 *       commandfilename: name of file to store commands in
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Shreyash Patodia and Matt Farrugia
 * 
 * modifications by ...
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "inthash.h"

/*************************************************************************/

void printusageexit(char *exe) {
	/* Print usage information: */
	fprintf(stderr, "usage: %s ninserts nlookups > commandfilename\n", exe);
	fprintf(stderr, " ninserts: number of insert commands to generate\n");
	fprintf(stderr, " nlookups: number of lookup commands to generate\n");
	fprintf(stderr, " commandfilename: name of file to store commands in\n");

	/* and exit, as promised :) */
	exit(1);
}

/*************************************************************************/

int main(int argc, char **argv) {
	int i;

	/* Get command line arguments. */
	if (argc < 3) {
		printusageexit(argv[0]);
	}
	int ninserts  = atoi(argv[1]);
	int nlookups = atoi(argv[2]);

	/* Seed the random number generator. */
	srand(time(NULL));

	/* Decide on some random numbers for insertion. */
	int max = 100 * ninserts + 1;
	int64 *inserts = malloc(sizeof (int64) * ninserts);
	for (i = 0; i < ninserts; i++) {
		inserts[i] = rand() % max;
	}

	/* Print insertion commands for these numbers. */
	for (i = 0; i < ninserts; i++) {
		printf("i %llu\n", inserts[i]);
	}


	/* Print lookup commands. Some will succeed, others will fail. */
	for (i = 0; i < nlookups; i++) {
		
		/* Flip a coin to decide whether to use an existing key or a new one. */
		int64 lookup;
		if (rand() % 2) {
			/* Use a random existing key */
			lookup = inserts[rand() % ninserts];
		
		} else {
			/* Generate a new random key */
			lookup = rand() % max;
		}
		printf("l %llu\n", lookup);
	}

	/* Finish with commands to print the table, print statistics, and quit. */

	printf("p\n");
	printf("s\n");
	printf("q\n"); 

	return 0;
}
