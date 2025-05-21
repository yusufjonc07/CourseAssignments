#include <iostream>
using namespace std;

void factoCalc(int num){
    cout << "Input a number to find the factorial:";

    if(num > 0){ cout << num << endl; }
    else{ cin >> num; }

    int fact=1;

    for(int i=num; i>0; --i){
        fact *= i;
    }

    cout << "The factorial of the given number is:" << fact << endl;
    cout << "-------------DONE-------------\n";

    factoCalc(0);


    
}

int main()
{
  
    factoCalc(5);
    factoCalc(0);

    
    return 0;
}
