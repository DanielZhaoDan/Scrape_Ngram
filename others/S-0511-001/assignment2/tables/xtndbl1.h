/* * * * * * * * *
 * Dynamic hash table using extendible hashing to resolve collisions by
 * incrementally growing the hash table
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Matt Farrugia <matt.farrugia@unimelb.edu.au>
 */

#ifndef XTNDBL1_H
#define XTNDBL1_H

#include <stdbool.h>
#include "../inthash.h"

typedef struct xtndbl1_table Xtndbl1HashTable;

// initialise a single-key extendible hash table
Xtndbl1HashTable *new_xtndbl1_hash_table();

// free all memory associated with 'table'
void free_xtndbl1_hash_table(Xtndbl1HashTable *table);

// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool xtndbl1_hash_table_insert(Xtndbl1HashTable *table, int64 key);

// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool xtndbl1_hash_table_lookup(Xtndbl1HashTable *table, int64 key);

// print the contents of 'table' to stdout
void xtndbl1_hash_table_print(Xtndbl1HashTable *table);

// print some statistics about 'table' to stdout
void xtndbl1_hash_table_stats(Xtndbl1HashTable *table);

#endif
