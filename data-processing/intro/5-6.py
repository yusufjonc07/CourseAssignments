# 5.	Use a while loop to calculate the sum of numbers from 1 to 50.
sum = 0
i = 1
while i <= 50:
    sum += i
    i += 1
print("The sum is:", sum)

# 6.	Write a function that returns the factorial of a given number.
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print("Factorial of 5 is:", factorial(5))
