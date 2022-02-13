xx = '1256442'
print(xx[0:1])


for x in range(5):
    # print(x) print random number
    inn = input('P  OR  N   ').lower()
    if inn == 'n':
        print(x)
    # elif inn == 'P':
    # print(x-2)
    else:
        print('Wrong input')
if inn == 'N':
    print('Next')
