/* * * * * * * * *
 * Dynamic hash table using extendible hashing with multiple keys per bucket,
 * resolving collisions by incrementally growing the hash table
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by ...
 */

#ifndef XTNDBLN_H
#define XTNDBLN_H

#include <stdbool.h>
#include "../inthash.h"

typedef struct xtndbln_table XtndblNHashTable;

// initialise an extendible hash table with 'bucketsize' keys per bucket
XtndblNHashTable *new_xtndbln_hash_table(int bucketsize);

// free all memory associated with 'table'
void free_xtndbln_hash_table(XtndblNHashTable *table);

// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool xtndbln_hash_table_insert(XtndblNHashTable *table, int64 key);

// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool xtndbln_hash_table_lookup(XtndblNHashTable *table, int64 key);

// print the contents of 'table' to stdout
void xtndbln_hash_table_print(XtndblNHashTable *table);

// print some statistics about 'table' to stdout
void xtndbln_hash_table_stats(XtndblNHashTable *table);

#endif