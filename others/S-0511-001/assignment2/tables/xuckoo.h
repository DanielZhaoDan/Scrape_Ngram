/* * * * * * * * *
* Dynamic hash table using a combination of extendible hashing and cuckoo
* hashing with a single keys per bucket, resolving collisions by switching keys 
* between two tables with two separate hash functions and growing the tables 
* incrementally in response to cycles
*
* created for COMP20007 Design of Algorithms - Assignment 2, 2017
* by ...
*/

#ifndef XUCKOO_H
#define XUCKOO_H

#include <stdbool.h>
#include "../inthash.h"

typedef struct xuckoo_table XuckooHashTable;

// initialise an extendible cuckoo hash table
XuckooHashTable *new_xuckoo_hash_table();

// free all memory associated with 'table'
void free_xuckoo_hash_table(XuckooHashTable *table);

// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool xuckoo_hash_table_insert(XuckooHashTable *table, int64 key);

// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool xuckoo_hash_table_lookup(XuckooHashTable *table, int64 key);

// print the contents of 'table' to stdout
void xuckoo_hash_table_print(XuckooHashTable *table);

// print some statistics about 'table' to stdout
void xuckoo_hash_table_stats(XuckooHashTable *table);

#endif
