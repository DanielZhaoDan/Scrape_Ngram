/* Solution to COMP20005 Assignment 1, 23th, April 2017.
   your name and email here!
   ******** programming is fun ******
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_DATASET_SIZE 50001
#define FILENAME_SIZE 20
#define TITLE_SIZE 100
#define INVALID_TEMP -999

/* Struct for record */
typedef struct {
  int bom_station_code;
  int year;
  int month;
  int day;
  double max_temp;
  double min_temp;
} record;

/* function prototypes */
int read_data_from_file_into_memory(char filename[], record data_set[], int n_line, int has_title);
void do_step_1(record data_set[], int data_set_length);
void do_step_2(record data_set[], int data_set_length);

/* main function */
int
main(int argc, char*argv[]) {
  int data_set_length;
  record data_set[MAX_DATASET_SIZE];

  if(argc!=2){
    printf("Please enter filename!");
    exit(0);
  }

  data_set_length = read_data_from_file_into_memory(argv[1], data_set, MAX_DATASET_SIZE, 1);

  do_step_1(data_set, data_set_length);
  do_step_2(data_set, data_set_length);

  return 0;
}

/*
@function: read data set from file into array
@params: filename: name of file
@params: data_set: the Struct array to store data
@params: max_line: the maximum number of record read from file
@params: has_title: if file has title, method should skip title
@return: number of record loaded from file
*/
int
read_data_from_file_into_memory(char filename[], record data_set[], int n_line, int has_title) {
  FILE *fd;
  int i=0;

  if((fd=fopen(filename,"r"))==NULL){
      perror("fopen");
      exit(1);
  }

  if (has_title == 1) {
    char title[TITLE_SIZE];
    fgets(title , 100 , fd);
  }

  while (fscanf(fd,"IDCJAC0010,%d,%d,%d,%d,%lf,%lf\n",
    &data_set->bom_station_code, &data_set->year, &data_set->month,
    &data_set->day, &data_set->max_temp, &data_set->min_temp)!=EOF) {
      if(++i==n_line) break;
      data_set++;
  }
  fclose(fd);
  return i;
}

/*
@function: print step result
@params: data_set: the Struct array to store data
*/
void
do_step_1(record data_set[], int data_set_length) {
  printf("Stage 1\n------\n");

  /* print records length */
  printf("Input has %d records\n", data_set_length);

  /* print first record */
  printf("First record in data file:\n");
  /* only print when there are records */
  if (data_set_length > 0) {
    record first_record = data_set[0];
    printf("  data: %02d/%02d/%d\n", first_record.day, first_record.month, first_record.year);
    printf("  min : %.1lf degrees C\n", first_record.min_temp);
    printf("  max : %.1lf degrees C\n", first_record.max_temp);
  }

  /* print last record */
  printf("Last record in data file:\n");
  if (data_set_length > 0) {
    record last_record = data_set[data_set_length-1];
    printf("  data: %02d/%02d/%d\n", last_record.day, last_record.month, last_record.year);
    printf("  min : %.1lf degrees C\n", last_record.min_temp);
    printf("  max : %.1lf degrees C\n", last_record.max_temp);
  }
  printf("\n");
}

void
do_step_2(record data_set[], int data_set_length) {
  double sum_min_temp = 0.0;
  double sum_max_temp = 0.0;
  int i;
  int n_valid_min_temp = 0;
  int n_valid_max_temp = 0;

  for (i=0;i<data_set_length;i++) {
    if (fabs(data_set[i].min_temp - INVALID_TEMP) > 0.0001) {
      sum_min_temp += data_set[i].min_temp;
      n_valid_min_temp++;
    }
    if (fabs(data_set[i].max_temp - INVALID_TEMP) > 0.0001) {
      sum_max_temp += data_set[i].max_temp;
      n_valid_max_temp++;
    }
  }

  double avg_min_temp = sum_min_temp / n_valid_min_temp;
  double avg_max_temp = sum_max_temp / n_valid_max_temp;
  printf("%.2lf\n", avg_min_temp);
  printf("%.2lf\n", avg_max_temp);
}
