/*
 * Written by Felipe Sasso <felipecsasso@gmail.com>, May 2016
 */

#include <iostream>
#include <math.h>
#include <time.h>

using namespace std;

long long getIndex(int *numberOfFoldsOp, long long *desiredNumber) {

	long long total;
	long long indexOfNumber[2];

 	total = pow(2, *numberOfFoldsOp);
	indexOfNumber[0] = 1;
	indexOfNumber[1] = *desiredNumber;

	for (int index = 0; index < *numberOfFoldsOp; index++) {
	
		long long half = total / 2;	
		long long row = indexOfNumber[1];

		if (row > half) {
			long long newRow = (total - row) + 1;
			long long col = indexOfNumber[0];

			long long newSize = pow(2, index + 1);
      long long newCol = newSize - (col - 1);

			indexOfNumber[0] = newCol;
			indexOfNumber[1] = newRow;
		}

		total = total / 2;
	}
	
	return indexOfNumber[0];	
}

int main ( ) {
	int numberOfFoldsOp;
	long long index;
	long long desiredNumber;

	clock_t timeCount;

	cout << "Please, enter the number of foldings: ";
	cin >> numberOfFoldsOp;	

	cout << "Please, enter the number you are looking for: ";
	cin >> desiredNumber;	

	timeCount = clock();

	index = getIndex(&numberOfFoldsOp, &desiredNumber);

	timeCount = clock() - timeCount;

	cout << "The index of " << desiredNumber << " is " << index - 1 << "."<< endl;
	cout << "Time: " << float(timeCount)/CLOCKS_PER_SEC * 1000 << " seconds." << endl;
	
	return 0;	
}
