
# 1. Implement a gachon_stack data structure from scratch with operations like push, pop, and peek.

gachon_stack = []

# Push
gachon_stack.append(29)
gachon_stack.append(23)
gachon_stack.append(98)


# Stack with capacity 3 elements
print("Stack: ", gachon_stack)

# Pop
element = gachon_stack.pop()
print("Pop: ", element)

# Peek
topElement = gachon_stack[-1]
print("Peek: ", topElement)

# isEmpty
isEmpty = not bool(gachon_stack)
print("isEmpty: ", isEmpty)

# Size
print("Size: ",len(gachon_stack))