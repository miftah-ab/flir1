import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'bb.settings'
django.setup()
from cities_light.models import City, Country, Region, CITY_SOURCES

li = ['a', 'b', 'c', 'd']
di = {'a': 'aa', 'b': 'bb', 'c': 'cc', 'd': 'dd'}


def ci():
    q = input('enter name   ')
    city = City.objects.filter(name__istartswith=q)
    co = Country.objects.filter(name__istartswith=q)
    re = Region.objects.filter(name__istartswith=q)
    coun = city.count()
    print(co)
    print(re)
    print(coun)
    global al
    al = {}
    for x in range(1, coun + 1):
        for y in city:
            al[x] = y
            print(f'{x}, {y}')
            x = x + 1
        break
    print(al.keys())
    print(al.values())
    inp = int(input('Select City   '))
    if inp in al.keys():
        print(f'your city is {al[inp]}')
    else:
        print('Wrong Input select Again')

    car = {'1': 'Qiah', '2': 'Nissan', '99': 'other'}
    # print(car.keys())


def main():
    ci()


if __name__ == '__main__':
    main()
