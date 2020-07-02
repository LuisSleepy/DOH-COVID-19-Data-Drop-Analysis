import sys
import numpy as np

a = np.array([1, 2, 3, 4], dtype = np.int8)
b = np.array([0, -5, 1, 1.5, 2])
# print(a[0:])
# print(b[[0, 2, -1]])
# print(a.dtype)
# print(b.dtype)

# Multi-dimensional arrays or matrices
A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
# print(A.ndim)

# Broadcast and vectorized operations
arr = np.arange(4)
# print(arr + 10)
# This will not change arr
# arr += 10
print(arr)
print(arr >= 2)
print(arr.mean())
print("Equal or greater than 2", arr[arr >= 2])
print("Numbers greater than the mean", arr [(arr > arr.mean())])
print("Numbers not greater than the mean", arr [~ (arr > arr.mean())])

# Creating filters using Boolean logic
B = np.random.randint(0, 100, size= (3, 3))
print(B)
print(B[B > 30])


