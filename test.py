n = input('Numerater: ')
d = input('Denomenater: ')
n = int(n)
d = int(d)
factors = []
for i in range(n):
    if n%(i+1) == 0:
        factors.append(i+1)
factors.reverse()
for i in factors:
    if d%i == 0:
        n /= i
        d /= i
        break
print(n)
print(d)
