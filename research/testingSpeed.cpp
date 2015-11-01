#include<time.h>
#include<math.h>
#include<iostream>
using namespace std;

int main (){
	clock_t tStart = clock();
	int c;
	for (int a = 0;a<31457280;a++){
		c = pow(3,3);
	}
	cout << (double)(clock() - tStart)/CLOCKS_PER_SEC;
}
