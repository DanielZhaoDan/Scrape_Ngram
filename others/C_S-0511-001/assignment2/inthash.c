/* * * * * * * * *
 * Module containing hash functions for 64-bit unsigned integers
 *
 * created for COMP20007 Design of Algorithms - Assignment 2, 2017
 * by Matt Farrugia <matt.farrugia@unimelb.edu.au>
 */

#include "inthash.h"

// constants for first hash function
#define A1 885390553
#define B1 639360243
#define p1 2147483629

// constants for second hash function
#define A2 853977193
#define B2 306837493
#define p2 2147483563

// first available hash function
int h1(int64 k) {
	return (A1 * k + B1) % p1;
}

// second available hash function
int h2(int64 k) {
	return (A2 * k + B2) % p2;
}
