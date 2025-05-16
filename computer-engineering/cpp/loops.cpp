#include <iostream>
using namespace std;

int main(){
    
    int x = 0;

    cout << "\nWhile loop is started!\n";
    while (x < 10)
    {
        x++;
        cout<<"X'value is " << x << "\n";
    }
    
    cout << "\nFor loop is started!\n";
    for (int i = 0; i < 10; ++i){
        cout<<"i'value is " << i << "\n";
    }

    return 0;

}