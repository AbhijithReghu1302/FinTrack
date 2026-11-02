import math


def find_twin_primes(limit=1000):
    primes = []

    for num in range(2, limit):
        is_prime = True

        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(num)

    twin_primes = []

    for i in range(len(primes) - 1):
        if primes[i + 1] - primes[i] == 2:
            twin_primes.append((primes[i], primes[i + 1]))

    return twin_primes


def permutation(n, r):
    if n < 0 or r < 0 or r > n:
        raise ValueError("Invalid values of n and r.")

    return math.factorial(n) // math.factorial(n - r)


def combination(n, r):
    if n < 0 or r < 0 or r > n:
        raise ValueError("Invalid values of n and r.")

    return math.factorial(n) // (
        math.factorial(r) * math.factorial(n - r)
    )