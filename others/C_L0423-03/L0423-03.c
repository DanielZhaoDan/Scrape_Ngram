/*
   Solution to COMP20005 Assignment 1, 23th, April 2017.
   your name and email here!
   ******** programming is fun ******
*/

#include <stdio.h>
#include <stdlib.h>

#define MAX_DATASET_SIZE 50001
#define FILENAME_SIZE 20
#define TITLE_SIZE 100
#define INVALID_TEMP -999
#define DEFAULT_MIN_YEAR 2017
#define DEFAULT_MAX_YEAR -1
#define CHARACTER_SIZE 0.5
#define MONTH_NUMBER 12
#define DOUBLE_DELTA 0.0001
#define STAGE4_OUTPUT_RECORD_NUMBER 5

/* formatting for Stage 3 */
#define DIV "                +---------+---------+---------+---------+---------+---------+"
#define HDR "                0         5        10        15        20        25        30"

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
int read_data_from_file_into_memory(record data_set[], int n_line);
void do_step_1(record data_set[], int data_set_length);
void do_step_2(record data_set[], int data_set_length);
void do_step_3(record data_set[], int data_set_length, double avg_min_temp[], double avg_max_temp[]);
void print_step3_each_month_data(int index, int n_valid_min_temp, int n_valid_max_temp, double avg_min_temp, double avg_max_temp);
void do_step_4(record data_set[], int data_set_length, double total_avg_min_temp[], double total_avg_max_temp[]);
double my_fabs(double ori_data);
int my_getchar(char* line, int max_size);

/* main function */
int
main(int argc, char*argv[]) {
    int data_set_length;
    /* user data_set to store data load from txt file*/
    record data_set[MAX_DATASET_SIZE];
    /* use avg_min_temp, avg_max_temp array to store avg_temp. */
    double avg_min_temp[MONTH_NUMBER] = {0.0};
    double avg_max_temp[MONTH_NUMBER] = {0.0};

    data_set_length = read_data_from_file_into_memory(data_set, MAX_DATASET_SIZE);

    do_step_1(data_set, data_set_length);
    do_step_2(data_set, data_set_length);
    do_step_3(data_set, data_set_length, avg_min_temp, avg_max_temp);
    do_step_4(data_set, data_set_length, avg_min_temp, avg_max_temp);

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
read_data_from_file_into_memory(record data_set[], int n_line) {
    int i=0;
    // read titles 'Product code,BoM station,Year,Month,Day,Maximum (C),Minimum (C)'
    char title[TITLE_SIZE];
    // gets(title);
    my_getchar(title, TITLE_SIZE);
    int location, yy, mm, dd;
    double max, min;
    while (scanf("IDCJAC0010,%d,%d,%d,%d,%lf,%lf\n",&location,&yy,&mm,&dd,&max,&min) != EOF) {
        data_set->bom_station_code = location;
        data_set->year = yy;
        data_set->month = mm;
        data_set->day = dd;
        data_set->max_temp = max;
        data_set->min_temp = min;
        if(++i == n_line) break;
        data_set++;
    }
    return i;
}


int
my_getchar(char* line, int max_size) {
    int c;
    int len = 0;
    while( (c = getchar()) != EOF && len < max_size ){
        line[len++] = c;
        if('\n' == c)
            break;
    }
    line[len] = '\0';
    return len;
}

/*
@function: print step result
@params: data_set: the Struct array to store data
@params: data_set_length: numbers of record
*/
void
do_step_1(record data_set[], int data_set_length) {
    printf("Stage 1\n-------\n");

    printf("Input has %d records\n", data_set_length);

    /* only print when there are records */
    printf("First record in data file:\n");
    if (data_set_length > 0) {
        record first_record = data_set[0];
        printf("  data: %02d/%02d/%d\n", first_record.day, first_record.month, first_record.year);
        printf("  min : %.1lf degrees C\n", first_record.min_temp);
        printf("  max : %.1lf degrees C\n", first_record.max_temp);
    }

    printf("Last record in data file:\n");
    if (data_set_length > 0) {
        record last_record = data_set[data_set_length-1];
        printf("  data: %02d/%02d/%d\n", last_record.day, last_record.month, last_record.year);
        printf("  min : %.1lf degrees C\n", last_record.min_temp);
        printf("  max : %.1lf degrees C\n", last_record.max_temp);
    }
    printf("\n");
}

/*
@function: fabs function to calculate the absolute value of value
@params: -0.0001
@return: 0.0001
*/
double
my_fabs(double ori_data) {
  if (ori_data > 0)
    return ori_data;
  return -ori_data;
}

void
do_step_2(record data_set[], int data_set_length) {
    int i;
    int min_year = DEFAULT_MIN_YEAR;
    int max_year = DEFAULT_MAX_YEAR;

    /* get minimum number of year and maximum number of year */
    for (i=0; i<data_set_length; i++) {
        if (data_set[i].year < min_year)
            min_year = data_set[i].year;
        if (data_set[i].year > max_year)
            max_year = data_set[i].year;
    }
    int array_length = max_year-min_year+1;

    /* use avg_min_temp, avg_max_temp array to store avg_temp.
       use n_valid_min_temp, n_valid_max_temp to store counts of valid temperature data.
       If min_year is 1971 and max_year is 2017, the array length should be 2017-1971+1=47
       avg_temp of 1971 store in index 0 of array,
       avg_temp year 1972 store in index 1 of array...
     */
    double avg_min_temp[array_length];
    double avg_max_temp[array_length];
    int n_valid_min_temp[array_length];
    int n_valid_max_temp[array_length];

    /* initialize the arrays */
    for (i=0; i<array_length; i++) {
      avg_max_temp[i] = 0.0;
      avg_max_temp[i] = 0.0;
      n_valid_min_temp[i] = 0;
      n_valid_max_temp[i] = 0;
    }

    for (i=0; i<data_set_length; i++) {
        int index = data_set[i].year - min_year;
        /* compare if temperature is -999 */
        if (my_fabs(data_set[i].min_temp - INVALID_TEMP) > DOUBLE_DELTA) {
            double total_min_temp = avg_min_temp[index] * n_valid_min_temp[index] + data_set[i].min_temp;
            n_valid_min_temp[index]++;
            avg_min_temp[index] = total_min_temp / n_valid_min_temp[index];
        }
        if (my_fabs(data_set[i].max_temp - INVALID_TEMP) > DOUBLE_DELTA) {
            double total_max_temp = avg_max_temp[index] * n_valid_max_temp[index] + data_set[i].max_temp;
            n_valid_max_temp[index]++;
            avg_max_temp[index] = total_max_temp / n_valid_max_temp[index];
        }
    }

    /* print result */
    printf("Stage 2\n-------\n");
    for (i = 0; i < array_length; i++) {
        if (n_valid_min_temp[i] != 0 || n_valid_max_temp[i] != 0) {
            int year = min_year + i;
            printf("%d: average min:  %5.2lf degrees C (%d days)\n", year, avg_min_temp[i], n_valid_min_temp[i]);
            printf("      average max:  %5.2lf degrees C (%d days)\n", avg_max_temp[i], n_valid_max_temp[i]);
            printf("\n");
        }
    }
}


void
do_step_3(record data_set[], int data_set_length, double avg_min_temp[], double avg_max_temp[]) {
    /* use avg_min_temp, avg_max_temp array to store avg_temp.
       use n_valid_min_temp, n_valid_max_temp to store counts of valid temperature data.
       Jan. will be stored in index 0,
       Feb. will be stored in index 1,
       ...
       Dec. will be stored in index 11.
     */
    int n_valid_min_temp[MONTH_NUMBER] = {0};
    int n_valid_max_temp[MONTH_NUMBER] = {0};
    int i;

    for (i = 0; i < data_set_length; i++) {
        int index = data_set[i].month - 1;
        /* compare if temperature is -999 */
        if (my_fabs(data_set[i].min_temp - INVALID_TEMP) > DOUBLE_DELTA) {
            double total_min_temp = avg_min_temp[index] * n_valid_min_temp[index] + data_set[i].min_temp;
            n_valid_min_temp[index]++;
            avg_min_temp[index] = total_min_temp / n_valid_min_temp[index];
        }
        if (my_fabs(data_set[i].max_temp - INVALID_TEMP) > DOUBLE_DELTA) {
            double total_max_temp = avg_max_temp[index] * n_valid_max_temp[index] + data_set[i].max_temp;
            n_valid_max_temp[index]++;
            avg_max_temp[index] = total_max_temp / n_valid_max_temp[index];
        }
    }

    /* print result */
    printf("Stage 3\n-------\n");
    for (i = 0; i < MONTH_NUMBER; i++) {
        print_step3_each_month_data(i, n_valid_min_temp[i], n_valid_max_temp[i], avg_min_temp[i], avg_max_temp[i]);
    }
    printf("%s\n", DIV);
    printf("%s\n\n", HDR);
}

void
print_step3_each_month_data(int index, int n_valid_min_temp, int n_valid_max_temp, double avg_min_temp, double avg_max_temp) {
    char *month_name[MONTH_NUMBER] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dev"};
    int blank_count = avg_min_temp / CHARACTER_SIZE;
    int star_count = avg_max_temp / CHARACTER_SIZE;
    int i;

    printf("%s (%4d,%4d) |", month_name[index], n_valid_min_temp, n_valid_max_temp);
    for (i = 0; i < blank_count; i++)
        printf(" ");
    for (i = 0; i < star_count-blank_count; i++) {
        (i == star_count-blank_count+1) ? printf("*\n"): printf("*");
    }
    printf("\n");
}

void
do_step_4(record data_set[], int data_set_length, double total_avg_min_temp[], double total_avg_max_temp[]) {
    int i;
    int j;
    int min_year = DEFAULT_MIN_YEAR;
    int max_year = DEFAULT_MAX_YEAR;

    /* get minimum number of year and maximum number of year */
    for (i = 0; i < data_set_length; i++) {
        if (data_set[i].year < min_year)
            min_year = data_set[i].year;
        if (data_set[i].year > max_year)
            max_year = data_set[i].year;
    }
    int array_length = max_year-min_year+1;

    /* use avg_min_temp, avg_max_temp 2-dimensional array to store avg_temp.
       use n_valid_min_temp, n_valid_max_temp to store counts of valid temperature data.
       For 1st dimension:
       If min_year is 1971 and max_year is 2017, the array length should be 2017-1971+1=47
       data of 1971 store in index 0 of 1st dimension,
       data year 1972 store in index 1 of 1st dimension...
       For 2nd dimension:
       data of Jan store in index 0, data of Feb store in index 1...
     */
    double avg_min_temp[array_length][MONTH_NUMBER];
    double avg_max_temp[array_length][MONTH_NUMBER];
    int n_valid_min_temp[array_length][MONTH_NUMBER];
    int n_valid_max_temp[array_length][MONTH_NUMBER];

    /* initialize 2-d array */
    for (i=0; i<array_length; i++)
        for (j=0; j<MONTH_NUMBER; j++) {
          avg_min_temp[i][j] = 0.0;
          avg_max_temp[i][j] = 0.0;
          n_valid_min_temp[i][j] = 0;
          n_valid_max_temp[i][j] = 0;
        }

    for (i=0; i<data_set_length; i++) {
        int year_index = data_set[i].year - min_year;
        int month_index = data_set[i].month - 1;
        if (my_fabs(data_set[i].min_temp - INVALID_TEMP) > DOUBLE_DELTA) {
            double total_min_temp =
              avg_min_temp[year_index][month_index] * n_valid_min_temp[year_index][month_index] + data_set[i].min_temp;
            n_valid_min_temp[year_index][month_index]++;
            avg_min_temp[year_index][month_index] = total_min_temp / n_valid_min_temp[year_index][month_index];
        }
        if (my_fabs(data_set[i].max_temp - INVALID_TEMP) > DOUBLE_DELTA) {
            double total_max_temp =
              avg_max_temp[year_index][month_index] * n_valid_max_temp[year_index][month_index] + data_set[i].max_temp;
            n_valid_max_temp[year_index][month_index]++;
            avg_max_temp[year_index][month_index] = total_max_temp / n_valid_max_temp[year_index][month_index];
        }
    }

    int result[50] = {0};

    printf("Stage 4\n-------\n");
    for (i = 0; i < array_length; i++) {
        for (j = 0; j < MONTH_NUMBER; j++) {
            if (avg_min_temp[i][j] > total_avg_min_temp[j])
                result[i]++;
            if (avg_max_temp[i][j] > total_avg_max_temp[j])
                result[i]++;
        }
        /* print result */
        if (i<STAGE4_OUTPUT_RECORD_NUMBER)
            printf("  %d: score is %2d/24\n", i+min_year, result[i]);
        else if (array_length <= 10) {
            printf("  %d: score is %2d/24\n", i+min_year, result[i]);
        } else {
            if (i == STAGE4_OUTPUT_RECORD_NUMBER+1)
                printf("--\n");
            else if (i >= array_length-STAGE4_OUTPUT_RECORD_NUMBER)
                printf("  %d: score is %2d/24\n", i+min_year, result[i]);
        }
    }
    printf("\n");
}
