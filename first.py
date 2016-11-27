import timeit

def countPrimes1(n):
    count = 1 if n > 2 else 0
    if count == 0:
        return 0
    list = [True] * n
    for i in range(3, n, 2):
        if not list[i]:
            continue
        count += 1
        for o in range(i * i, n, i):
            list[o] = False
    return count


def countPrimes2(n):
    count = 1 if n > 2 else 0
    if count == 0:
        return 0
    dict = {x: True for x in range(n)}
    for i in range(3, n, 2):
        if not dict[i]:
            continue
        count += 1
        for o in range(i * i, n, i):
            del dict[o]
    return count

class Fun:
    v = 'taras'
    d = 14

fun = Fun()
print(fun.__dict__)

# print('1 ', timeit.timeit('countPrimes1(1000000)', 'from __main__ import countPrimes1', number=10))
# print('2 ', timeit.timeit('countPrimes2(1000000)', 'from __main__ import countPrimes2', number=10))



