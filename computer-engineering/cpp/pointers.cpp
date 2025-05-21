#include <iostream>
using namespace std;

void myFunc()
{
    int a = 10;
    int b = 20;

    cout << "Address of a: " << &a << endl;
    cout << "Address of b: " << &b << endl;
}

void scanStack()
{
    int localVar = 123;
    unsigned char *p = (unsigned char *)&localVar;

    for (int i = 0; i < 100; ++i)
    {
        cout << "Byte " << i << ": " << hex << (int)*(p - i) << endl;
    }
}

int main()
{
    int num = 42;
    int *ptr = &num; // getting the address of num

    cout << "Value of num: " << num << endl;
    cout << "Address of num: " << &num << endl;
    cout << "Pointer adress: " << &ptr << endl;

    int arr[5] = {10, 20, 30, 40, 50};

    cout << "Address of arr:      " << arr << endl;
    cout << "Address of &arr[0]:  " << &arr[0] << endl;
    cout << "Address of &arr[1]:  " << &arr[1] << endl;
    cout << "Address of &arr[1]:  " << &arr[2] << endl;
    cout << "Address of &arr[1]:  " << &arr[3] << endl;

    cout << "Address of function:  " << (void *)myFunc << endl;
    myFunc();

    scanStack();

    int a = 123;
    int *p = &a;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 1e9; ++i)
        volatile int x = a;
    auto end = std::chrono::high_resolution_clock::now();
    // Compare with:
    for (int i = 0; i < 1e9; ++i)
        volatile int x = *p;

    return 0;
}
