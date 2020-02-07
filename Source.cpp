#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <math.h>

int int_max(int* int_array, int length) {

	//finding the maximum value for an int array

	int res = 0;
	for (int i = 0; i < length; i++) {
		if (res < int_array[i])
			res = int_array[i];
	}

	return res;
}

double double_max(double* double_array, int length) {

	//finding the maximum value for an double array

	double result = 0.0;

	for (int i = 0; i < length; i++) {
		if (result < double_array[i])
			result = double_array[i];
	}

	return result;
}

int int_min(int* int_array, int length) {

	//finding the minimum value for an int array

	int result = int_max(int_array, length);
	for (int i = 0; i < length; i++) {
		if (result > int_array[i])
			result = int_array[i];
	}

	return result;
}

double double_min(double* double_array, int length, int* k_min) {

	//finding the minimum value for an double array

	double result = 0.0;

	double_max(double_array, length);
	for (int i = 0; i < length; i++) {
		if (result > double_array[i]) {
			result = double_array[i];
			if (k_min != NULL)
				*k_min = i;
		}
	}

	return result;
}

void calculation_interval(int x, int length, int parameter, int* start, int* finish) {

	//calculating the start and end of an interval of
	//length <= 2 * parameter to which the point x belongs
	int amount_points = parameter;  //number of points for aveaging


	if (x < amount_points) {
		*start = 0;
		*finish = x + amount_points;
	}
	else if (x >= length - amount_points) {
		*start = x - amount_points;
		*finish = length;
	}
	else {
		*start = x - amount_points;
		*finish = x + amount_points;
	}
}

void int_array_averaging(int int_array_parameter, int length, int* in_array, int* out_array) {

	//averaging an array over several points, the number of which is equal to parameter

	int sum, start = 0, finish = 0;     //start and finish belongs interval

	for (int i = 0; i < length; i++) {
		calculation_interval(i, length, int_array_parameter, &start, &finish);
		sum = 0;
		for (int j = start; j < finish; j++) {
			sum = sum + in_array[j];
		}
		out_array[i] = (int)(sum / (finish - start));
	}
}

void double_array_averaging(int double_array_parameter, int length, double* in_array, double* out_array) {

	//averaging an array over several points, the number of which is equal to parameter
	//if flag = 0, array will has only int values
	//if flag = 1, array will has only double values

	int start = 0, finish = 0;     //start and finish belongs interval
	double sum;

	for (int i = 0; i < length; i++) {
		calculation_interval(i, length, double_array_parameter, &start, &finish);
		sum = 0;
		for (int j = start; j < finish; j++) {
			sum = sum + in_array[j];
		}
		out_array[i] = sum / (finish - start);
	}
}

int search_minimal_period(int* array, int length, int very_average_array_parameter) {

	//finding the minimum period of a periodic function that can only accept int values

	int* very_averaged_array = (int*)malloc(4 * (length + 1) * sizeof(int));
	//it is averaged array. It is needed to celculate minimal period
	int_array_averaging(very_average_array_parameter, length, array, very_averaged_array);
	int maximum = int_max(very_averaged_array, length);
	int minimum = int_min(very_averaged_array, length);
	int middle = (maximum + minimum) / 2;
	int* array_intersections = (int*)malloc(4 * (length + 1) * sizeof(int));
	//it is array of intersections array and line "y = middle"
	int number = 0;     //it is amount of intersections
	int period = length;

	for (int i = 0; i < length; i++) {
		if (((very_averaged_array[i] <= middle) && (middle < very_averaged_array[i + 1])) ||
			((very_averaged_array[i] >= middle) && (middle > very_averaged_array[i + 1]))) {
			array_intersections[number] = i;
			number++;
		}
	}
	for (int i = 0; i < number - 2; i++) {
		if (period >(array_intersections[i + 2] - array_intersections[i]))
			period = array_intersections[i + 2] - array_intersections[i];
	}

	free(very_averaged_array);
	free(array_intersections);

	return (int)(period / 2);
}

void create_array_square_deviation(int* array, int length, int very_average_array_parameter, double* result_array) {

	//calculation of the square deviation of each
	//point of the array from the vertex of the parabola

	long sum1, sum2, sum3;      //variables for calculating the square deviation
	double res;
	int start = 0, finish = 0;
	int period = search_minimal_period(array, length, very_average_array_parameter);
	period = (int)(period / 2);

	for (int i = 0; i < length; i++) {
		calculation_interval(i, length, period, &start, &finish);
		sum1 = 0;
		sum2 = 0;
		sum3 = 0;
		for (int j = start; j < finish; j++) {
			sum1 = sum1 + pow((array[j] - array[i]), 2);
			sum2 = sum2 + (array[j] - array[i]) * pow((j - i), 2);
			sum3 = sum3 + pow((j - i), 4);
		}
		res = sum1 - 3 * (pow(sum2, 2)) / (4 * sum3);
		result_array[i] = res;
	}
}

void rough_search_lows(double* array, int length, int double_array_parameter, int* result_array, int* amount_minima) {

	//create an array of minims on each segment
	//with a length equal to the minimum period
	int amount_intersections = 0, flag = 0, x = 0;  //k_min - x of min
													//if function decreases, flag = 0
													//if function increases, flag = 1
	double max = double_max(array, length);
	double min = double_min(array, length, &x);
	double middle = (max + min) / 2;
	int* array_intersections = (int*)malloc(4 * (length + 1) * sizeof(int));
	double* average_array = (double*)malloc(4 * (length + 1) * sizeof(double));

	double_array_averaging(double_array_parameter, length, array, average_array);
	//1) divide the length into segments at the intersections
	for (int i = 0; i < length - 1; i++) {
		//for the first intersection of the function, only this case is important
		if ((amount_intersections == 0) && (array[i] <= middle) && (middle < array[i + 1])) {
			array_intersections[0] = 0;
			array_intersections[1] = i;
			amount_intersections = 2;
			flag = 1;
		}
		else if (((array[i] >= middle) && (middle > array[i + 1]) && (flag == 0)) ||   //function is decreasing and flag = 0
			((array[i] <= middle) && (middle < array[i + 1]) && (flag == 1))) {        //function is increasing and flag = 1
			array_intersections[amount_intersections] = i;
			amount_intersections++;
			flag = (flag + 1) % 2;		//changing the sign of the derivative
		}
	}
	//for the last intersection of the function, only this case is important
	if (flag == 1) {
		array_intersections[amount_intersections] = length - 1;
		amount_intersections++;
	}

	//2)search for the minimum value on individual segments
	double minimum_separate_segment = 0;
	int k_min = 0;      //k_min is x of minimum_value_separate_segment

	for (int i = 0; i < amount_intersections; i = i + 2) {
		minimum_separate_segment = double_min(&(array[array_intersections[i]]), array_intersections[i + 1] - array_intersections[i], &k_min);
		result_array[i / 2] = array_intersections[i] + k_min;
	}
	*amount_minima = amount_intersections / 2;
	free(array_intersections);
}

void accurate_search_extremes(int* x_array, int length, int* y_array, int* result_array, int* out_length) {

	//specification of extremum coordinates

	int j = 1, number_extrems = 1;      //it is amount of extrems
	int x1, x, x2, y1, y, y2;

	result_array[0] = x_array[0];
	while (j < length - 1) {
		x1 = x_array[j - 1];		//x, x1, and x2 are the coordinates of the rough minima
		x = x_array[j];
		x2 = x_array[j + 1];

		y1 = y_array[x1];			//y, y1, and y2 - function values at points x, x1, and x2
		y = y_array[x];
		y2 = y_array[x2];

		if (((y1 < y) && (y2 < y)) ||
			((y1 > y) && (y2 > y))) {
			result_array[number_extrems] = x;
			number_extrems++;
		}
		j++;
	}
	result_array[number_extrems] = x_array[length - 1];
	*out_length = number_extrems + 1;
}

void trace(int* in_array, int height, int width, int int_array_parameter, int double_array_parameter,
	int very_average_array_parameter, int* out_array, int* amount_lines) {

	//create lines

	int* array_all_extrems = (int*)malloc(4 * (width + 1) * (height + 1) * sizeof(int));
	//it is an array that stores the coordinates of these extremes
	int* array_amounts_extrems = (int*)malloc(4 * (width + 1) * sizeof(int));
	//it is an array which stores numbers of extrems in each segments
	int* averaged_array = (int*)malloc(4 * (height + 1) * sizeof(int));
	//it is an averaged in_array
	double* array_square_deviations = (double*)malloc(4 * (height + 1) * sizeof(double));
	//it is an array of square deviations for each point in one segment
	int* rough_extrems = (int*)malloc(4 * (height + 1) * sizeof(int));
	//it is an array of extrems after rough_search_extrems
	int* accurate_extrems = (int*)malloc(4 * (height + 1) * sizeof(int));
	//it is an array of extrems after accurate_search_extrems
	int amount_rough_extrems = 0;      //number of extrems after rough_search_lows
	int amount_accurate_extrems = 0;   //number of extrems after accurate_search_lows
	int amount_all_extrem = 0;         //number of all extrems
	int minimal_amount_extrem = height;//minimal number of extrem among all segments
	int sum;                       //for create array of lines

								   //1) search for extremes for each slice, creation of array_amounts_extrems and array_amounts_extrems and search minimal_amount_extrem
	for (int i = 0; i < width; i++) {
		int_array_averaging(int_array_parameter, height, &(in_array[i * width]), averaged_array);
		create_array_square_deviation(averaged_array, height, very_average_array_parameter, array_square_deviations);
		rough_search_lows(array_square_deviations, height, double_array_parameter, rough_extrems, &amount_rough_extrems);
		accurate_search_extremes(rough_extrems, amount_rough_extrems, averaged_array,
			accurate_extrems, &amount_accurate_extrems);

		array_amounts_extrems[i] = amount_accurate_extrems;
		if (minimal_amount_extrem > amount_accurate_extrems)
			minimal_amount_extrem = amount_accurate_extrems;
		for (int j = 0; j < amount_accurate_extrems; j++) {
			array_all_extrems[amount_all_extrem + j] = accurate_extrems[j];
		}
		amount_all_extrem = amount_all_extrem + amount_accurate_extrems;
	}

	//2)creation of final one-dimensional array
	*amount_lines = minimal_amount_extrem;
	int x = 0;
	for (int i = 0; i < *amount_lines; i++) {
		sum = 0;
		for (int j = 0; j < width; j++) {
			sum = sum + array_amounts_extrems[j];
			x = array_all_extrems[sum + i + 1];
			out_array[i * width + j] = array_all_extrems[sum + i];
		}
	}

	free(array_all_extrems);
	free(array_amounts_extrems);
	free(averaged_array);
	free(array_square_deviations);
	free(rough_extrems);
	free(accurate_extrems);
}
