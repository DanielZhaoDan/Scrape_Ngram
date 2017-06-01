/* * * * * * * * *
 * Dynamic hash table using cuckoo hashing, resolving collisions by switching
 * keys between two tables with two separate hash functions
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by ...
 */

#ifndef CUCKOO_H
#define CUCKOO_H

#include <stdbool.h>
#include "../inthash.h"

typedef struct cuckoo_table CuckooHashTable;

// initialise a cuckoo hash table with 'size' slots in each table
CuckooHashTable *new_cuckoo_hash_table(int size);

// free all memory associated with 'table'
void free_cuckoo_hash_table(CuckooHashTable *table);

// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool cuckoo_hash_table_insert(CuckooHashTable *table, int64 key);

// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool cuckoo_hash_table_lookup(CuckooHashTable *table, int64 key);

// print the contents of 'table' to stdout
void cuckoo_hash_table_print(CuckooHashTable *table);

// print some statistics about 'table' to stdout
void cuckoo_hash_table_stats(CuckooHashTable *table);

#endif
