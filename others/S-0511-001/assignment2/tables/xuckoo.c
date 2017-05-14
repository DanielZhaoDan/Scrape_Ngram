/* * * * * * * * *
* Dynamic hash table using a combination of extendible hashing and cuckoo
* hashing with a single keys per bucket, resolving collisions by switching keys
* between two tables with two separate hash functions and growing the tables
* incrementally in response to cycles
*
* created for COMP20007 Design of Algorithms - Assignment 2, 2017
* by ...
*/

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "xuckoo.h"

#define MAX_LOOP_DEPTH 100
#define INNER_TABLE_SIZE 2
#define MAX_LOAD 0.8
#define rightmostnbits(n, x) (x) & ((1 << (n)) - 1)

// a bucket stores a single key (full=true) or is empty (full=false)
// it also knows how many bits are shared between possible keys, and the first
// table address that references it
typedef struct bucket {
	int id;		// a unique id for this bucket, equal to the first address
				// in the table which points to it
	int depth;	// how many hash value bits are being used by this bucket
	bool full;	// does this bucket contain a key
	int64 key;	// the key stored in this bucket
} Bucket;

// an inner table is an extendible hash table with an array of slots pointing
// to buckets holding up to 1 key, along with some information about the number
// of hash value bits to use for addressing
typedef struct inner_table {
	Bucket **buckets;	// array of pointers to buckets
	int size;			// how many entries in the table of pointers (2^depth)
	int depth;			// how many bits of the hash value to use (log2(size))
	int nkeys;			// how many keys are being stored in the table
	int nbuckets;  //how many buckets in this inner table
} InnerTable;

// a xuckoo hash table is just two inner tables for storing inserted keys
struct xuckoo_table {
	InnerTable *innerTable[INNER_TABLE_SIZE];
	int load;      //how many keys stored in this xuckoo table
	int failedSize;
};

/*
helper functions
*/
// create a new bucket first referenced from 'first_address', based on 'depth'
// bits of its keys' hash values
static Bucket *new_bucket(int first_address, int depth) {
	Bucket *bucket = malloc(sizeof *bucket);
	assert(bucket);
	bucket->id = first_address;
	bucket->depth = depth;
	bucket->full = false;
	return bucket;
}

//new innerTable
InnerTable *new_inner_table() {
	InnerTable *table = malloc(sizeof *table);
	assert(table);

	table->size = 1;
	table->buckets = malloc(sizeof *table->buckets);
	assert(table->buckets);
	table->buckets[0] = new_bucket(0, 0);
	table->depth = 0;
	table->nbuckets = 1;
	table->nkeys = 0;

	return table;
}

//do free inner table structure
void do_free_inner_table(InnerTable *table) {
	assert(table);
	// loop backwards through the array of pointers, freeing buckets only as we
	// reach their first reference
	// (if we loop through forwards, we wouldn't know which reference was last)
	int i;
	for (i = table->size-1; i >= 0; i--) {
		if (table->buckets[i]->id == i) {
			free(table->buckets[i]);
		}
	}
	// free the array of bucket pointers
	free(table->buckets);
	// free the table struct itself
	free(table);
}

// double the table of bucket pointers, duplicating the bucket pointers in the
// first half into the new second half of the table
static void double_table(InnerTable *table) {
	int size = table->size * 2;
	assert(size < MAX_TABLE_SIZE && "error: table has grown too large!");

	// get a new array of twice as many bucket pointers, and copy pointers down
	table->buckets = realloc(table->buckets, (sizeof *table->buckets) * size);
	assert(table->buckets);
	int i;
	for (i = 0; i < table->size; i++) {
		table->buckets[table->size + i] = table->buckets[i];
	}

	// finally, increase the table size and the depth we are using to hash keys
	table->size = size;
	table->depth++;
}

// reinsert a key into the hash table after splitting a bucket --- we can assume
// that there will definitely be space for this key because it was already
// inside the hash table previously
// use 'xtndbl1_hash_table_insert()' instead for inserting new keys
static void reinsert_key(InnerTable *table, int64 key) {
	int address = rightmostnbits(table->depth, h1(key));
	table->buckets[address]->key = key;
	table->buckets[address]->full = true;
}


// split the bucket in 'table' at address 'address', growing table if necessary
static void split_bucket(InnerTable *table, int address) {
	// FIRST,
	// do we need to grow the table?
	if (table->buckets[address]->depth == table->depth) {
		// yep, this bucket is down to its last pointer
		double_table(table);
	}
	// either way, now it's time to split this bucket


	// SECOND,
	// create a new bucket and update both buckets' depth
	Bucket *bucket = table->buckets[address];
	int depth = bucket->depth;
	int first_address = bucket->id;

	int new_depth = depth + 1;
	bucket->depth = new_depth;

	// new bucket's first address will be a 1 bit plus the old first address
	int new_first_address = 1 << depth | first_address;
	Bucket *newbucket = new_bucket(new_first_address, new_depth);
	table->nbuckets++;
	// THIRD,
	// redirect every second address pointing to this bucket to the new bucket
	// construct addresses by joining a bit 'prefix' and a bit 'suffix'
	// (defined below)

	// suffix: a 1 bit followed by the previous bucket bit address
	int bit_address = rightmostnbits(depth, first_address);
	int suffix = (1 << depth) | bit_address;

	// prefix: all bitstrings of length equal to the difference between the new
	// bucket depth and the table depth
	// use a for loop to enumerate all possible prefixes less than maxprefix:
	int maxprefix = 1 << (table->depth - new_depth);

	int prefix;
	for (prefix = 0; prefix < maxprefix; prefix++) {
		// construct address by joining this prefix and the suffix
		int a = (prefix << new_depth) | suffix;

		// redirect this table entry to point at the new bucket
		table->buckets[a] = newbucket;
	}

	// FINALLY,
	// filter the key from the old bucket into its rightful place in the new
	// table (which may be the old bucket, or may be the new bucket)

	// remove and reinsert the key
	int64 key = bucket->key;
	bucket->full = false;
	reinsert_key(table, key);
}


bool do_insert_innerTable(InnerTable *table, int64 key, int address, int hash) {
	assert(table);
	// is this key already there?
	if (table->buckets[address]->full && table->buckets[address]->key == key) {
		return false;
	}
	// if not, make space in the table until our target bucket has space
	while (table->buckets[address]->full) {
		split_bucket(table, address);

		// and recalculate address because we might now need more bits
		address = rightmostnbits(table->depth, hash);
	}

	// there's now space! we can insert this key
	table->buckets[address]->key = key;
	table->buckets[address]->full = true;
	table->nkeys++;
	return true;
}

bool do_xuckoo_hash_table_insert(XuckooHashTable *table, int64 key, int depth) {
	// choose an innertable with fewer keys
	int innerTableIndex = 0;
	if (table->innerTable[1]->nbuckets < table->innerTable[innerTableIndex]->nbuckets)
		innerTableIndex = 1;

	if (depth >= MAX_LOOP_DEPTH) {
		return false;
	}

	//calculate the hashedKey and address
	int hashedKey[INNER_TABLE_SIZE] = {h1(key), h2(key)};
	InnerTable * innerTable = table->innerTable[innerTableIndex];
	int address = rightmostnbits(innerTable->depth, hashedKey[innerTableIndex]);
	/*
	if can successfully insert, then insert it
	else get existed key and put new key here; And then reinsert the existed key
	*/
	if (!innerTable->buckets[address]->full) {
		do_insert_innerTable(table->innerTable[innerTableIndex], key, address, hashedKey[innerTableIndex]);
		return true;
	} else {
		// replace old_key with new_key, and try to insert old_key again
		int64 old_key = innerTable->buckets[address]->key;
		innerTable->buckets[address]->key = key;
		//split bucket
		split_bucket(innerTable, address);
		return do_xuckoo_hash_table_insert(table, old_key, depth+1);
	}
	return false;
}

bool do_lookup_inner_table(InnerTable *table, int64 key, int hashKay) {
	assert(table);
	// calculate table address for this key
	int address = rightmostnbits(table->depth, hashKay);
	// look for the key in that bucket (unless it's empty)
	bool found = false;
	if (table->buckets[address]->full) {
		found = table->buckets[address]->key == key;
	}
	return found;
}
//end of helper functions


// initialise an extendible cuckoo hash table
XuckooHashTable *new_xuckoo_hash_table() {
	XuckooHashTable *table = malloc(sizeof *table);
	assert(table);
	// initialise inner table
	int i;
	for (i=0; i<INNER_TABLE_SIZE; i++) {
		table->innerTable[i] = new_inner_table();
		assert(table->innerTable[i]);
	}
	table->load = 0;
	table->failedSize = 0;
	return table;
}


// free all memory associated with 'table'
void free_xuckoo_hash_table(XuckooHashTable *table) {
	assert(table != NULL);
	//free tables' inner arrays and then free the two tables
	int i=0;
	for (i=0; i<INNER_TABLE_SIZE; i++) {
		do_free_inner_table(table->innerTable[i]);
	}
	// free cuckoo hash table finally
	free(table);
}


// insert 'key' into 'table', if it's not in there already
// returns true if insertion succeeds, false if it was already in there
bool xuckoo_hash_table_insert(XuckooHashTable *table, int64 key) {
	assert(table != NULL);
	if (xuckoo_hash_table_lookup(table, key)){
		return false;
	}

	bool insertResult = do_xuckoo_hash_table_insert(table, key, 1);
	//update load
	if (insertResult) {
		table->load++;
	} else {
		table->failedSize++;
	}
	return insertResult;
}


// lookup whether 'key' is inside 'table'
// returns true if found, false if not
bool xuckoo_hash_table_lookup(XuckooHashTable *table, int64 key) {
	assert(table != NULL);
	int key1 = h1(key);
	int key2 = h2(key);
	return (do_lookup_inner_table(table->innerTable[0], key, key1))
			|| (do_lookup_inner_table(table->innerTable[1], key, key2));
}


// print the contents of 'table' to stdout
void xuckoo_hash_table_print(XuckooHashTable *table) {
	assert(table != NULL);

	printf("--- table ---\n");
	// loop through the two tables, printing them
	int t;
	for (t = 0; t < 2; t++) {
		// print header
		printf("table %d\n", t+1);
		printf("  table:               buckets:\n");
		printf("  address | bucketid   bucketid [key]\n");

		// print table and buckets
		int i;
		for (i = 0; i < table->innerTable[t]->size; i++) {
			// table entry
			printf("%9d | %-9d ", i, table->innerTable[t]->buckets[i]->id);
			// if this is the first address at which a bucket occurs, print it
			if (table->innerTable[t]->buckets[i]->id == i) {
				printf("%9d ", table->innerTable[t]->buckets[i]->id);
				if (table->innerTable[t]->buckets[i]->full) {
					printf("[%llu]", table->innerTable[t]->buckets[i]->key);
				} else {
					printf("[ ]");
				}
			}
			// end the line
			printf("\n");
		}
	}
	printf("--- end table ---\n");
}


// print some statistics about 'table' to stdout
void xuckoo_hash_table_stats(XuckooHashTable *table) {
	assert(table);
	int totalSize = 0;
	// print some stats about state of the table
	int i;
	for (i=0; i<INNER_TABLE_SIZE; i++) {
		printf("--- InnerTable %d ---\n", i);
		printf("   InnerTable size: %d\n", table->innerTable[i]->size);
		printf("    number of keys: %d\n", table->innerTable[i]->nkeys);
		printf(" number of buckets: %d\n\n", table->innerTable[i]->nbuckets);
		totalSize += table->innerTable[i]->nbuckets;
	}
	printf("--- table  stats ---\n");
	printf("current load: %d items\n", table->load);
	printf("current size: %d buckets\n", totalSize);
	printf("load factor: %.3f%%\n", table->load * 100.0 / totalSize);
	printf("Failed to insert: %d\n", table->failedSize);
}
