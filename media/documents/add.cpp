#include<bits/stdc++.h>

using namespace std;

int add(int a, int b)
{
	int sum,carry;
	if(b==0)
		return a;
	sum = a ^ b;
	carry = (a & b) << 1;
	return add(sum,carry);
}

