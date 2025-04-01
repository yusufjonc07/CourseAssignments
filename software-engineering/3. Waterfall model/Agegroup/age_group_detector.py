# Age group detector class  

# Define the age groups
AGE_GROUPS = [
    {
        "name": "Child",
        "min_age": 0,
        "max_age": 12,
    },
    {
        "name": "Teenager",
        "min_age": 13,
        "max_age": 19,
    },
    {
        "name": "Adult",
        "min_age": 20,
        "max_age": 59,
    }
]


# Define the function to detect the age group
def detect_age_group(age):
    
    
    # Check if the age is a number
    if not age.isnumeric():
        raise ValueError("Age must be a number")
    
    # Convert the age to an integer
    age = int(age)
    
    # Check if the age is negative
    if age < 0:
        raise ValueError("Age cannot be negative")
    
    # Check if the age is greater than 59
    if age > 59:
        return "Senior"
    
    # Check the age group
    for group in AGE_GROUPS:
        if group["min_age"] <= age <= group["max_age"]:
            return group["name"]
    
    # Return unknown if the age group is not found  
    return "Unknown"



while True:
    
    # Get the name and age from the user
    name = input("Enter your name or 'exit' to quit: ")
    
    # Check if the user wants to exit
    if name.lower() == "exit":
        break
    
    age = input("Enter your age: ")
    age_group = detect_age_group(age)
    
    print(f"Hello {name}, you are a {age_group}")
    
    
