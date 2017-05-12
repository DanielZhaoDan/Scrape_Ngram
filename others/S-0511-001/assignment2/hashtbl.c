/* * * * * * * * *
 * Interface for using various hash table data structures through a
 * single unified list of functions
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Matt Farrugia <matt.farrugia@unimelb.edu.au>
 */

#include <string.h>
#include <stdlib.h>
#include <assert.h>

#include "hashtbl.h"

#include "tables/linear.h"	// provided
#include "tables/xtndbl1.h"	// provided
#include "tables/cuckoo.h"	// create for part 1
#include "tables/xtndbln.h" // create for part 2
#include "tables/xuckoo.h"	// create for part 3

// converts from a string representation to a TableType constant:
// "linear"			->	LINEAR
// "xtndbl1"		->	XTNDBL1
// "1" or "cuckoo"	->	CUCKOO
// "2" or "xtndbln"	->	XTNDBLN
// "3" or "xuckoo"	->	XUCKOO
TableType strtotype(char *str) {
	if (strcmp("linear",  str) == 0) {
		return LINEAR;
	}
	if (strcmp("xtndbl1", str) == 0) {
		return XTNDBL1;
	}
	if (strcmp("1", str) == 0 || strcmp("cuckoo",  str) == 0) {
		return CUCKOO;
	}
	if (strcmp("2", str) == 0 || strcmp("xtndbln", str) == 0) {
		return XTNDBLN;
	}
	if (strcmp("3", str) == 0 || strcmp("xuckoo",  str) == 0) {
		return XUCKOO;
	}
	return NOTYPE;
}

// a HashTable is a wrapper for an actual table structure of some type,
// and it also remembers is own type
struct table {
	TableType type;	// what type of hash table is this?
	void *table;	// the hash table itself
};

// initialise a hash table of type 'type' with initial size 'size',
// and return its pointer
HashTable *new_hash_table(TableType type, int size) {
	
	// allocate space for the table wrapper
	HashTable *table = malloc(sizeof *table);
	assert(table);

	// store the table type, so we know which functions to call later
	table->type = type;

	// create and store the table itself
	switch (type) {
		case LINEAR:
			table->table = new_linear_hash_table(size);
			break;
		case XTNDBL1:
			table->table = new_xtndbl1_hash_table();
			break;
		case CUCKOO:
			table->table = new_cuckoo_hash_table(size);
			break;
		case XTNDBLN:
			table->table = new_xtndbln_hash_table(size);
			break;
		case XUCKOO:
			table->table = new_xuckoo_hash_table();
			break;
		default:
			// no such table type? error. release memory and return NULL
			free(table);
			return NULL;
	}

	return table;
}

// free all memory associated with 'table'
void free_hash_table(HashTable *table) {
	assert(table != NULL);

	// free the actual table, using the relevant free function for its type
	switch (table->type) {
		case LINEAR:
			free_linear_hash_table(table->table);
			break;
		case XTNDBL1:
			free_xtndbl1_hash_table(table->table);
			break;
		case CUCKOO:
			free_cuckoo_hash_table(table->table);
			break;
		case XTNDBLN:
			free_xtndbln_hash_table(table->table);
			break;
		case XUCKOO:
			free_xuckoo_hash_table(table->table);
			break;
		default:
			break;
	}

	// free the wrapper struct itself
	free(table);
}

// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool hash_table_insert(HashTable *table, int64 key) {
	assert(table != NULL);

	// forward the call onto the relevant insert function
	switch (table->type) {
		case LINEAR:
			return linear_hash_table_insert(table->table, key);
		case XTNDBL1:
			return xtndbl1_hash_table_insert(table->table, key);
		case CUCKOO:
			return cuckoo_hash_table_insert(table->table, key);
		case XTNDBLN:
			return xtndbln_hash_table_insert(table->table, key);
		case XUCKOO:
			return xuckoo_hash_table_insert(table->table, key);
		default:
			return false;
	}
}

// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool hash_table_lookup(HashTable *table, int64 key) {
	assert(table != NULL);

	// forward the call onto the relevant lookup function
	switch (table->type) {
		case LINEAR:
			return linear_hash_table_lookup(table->table, key);
		case XTNDBL1:
			return xtndbl1_hash_table_lookup(table->table, key);
		case CUCKOO:
			return cuckoo_hash_table_lookup(table->table, key);
		case XTNDBLN:
			return xtndbln_hash_table_lookup(table->table, key);
		case XUCKOO:
			return xuckoo_hash_table_lookup(table->table, key);
		default:
			return false;
	}
}

// print the contents of 'table' to stdout
void hash_table_print(HashTable *table) {
	assert(table != NULL);

	// call the relevant print function
	switch (table->type) {
		case LINEAR:
			linear_hash_table_print(table->table);
			break;
		case XTNDBL1:
			xtndbl1_hash_table_print(table->table);
			break;
		case CUCKOO:
			cuckoo_hash_table_print(table->table);
			break;
		case XTNDBLN:
			xtndbln_hash_table_print(table->table);
			break;
		case XUCKOO:
			xuckoo_hash_table_print(table->table);
			break;
		default:
			break;
	}
}

// print some statistics about 'table' to stdout
void hash_table_stats(HashTable *table) {
	assert(table != NULL);

	// call the relevant print stats function
	switch (table->type) {
		case LINEAR:
			linear_hash_table_stats(table->table);
			break;
		case XTNDBL1:
			xtndbl1_hash_table_stats(table->table);
			break;
		case CUCKOO:
			cuckoo_hash_table_stats(table->table);
			break;
		case XTNDBLN:
			xtndbln_hash_table_stats(table->table);
			break;
		case XUCKOO:
			xuckoo_hash_table_stats(table->table);
			break;
		default:
			break;
	}
}