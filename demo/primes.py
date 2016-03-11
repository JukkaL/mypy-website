# Generate all prime numbers up to 1000 using the
# sieve of Eratosthenes.

import math
import sys

max = 1000

# Calculate a table a where a[i] == True
# iff i is a prime.
a = [True] * (max + 1)
for i in range(2, int(math.sqrt(max)) + 1):
    if a[i]:
        j = i * i
        while j <= max:
            a[j] = False
            j += i
            
for i in range(2, max + 1):
    if a[i]:
        print(i)
