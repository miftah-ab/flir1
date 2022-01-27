import random
import secrets

x = ['1', '2', '3', '4', '5']
ref = 0
inn = input('your reference  ')
if inn in x:
    ref = ref + 1
    print(x[ref])
li = {}
for x in range(1, 6):
    for k in range(5):
        li[x] = k

        print(f'{x}, {secrets.token_hex(2)}  ...... {ref} reference')
        x = x + 1
    break
print(li.keys())
print(li.values())
x = random.randrange(10)
print(x)
