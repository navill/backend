from datetime import *
from random import *

# print(dir(datetime.today()))
print(datetime.today().day)
temp_date = datetime.today().replace(day=datetime.today().day + 1).date()

# print(datetime.datetime().replace(minute=30))


# print(time)
# temp_time = 24 - 8 // 5
# print('aa', temp_time)
print()


def random_time():
    temp_time = time()
    add_time = 0
    rand_hour = randint(8, 11)
    for i in range(0, 8):
        rand_minute = randrange(0, 60, 10)
        temp_time = time(rand_hour + add_time, rand_minute)
        print(temp_time)
        add_time += 3
        if (add_time + rand_hour) >= 24:
            break
        print(temp_time)


# print('{0.hour:02}:{0.minute:02}'.format(temp_time))
# 영화는 8시 부터 24시까지

# print('rand:', randint(8, 10))
if __name__ == '__main__':
    random_time()
    print(12 * 12)

    import random

    print(random.sample(range(5), 3))
    screen_max_seat = [36, 82, 150, 140, 130]
    random.shuffle(screen_max_seat)
    print(screen_max_seat[0])
    for i in range(10):
        print(randint(0, 4))

strt = ['디지털', '아날로그', '뭐뭐']
a = ','.join(strt)
print(a)
b = a.split(',')
print(b)

c = [0, 1, 2]
a = [0, 4, 0, 5, 1, 4, 1, 5, 3, 4]
a = list(map(str, a))
print(a)
type_list = list()
# type_list2 = list()

# if (4 or 5) in a:
#     for i in range(0, len(a), 2):
#         type_list.append(a[i:i + 2])
# else:
#     for i in a:
#         z = list()
#         z.append(i)
#         type_list.append(z)

# print(type_list)

# b = ','.join(str(a))
cinema = [{1: '강남'}, {1: '신촌'}, {1: '코엑스'}, {2: '고양스타필드'}, {3: '해운대(장산)'}]

# for i in cinema:
# index, str_cinema = cinema[i].items()
# print(index, str_cinema)

for i in cinema:
    a,b = i.popitem()
    print(a,b)
    print(type(a))


# print(i.keys())
