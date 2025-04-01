import time

#simple array of numbers
numArr = [101, 202, 303, 404, 505]
print("Given array:", numArr)

# Traversing
for num in numArr:
    print(num)

# Insertion

# insert at the begin
numArr.insert(0,101)
print("101 was added at the begin:", numArr)

# insert to end
numArr.append(606)
print("606 was added to the end:", numArr)

# insert at index
numArr.insert(2, 707)
print("707 was added at index 2:", numArr)

# Deletion

# delete from the begin
numArr.pop(0)
print("10 was deleted from the begin:", numArr)

# delete an at a given index
numArr.pop(2)
print("303 was deleted at index 2:", numArr)

# delete a given element at fitst occurance
numArr.remove(404)
print("404 was deleted:", numArr)

# delete a given element at all occurances
newNumArr = [x for x in numArr if x != 100]
print("All 100s were deleted:", newNumArr)

# just delete last element from the array
lastElement = numArr[-1]
numArr.pop()
print(f"Last element ({lastElement}) was deleted:", numArr)

# Searching

bigNumerArr = [x for x in range(1000000)]

# Linear search
def linearSearch(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1

startAt = time.time()
foundIndex = linearSearch(bigNumerArr, 505)
endAt = time.time()

if foundIndex != -1:
    print("Linear Search:", foundIndex, "and found in", (endAt - startAt)*1000, "milliseconds")
else:
    print("Element not found")


# Binary search
def binarySearch(arr, key):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            left = mid + 1
        else:
            right = mid 
            - 1
    return -1

startAt = time.time()
foundIndex = binarySearch(bigNumerArr, 505)
endAt = time.time()

if foundIndex != -1:
    print("Binary Search:", foundIndex, "and found in", (endAt - startAt)*1000, "milliseconds")
else:
    print("Element not found")
    
# Sorting
# Bubble sort
unsortedArr = [4, 2, 8, 0, 5, 1, 9]

for i in range(len(unsortedArr)-1):
    for j in range(len(unsortedArr)-i-1):
        if unsortedArr[j] > unsortedArr[j+1]:
            unsortedArr[j], unsortedArr[j+1] =unsortedArr[j+1], unsortedArr[j]
            
print("Bubble Sort:", unsortedArr)