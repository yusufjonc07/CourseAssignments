# 1. Given an array of integers nums and an integer target, 
# return indices of the two numbers such that they add up to target. 
# You may assume that each input would have exactly one solution, 
# and you may not use the same element twice. 
# You can return the answer in any order.

# Input: nums = [2, 7, 11, 15], target = 9

def twoSum(nums, target):
    hash_table = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_table:
            return [hash_table[complement], i]
        hash_table[num] = i
    return []

# Example usage:
nums = [2, 7, 11, 15]
target = 9
print(twoSum(nums, target))  # Output: [0, 1]


# 2. Given an array of strings strs, group the anagrams together. 
# You can return the answer in any order. 
# An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, 
# typically using all the original letters exactly once.
# Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

def groupAnagrams(strs):
    anagrams = {}
    for word in strs:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in anagrams:
            anagrams[sorted_word] = []
        anagrams[sorted_word].append(word)
    return list(anagrams.values())

# Example usage:
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(groupAnagrams(strs))
# Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

# 3. Given an array of integers and an integer k, 
# find out whether there are two distinct indices i and j in the array such that the sum of the elements 
# between indices i and j is exactly k, and i and j are less than k distance apart. Use linear probing 
# to store the running sum mod k values to handle collisions and check for the conditions.
# Input: nums = [23, 2, 4, 6, 7], k = 6
def checkSubarraySum(nums, k):
    if k == 0:
        return False
    
    hash_table = {}
    running_sum = 0
    
    for i in range(len(nums)):
        running_sum += nums[i]
        mod = running_sum % k
        
        if mod in hash_table:
            if i - hash_table[mod] <= k:
                return True
        else:
            # Linear probing to handle collisions
            j = mod
            while j in hash_table:
                j = (j + 1) % len(nums)
            hash_table[j] = i
    
    return False

# Example usage:
nums = [23, 2, 4, 6, 7]
k = 6
print(checkSubarraySum(nums, k))  # Output: True (because 2 + 4 = 6)

