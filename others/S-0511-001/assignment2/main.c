/* * * * * * * * *
 * Main program:
 * reads command line options, runs a hash table interpreter
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Matt Farrugia <matt.farrugia@unimelb.edu.au>
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <getopt.h>

#include "inthash.h"
#include "hashtbl.h"

// command line options
#define DEFAULT_SIZE 4
typedef struct options {
	TableType type;
	int initial_size;
} Options;
Options get_options(int argc, char** argv);


// interpreter commands

#define INSERT 'i'
#define LOOKUP 'l'
#define PRINT  'p'
#define STATS  's'
#define HELP   'h'
#define QUIT   'q'
#define MAX_LINE_LEN 80
int get_command(char *operation, int64 *key);


// main program

void run_interpreter(HashTable *table);

int main(int argc, char **argv) {
	
	// get command line options (to determine table type, size, etc.)
	Options options = get_options(argc, argv);

	// create hashtable (of given type)
	HashTable *table = new_hash_table(options.type, options.initial_size);

	// start the interpreter loop
	run_interpreter(table);

	// done!
	free_hash_table(table);
	return 0;
}

// print out the valid operations
void print_operations() {
	printf(" %c number: insert 'number' into table\n",  INSERT);
	printf(" %c number: lookup is 'number' in table\n", LOOKUP);
	printf(" %c: print table\n", PRINT);
	printf(" %c: print stats\n", STATS);
	printf(" %c: quit\n", QUIT);
}

// run the interpreter, reading and performing commands until 'quit'
void run_interpreter(HashTable *table) {
	
	// print a prompt at the beginning
	printf("enter a command (h for help):\n");
	
	char op;
	int64 key;
	
	// then loop, getting and executing commands, until 'quit'
	while (true) {

		// read a command, storing results in op and key variables
		int argc = get_command(&op, &key);
		if (argc < 1) {
			continue; // no valid command entered, get another
		}

		// execute the command
		switch (op) {
			case INSERT:
				if (argc < 2) {
					// insert commands must have an argument
					printf("syntax: %c number\n", INSERT);
				
				} else {
					// perform the insertion
					if (hash_table_insert(table, key)) {
						printf("%llu inserted\n", key);
					} else {
						printf("%llu already in table\n", key);
					}
				}
				break;

			case LOOKUP:
				if (argc < 2) {
					// lookup commands must have an argument
					printf("syntax: %c number\n", LOOKUP);

				} else {
					// perform the lookup
					if (hash_table_lookup(table, key)) {
						printf("%llu found\n", key);
					} else {
						printf("%llu not found\n", key);
					}
				}
				break;

			case PRINT:
				// perform the print table
				hash_table_print(table);
				break;

			case STATS:
				// perform the print stats
				hash_table_stats(table);
				break;

			default:
				// display error
				printf("unknown operation '%c'\n", op);
				// fall through!
			case HELP:
				// list available options
				printf("available operations:\n");
				print_operations();
				break;
				
			case QUIT:
				// leave the interpreter loop
				printf("exiting\n");
				return;
		}
	}
}

// reads a line from stdin, parses it into an operation character and possibly
// a long long uinteger argument. store results in *operation and *key, resp.
//
// returns the number of tokens successfully read (e.g. 0 for none,
// 1 for operation only, 2 for both operation and integer)
int get_command(char *operation, int64 *key) {
	
	// read a line from stdin, up to MAX_LINE_LENGTH, into character buffer
	char line[MAX_LINE_LEN];
	fgets(line, MAX_LINE_LEN, stdin);
	line[strlen(line)-1] = '\0'; // strip trailing newline

	// attempt to parse the line string into *operation and *key
	int argc = sscanf(line, "%c %llu", operation, key);
	// note: since llu is unsigned, a command like 'i -1' will overflow,
	// resulting in *key = 18446744073709551615 (2^64-1). this is a feature.
	
	// return the number of variables successfully read, as required
	return argc;
}




// scans command line arguments for program options,
// prints usage info and exits if commands are missing or otherwise invalid
Options get_options(int argc, char** argv) {
	
	// create the Options structure with defaults
	Options options = { .type = NOTYPE, .initial_size = DEFAULT_SIZE };

	// use C's built-in getopt function to scan inputs by flag
	char option;
	while ((option = getopt(argc, argv, "t:s:")) != EOF){
		switch (option){
			case 't': // set hash table type
				options.type = strtotype(optarg);
				break;
			case 's': // set hash table size
				options.initial_size = atoi(optarg);
				break;
			default:
				break;
		}
	}

	// validation and printing error / usage messages
	bool valid = true;
		
	// check part validity
	if(options.type == NOTYPE){
		fprintf(stderr,
			"please specify which table type to use, using the -t flag:\n");
		fprintf(stderr, " -t linear:  linear hash table\n");
		fprintf(stderr, " -t xtndbl1: 1-key extendible hash table\n");
		fprintf(stderr, " -t 1 or cuckoo:  cuckoo hash table (part 1)\n");
		fprintf(stderr,
			" -t 2 or xtnbdln: n-key extendible hash table (part 2)\n");
		fprintf(stderr, " -t 3 or xuckoo:  extendible cuckoo table (part 3)\n");
		valid = false;
	}

	// validate table size
	if(options.initial_size <= 0) {
		fprintf(stderr,
			"please specify initial table size (>0) using the -s flag\n");
		valid = false;
	}

	// check overall validity before continuing
	if(!valid){
		exit(EXIT_FAILURE);
	}

	return options;
}
