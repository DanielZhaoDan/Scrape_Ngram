/* * * * * * * * *
 * Dynamic hash table using cuckoo hashing, resolving collisions by switching
 * keys between two tables with two separate hash functions
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by ...
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "cuckoo.h"

#define MAX_LOOP_DEPTH 100
#define INNER_TABLE_SIZE 2

// an inner table represents one of the two internal tables for a cuckoo
// hash table. it stores two parallel arrays: 'slots' for storing keys and
// 'inuse' for marking which entries are occupied
typedef struct inner_table {
	int64 *slots;	// array of slots holding keys
	bool  *inuse;	// is this slot in use or not?
} InnerTable;

// a cuckoo hash table stores its keys in two inner tables
struct cuckoo_table {
	InnerTable *innerTable[INNER_TABLE_SIZE]; // inner tables
	int size;			// size of each table
	int load;
	int64 *failedInsertKeys;
	int failedSize;
};

int h1_for_cuckoo_hash(int size, int key) {
	return h1(key) % size;
}

int h2_for_cuckoo_hash(int size, int key) {
	return h2(key) % size;
}

// initialise a cuckoo hash table with 'size' slots in each table
CuckooHashTable *new_cuckoo_hash_table(int size) {
	assert(size < MAX_TABLE_SIZE && "error: table has grown too large!");
	CuckooHashTable *newCuckooHashTable = malloc(sizeof *newCuckooHashTable);
	assert(newCuckooHashTable);

	// initialise structure table1 and its inner arrays with 'size'
	int i=0;
	for (i=0; i<INNER_TABLE_SIZE; i++) {
		newCuckooHashTable->innerTable[i] = malloc(sizeof *newCuckooHashTable->innerTable[i]);
		assert(newCuckooHashTable->innerTable[i]);
		newCuckooHashTable->innerTable[i]->slots = malloc((sizeof *newCuckooHashTable->innerTable[i]->slots) * size);
		assert(newCuckooHashTable->innerTable[i]->slots);
		newCuckooHashTable->innerTable[i]->inuse = malloc((sizeof *newCuckooHashTable->innerTable[i]->inuse) * size);
		assert(newCuckooHashTable->innerTable[i]->inuse);
	}

	newCuckooHashTable->failedInsertKeys = malloc((sizeof *newCuckooHashTable->failedInsertKeys) * size);

	newCuckooHashTable->size = size;
	newCuckooHashTable->load = 0;
	newCuckooHashTable->failedSize = 0;
	return newCuckooHashTable;
}


// free all memory associated with 'table'
void free_cuckoo_hash_table(CuckooHashTable *table) {
	assert(table != NULL);

	//free tables' inner arrays and then free the two tables
	int i=0;
	for (i=0; i<INNER_TABLE_SIZE; i++) {
		free(table->innerTable[i]->slots);
		free(table->innerTable[i]->inuse);
		free(table->innerTable[i]);
	}
	// free cuckoo hash table finally
	free(table);
}


bool do_cuckoo_hash_table_insert(CuckooHashTable *table, int innerTableIndex, int64 key, int depth) {
	if (depth >= MAX_LOOP_DEPTH) {
		return false;
	}
	int hashedKey = 0;
	if (innerTableIndex == 0){
		hashedKey = h1_for_cuckoo_hash(table->size, key);
	} else {
		hashedKey = h2_for_cuckoo_hash(table->size, key);
	}
	/*
	if can successfully insert, then insert it
	else get existed key and put new key here; And then reinsert the existed key
	*/
	if (!table->innerTable[innerTableIndex]->inuse[hashedKey]) {
		table->innerTable[innerTableIndex]->slots[hashedKey] = key;
		table->innerTable[innerTableIndex]->inuse[hashedKey] = true;
		return true;
	} else {
		int64 old_key = table->innerTable[innerTableIndex]->slots[hashedKey];
		table->innerTable[innerTableIndex]->slots[hashedKey] = key;
		return do_cuckoo_hash_table_insert(table, (innerTableIndex+1)%INNER_TABLE_SIZE, old_key, depth+1);
	}
	return false;
}


// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool cuckoo_hash_table_insert(CuckooHashTable *table, int64 key) {
	assert(table != NULL);
	// check if key has been added
	if (cuckoo_hash_table_lookup(table, key))
		return false;

	// start insert by trying innerTable[0]
	bool insertResult = do_cuckoo_hash_table_insert(table, 0, key, 1);

	//update load
	if (insertResult) {
		table->load++;
	} else {
		table->failedInsertKeys[table->failedSize] = key;
		table->failedSize++;
	}
	return insertResult;
}


// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool cuckoo_hash_table_lookup(CuckooHashTable *table, int64 key) {
	assert(table != NULL);
	int key1 = h1_for_cuckoo_hash(table->size, key);
	int key2 = h2_for_cuckoo_hash(table->size, key);
	return (table->innerTable[0]->slots[key1] == key) || (table->innerTable[1]->slots[key2] == key);
	return false;
}


// print the contents of 'table' to stdout
void cuckoo_hash_table_print(CuckooHashTable *table) {
	assert(table);
	printf("--- table size: %d\n", table->size);

	// print header
	printf("                    table one         table two\n");
	printf("                  key | address     address | key\n");

	// print rows of each table
	int i;
	for (i = 0; i < table->size; i++) {

		// table 1 key
		if (table->innerTable[0]->inuse[i]) {
			printf(" %20llu ", table->innerTable[0]->slots[i]);
		} else {
			printf(" %20s ", "-");
		}

		// addresses
		printf("| %-9d %9d |", i, i);

		// table 2 key
		if (table->innerTable[1]->inuse[i]) {
			printf(" %llu\n", table->innerTable[1]->slots[i]);
		} else {
			printf(" %s\n",  "-");
		}
	}
	// done!
	printf("--- end table ---\n");
}


// print some statistics about 'table' to stdout
void cuckoo_hash_table_stats(CuckooHashTable *table) {
	assert(table != NULL);
	printf("--- table stats ---\n");

	// print some information about the table
	printf("current size: %d slots\n", 2*table->size);
	printf("current load: %d items\n", table->load);
	printf("load factor: %.3f%%\n", table->load * 100.0 / 2 / table->size);
	printf("Failed to insert: %d\n", table->failedSize);
	printf("\n--- end stats ---\n");
}
