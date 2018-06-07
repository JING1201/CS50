/**
 * helpers.c
 *
 * Computer Science 50
 * Problem Set 3
 *
 * Helper functions for Problem Set 3.
 */
       
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    //linear
    /*
    for (int i=0;i<n;i++){
        if (values[i]==value){
            return true;
        }
    }
    return false;
    */
    
    //binary
    int midIndex=n/2;
    int left=0;
    int right=n-1;
    while (right>=left){
        if (values[midIndex]==value){
            return true;
        }
        else if(value>values[midIndex]){
            left=midIndex+1;
        }
        else if(value<values[midIndex]){
            right=midIndex-1;
        }
        midIndex=(left+right)/2;
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement an O(n^2) sorting algorithm
    //selection sort
    int temp;
    int minIndex;
    for(int i=0;i<n;i++){
        minIndex=i;
        for (int j=i+1;j<n;j++){
            if (values[j]<values[minIndex]){
                minIndex=j;
            }
        }
        temp=values[minIndex];
        values[minIndex]=values[i];
        values[i]=temp;
    }
    return;
}