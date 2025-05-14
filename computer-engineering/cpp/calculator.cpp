#include <iostream>

int main()
{

    std::cout << "Hello, welcome to CPP calculator!\n";
    std::cout << "Please enter first number:\n";

    int firstNumber;
    std::cin >> firstNumber;

    std::cout << "Please enter second number:\n";

    int secondNumber;
    std::cin >> secondNumber;

    std::cout << "Choose one of operations below:\n\t1) Adding \n\t2) Substracting \n\t3) Multiplying \n\t4) Dividing \n";

    
    int oper;
    std::cin >> oper;

    float result;

    if(oper == 1){
        result = firstNumber + secondNumber;
    }else if(oper == 2){
        result = firstNumber - secondNumber;
    }else if(oper == 3){
        result = firstNumber * secondNumber;
    }else if(oper == 4){
        result = firstNumber / secondNumber;
    }

    std::cout << "The reuslt is --- " << result << ":\n";

    std::cout << "Want to calculate again, type 'yes' or any other to exit:\n";
    std::string again;
    std::cin >> again;

    if(again == "yes"){
        main();
    }
    

    return 0;
}
