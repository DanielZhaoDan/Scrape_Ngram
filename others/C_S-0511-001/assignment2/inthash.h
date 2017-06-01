/* * * * * * * * *
 * Module containing hash functions for 64-bit unsigned integers
 *
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Matt Farrugia <matt.farrugia@unimelb.edu.au>
 */

#ifndef INTHASH_H
#define INTHASH_H

#include <stdint.h>

// the maximum allowable table size; 2^27 = ~134 million entries
// a table with this many 8 byte entries (e.g. pointers or 64-bit integers)
// would take up 2^27 * 8 bytes = 2^30 bytes = 1GB of memory
#define MAX_TABLE_SIZE 134217728

// alias for unsigned 64-bit integer type
typedef uint64_t int64;


// the following functions take a 64-bit integer key and return a 32-bit signed
// integer hash, calculated as ( A * key + B ) % p where p is a large prime.
// p is just under 2^31, so the result of this expression will always be
// between 0 and 2^31-1 (including accounting for overflows, since the
// expression is unsigned). therefore, when returned as a 32-bit signed
// integer, the result will always be non-negative
//
// when using these functions, remember to modulo by the size of your hash table
// to get a valid address

// first available hash function
int h1(int64 k);

// second available hash function
int h2(int64 k);

#endif
