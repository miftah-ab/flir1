import os

import django



from cities_light.models import City


q = input('enter name   ')
city = City.objects.filter(name__istartswith=q)
for c in city:
    print(c)

coun = city.count()
print(coun)
for x in range(1, coun + 1):

    for y in city:
        print(x, y)
        break
        # print(f'{x},{c}')
