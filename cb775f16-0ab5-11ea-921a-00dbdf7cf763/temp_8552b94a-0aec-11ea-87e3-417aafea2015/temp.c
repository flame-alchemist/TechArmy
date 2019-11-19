#include<stdio.h>
int binarySearch(int *arr, int l, int r, int x)
{
    if (r >= l) { 
		int mid = l + (r - l) / 2; 

		if (arr[mid] == x) 
			return mid; 

		if (arr[mid] > x) 
			return binarySearch(arr, l, mid - 1, x); 

		return binarySearch(arr, mid + 1, r, x); 
	} 
	return -1; 
}
int main()
{
	int n,x;
	scanf("%d",&n);
	int arr[n];
	for(int i=0;i<n;i++)
		scanf("%d",&arr[i]);
	scanf("%d",&x);
	printf("%d",binarySearch(arr, 0, n-1, x));
	return 0;
}