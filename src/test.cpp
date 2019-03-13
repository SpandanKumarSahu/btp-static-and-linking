#include <stdlib>

class Sample{
public:
	int x(){
		return 10;
	}
};


class Sample2: public Sample{
public:
	int z;
};

struct Sample{
	int x;
	struct Sample2{
		int y;
	};
	struct Sample2 z;
}

int sum(int a, int b){
	return a+b;
}

// #define LIMIT 5
int main(){
	int ar[6];
	ar[5] = 7;
	return 0;
}
