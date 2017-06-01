/* * * * * * * * *
 * Dynamic hash table using linear probing to resolve collisions
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Matt Farrugia <matt.farrugia@unimelb.edu.au>
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "linear.h"

// how many cells to advance at a time while looking for a free slot
#define STEP_SIZE 1

// a hash table is an array of slots holding keys, along with a parallel array
// of boolean markers recording which slots are in use (true) or free (false)
// important because not-in-use slots might hold garbage data, as they may
// not have been initialised
struct linear_table {
	int64 *slots;	// array of slots holding keys
	bool  *inuse;	// is this slot in use or not?
	int size;		// the size of both of these arrays right now
	int load;		// number of keys in the table right now
};


/* * * *
 * helper functions
 */

// set up the internals of a linear hash table struct with new
// arrays of size 'size'
static void initialise_table(LinearHashTable *table, int size) {
	assert(size < MAX_TABLE_SIZE && "error: table has grown too large!");

	table->slots = malloc((sizeof *table->slots) * size);
	assert(table->slots);
	table->inuse = malloc((sizeof *table->inuse) * size);
	assert(table->inuse);
	int i;
	for (i = 0; i < size; i++) {
		table->inuse[i] = false;
	}

	table->size = size;
	table->load = 0;
}


// double the size of the internal table arrays and re-hash all
// keys in the old tables
static void double_table(LinearHashTable *table) {
	int64 *oldslots = table->slots;
	bool  *oldinuse = table->inuse;
	int oldsize = table->size;

	initialise_table(table, table->size * 2);

	int i;
	for (i = 0; i < oldsize; i++) {
		if (oldinuse[i] == true) {
			linear_hash_table_insert(table, oldslots[i]);
		}
	}

	free(oldslots);
	free(oldinuse);
}


/* * * *
 * all functions
 */

// initialise a linear probing hash table with initial size 'size'
LinearHashTable *new_linear_hash_table(int size) {
	LinearHashTable *table = malloc(sizeof *table);
	assert(table);

	// set up the internals of the table struct with arrays of size 'size'
	initialise_table(table, size);

	return table;
}


// free all memory associated with 'table'
void free_linear_hash_table(LinearHashTable *table) {
	assert(table != NULL);

	// free the table's arrays
	free(table->slots);
	free(table->inuse);

	// free the table struct itself
	free(table);
}


// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool linear_hash_table_insert(LinearHashTable *table, int64 key) {
	assert(table != NULL);

	// need to count our steps to make sure we recognise when the table is full
	int steps = 0;

	// calculate the initial address for this key
	int h = h1(key) % table->size;

	// step along the array until we find a free space (inuse[]==false),
	// or until we visit every cell
	while (table->inuse[h] && steps < table->size) {
		if (table->slots[h] == key) {
			// this key already exists in the table! no need to insert
			return false;
		}

		// else, keep stepping through the table looking for a free slot
		h = (h + STEP_SIZE) % table->size;
		steps++;
	}

	// if we used up all of our steps, then we're back where we started and the
	// table is full
	if (steps == table->size) {
		// let's make some more space and then try to insert this key again!
		double_table(table);
		return linear_hash_table_insert(table, key);

	} else {
		// otherwise, we have found a free slot! insert this key right here
		table->slots[h] = key;
		table->inuse[h] = true;
		table->load++;
		return true;
	}
}


// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool linear_hash_table_lookup(LinearHashTable *table, int64 key) {
	assert(table != NULL);

	// need to count our steps to make sure we recognise when the table is full
	int steps = 0;

	// calculate the initial address for this key
	int h = h1(key) % table->size;

	// step along until we find a free space (inuse[]==false), or until we
	// visit every cell
	while (table->inuse[h] && steps < table->size) {

		if (table->slots[h] == key) {
			// found the key!
			return true;
		}

		// keep stepping
		h = (h + STEP_SIZE) % table->size;
		steps++;
	}

	// we have either searched the whole table or come back to where we started
	// either way, the key is not in the hash table
	return false;
}


// print the contents of 'table' to stdout
void linear_hash_table_print(LinearHashTable *table) {
	assert(table != NULL);

	printf("--- table size: %d\n", table->size);

	// print header
	printf("   address | key\n");

	// print the rows of the hash table
	int i;
	for (i = 0; i < table->size; i++) {

		// print the address
		printf(" %9d | ", i);

		// print the contents of the slot
		if (table->inuse[i]) {
			printf("%llu\n", table->slots[i]);
		} else {
			printf("-\n");
		}
	}

	printf("--- end table ---\n");
}


// print some statistics about 'table' to stdout
void linear_hash_table_stats(LinearHashTable *table) {
	assert(table != NULL);
	printf("--- table stats ---\n");

	// print some information about the table
	printf("current size: %d slots\n", table->size);
	printf("current load: %d items\n", table->load);
	printf(" load factor: %.3f%%\n", table->load * 100.0 / table->size);
	printf("   step size: %d slots\n", STEP_SIZE);

	printf("--- end stats ---\n");
}
