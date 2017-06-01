/* * * * * * * * *
 * Dynamic hash table using linear probing to resolve collisions
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Matt Farrugia <matt.farrugia@unimelb.edu.au>
 */

#include <stdbool.h>
#include "../inthash.h"

typedef struct linear_table LinearHashTable;

// initialise a linear probing hash table with initial size 'size'
LinearHashTable *new_linear_hash_table(int size);

// free all memory associated with 'table'
void free_linear_hash_table(LinearHashTable *table);

// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool linear_hash_table_insert(LinearHashTable *table, int64 key);

// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool linear_hash_table_lookup(LinearHashTable *table, int64 key);

// print the contents of 'table' to stdout
void linear_hash_table_print(LinearHashTable *table);

// print some statistics about 'table' to stdout
void linear_hash_table_stats(LinearHashTable *table);

