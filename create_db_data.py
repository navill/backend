from database.models import *
from random import *
from datetime import *
import random

age = {
    0: '전체 관람가',
    1: '12세 관람가',
    2: '15세 관람가',
    3: '19세 관람가',
}
data = [
    {
        "id": 1,
        "title": "스파이더맨: 파프 롬 홈",
        "age": 1,
        "booking_rate": 9.5,
        "type": "디지털(자막), ATMOS(자막), 3D(자막), 3D ATMOS(자막)",
        "release_date": "2019-07-02",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/9F/B762F4-F7EE-48BB-B54F-F9000DCCA155.large.jpg',
        "director": "존 왓츠",
        "cast": "톰 홀랜드, 사무엘 L. 잭슨, 젠다야 콜맨, 코비 스멀더스, 존 파브로, 마리사 토메이, 제이크 질렌할, 제이콥 배덜런",
        "genre": "코미디, SF, 액션, 어드벤처",
        "running_time": 130,
        "description": " ",
    },
    {
        "id": 2,
        "title": "라이온킹",
        "age": 0,
        "booking_rate": 67.5,
        "type": "디지털(자막), ATMOS(자막), 디지털(더빙), 3D(자막), 3D(더빙)",
        "release_date": "2019-07-17",
        "img_url": "http://image2.megabox.co.kr/mop/poster/2019/07/996B6C-3897-4580-B419-36B37F7FB043.large.jpg",
        "director": "존 파브로",
        "cast": "도날드 글로버, 비욘세 놀즈, 제임스 얼 존스, 치웨텔 에지오포, 세스 로건",
        "genre": "가족, 드라마, 어드벤처",
        "running_time": 118,
        "description": " ",
    },
    {
        "id": 3,
        "title": "알라딘",
        "age": 0,
        "booking_rate": 8.1,
        "type": "디지털(자막), ATMOS(자막), 디지털(더빙), 3D(자막), 3D(더빙)",
        "release_date": "2019-05-23",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/BC/F3BD5B-0A1A-4D98-A22E-3743EEDBF403.large.jpg',

        "director": "가이 리치",
        "cast": "윌 스미스, 나오미 스콧",
        "genre": "가족, 판타지, 어드벤처",
        "running_time": 127,
        "description": " ",
    },
    {
        "id": 4,
        "title": "토이스토리4",
        "age": 0,
        "booking_rate": 1.5,
        "type": "디지털(자막), 디지털(더빙), 3D(자막), 3D(더빙), ATMOS(자막)",
        "release_date": "2019-06-20",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/08/2A0450-B477-4367-A065-85236F25C540.large.jpg',

        "director": "조시 쿨리",
        "cast": "톰 행크스, 애니 팟츠, 조앤 쿠삭, 팀 알렌",
        "genre": "애니메이션",
        "running_time": "100",
        "description": " ",
    },
    {
        "id": 5,
        "title": "기생충",
        "age": 2,
        "booking_rate": "0.8",
        "type": "디지털, ATMOS, 디지털배리어프리",
        "release_date": "2019-05-30",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/07/F2B772-860E-4A3B-873C-F9E1C8C47966.large.jpg',

        "director": "봉준호",
        "cast": "송강호, 이선균, 조여정, 최우식, 박소담, 장혜진",
        "genre": "드라마",
        "running_time": 131,
        "description": " ",
    },
    {
        "id": 6,
        "title": "존 윅 3: 파라벨룸",
        "age": 3,
        "booking_rate": 0.3,
        "type": "디지털(자막)",
        "release_date": "2019-06-26",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/F9/FA465F-5589-4C68-A188-F50DE69F97B0.large.jpg',

        "director": "채드 스타헬스키",
        "cast": "키아누 리브스, 할리 베리, 로렌스 피쉬번, 이안 맥쉐인",
        "genre": "스릴러, 액션, 범죄",
        "running_time": 131,
        "description": " ",
    },
    {
        "id": 7,
        "title": "기방도령",
        "age": 2,
        "booking_rate": 0.4,
        "type": "디지털",
        "release_date": "2019-07-10",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/89/E48867-C962-41A8-A796-63544421A8A7.large.jpg',

        "director": "남대중",
        "cast": "이준호, 정소민, 최귀화, 예지원, 공명",
        "genre": "/",
        "running_time": 110,
        "description": " ",
    },
]

movie_urls = {
    '스파이더맨: 파 프롬 홈': ['http://image2.megabox.co.kr/mop/poster/2019/9F/B762F4-F7EE-48BB-B54F-F9000DCCA155.large.jpg',
                      '2019-07-03', 8.5],
    '라이온킹': ['http://image2.megabox.co.kr/mop/poster/2019/07/996B6C-3897-4580-B419-36B37F7FB043.large.jpg',
             '2019-07-17', 69.4],
    '알라딘': ['http://image2.megabox.co.kr/mop/poster/2019/BC/F3BD5B-0A1A-4D98-A22E-3743EEDBF403.large.jpg', '2019-05-23',
            7.1],
    '토이스토리 4': ['http://image2.megabox.co.kr/mop/poster/2019/08/2A0450-B477-4367-A065-85236F25C540.large.jpg',
                '2019-07-03', 60],
    '기생충': ['http://image2.megabox.co.kr/mop/poster/2019/07/F2B772-860E-4A3B-873C-F9E1C8C47966.large.jpg', '2019-07-03',
            60],
    '존 윅 3: 파라벨룸': ['http://image2.megabox.co.kr/mop/poster/2019/F9/FA465F-5589-4C68-A188-F50DE69F97B0.large.jpg',
                    '2019-07-03', 60],
    '기방도령': ['http://image2.megabox.co.kr/mop/poster/2019/89/E48867-C962-41A8-A796-63544421A8A7.large.jpg',
             '2019-07-03', 60],
}
# 너무 많아서 아래는 보류
#     '걸캅스': ['http://image2.megabox.co.kr/mop/poster/2019/69/34A92B-6A66-4BE5-A0B3-A4BDE4D10D41.large.jpg', '2019-07-03',
#             60],
#     '칠드런 액트': ['http://image2.megabox.co.kr/mop/poster/2019/BD/8B9A17-1A31-4160-920E-5B0A88B9593E.large.jpg',
#                '2019-07-03', 60],
#     '마리아 칼라스: 세기의 디바': ['http://image2.megabox.co.kr/mop/poster/2019/DB/C1D446-456D-4E07-9AB0-6BB8B760A4DA.large.jpg',
#                         '2019-07-03', 60],
#     '나랏말싸미': ['http://image2.megabox.co.kr/mop/poster/2019/F5/A1A99E-025A-4874-B479-1597994D94A8.large.jpg',
#               '2019-07-03', 60],
#     '어벤져스: 엔드게임': ['http://image2.megabox.co.kr/mop/poster/2019/01/3EA32B-AC6E-444E-ADD8-E3D8C05193CD.large.jpg',
#                    '2019-07-03', 60],
#     '행복한 라짜로': ['http://image2.megabox.co.kr/mop/poster/2019/8B/AD4DE6-D90F-42AA-8BA8-ECF6126CA247.large.jpg',
#                 '2019-07-03', 60],
#     '이웃집 토토로': ['http://image2.megabox.co.kr/mop/poster/2019/DF/520A19-8CA5-47B8-B0BD-82FA80029FA4.large.jpg',
#                 '2019-07-03', 60],
# }


# Movie & Movie_detail 객체 생성
def create_objects_movie_movie_detail():
    for index, movie_data in enumerate(movie_urls.items()):
        # print(data[index]['title'], data[index]['age'], data[index]['booking_rate'], data[index]['type'],
        #       data[index]['release_date'], data[index]['img_url'], data[index]['director'], data[index]['cast'],
        #       data[index]['running_time'])
        # print(data[index]['img_url'])
        Movie.objects.create(title=data[index]['title'], age=data[index]['age'],
                             type=data[index]['type'],
                             booking_rate=data[index]['booking_rate'], release_date=data[index]['release_date'],
                             img_url=data[index]['img_url'])
        Movie_detail.objects.create(movie_id=data[index]['id'], director=data[index]['director'],
                                    cast=data[index]['cast'], genre=data[index]['genre'],
                                    running_time=data[index]['running_time'])


# Screen 객체 생성
# fields : screen_number, total_seat, cinema_id_id
def create_objects_screen():
    total_seat = [120, 110, 90, 80, 70, 130, 135, 150, 200]
    cinema = ['강남', '군자', '동대문', '대전', '세종']
    for i in range(len(cinema)):
        Cinema.objects.create(cinema_name=cinema[i])
    for i in range(1, 6):
        for j in range(1, 5):
            rand = int(randint(0, 8))
            id_number = i + j
            Screen.objects.create(screen_number=j, total_seat=total_seat[rand], cinema_id_id=i)


# date 객체 생성
# fields : date, screen_id_id
def create_objects_date():
    screen_objects = Screen.objects.all().order_by('id')
    for index, screen_object in enumerate(screen_objects, start=1):
        for i in range(0, 4):
            temp_date = datetime.today().replace(day=datetime.today().day + i).date()
            Schedule_date.objects.create(date=temp_date, screen_id_id=index)


# fields : seat_count, start_time, string_date, date_id_id, movie_id_id
def create_objects_time():
    date_objects = Schedule_date.objects.all().order_by('id')
    for index, date_object in enumerate(date_objects, start=1):
        splited_date = list(map(int, str(date_object.date).split('-')))
        str_list_date = [str(a) for a in splited_date]
        str_date = ''.join(str_list_date)

        temp_time = time()
        add_time = 0
        rand_hour = randint(8, 11)
        for i in range(0, 8):
            movie_id = randint(1, 7)
            rand_minute = randrange(0, 60, 10)
            temp_time = time(rand_hour + add_time, rand_minute)
            add_time += 3
            if (add_time + rand_hour) >= 24:
                break
            Schedule_time.objects.create(seat_count=0, string_date=str_date, start_time=temp_time,
                                         date_id_id=date_object.id, movie_id_id=movie_id)


seat_numbers = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F',
    7: 'G',
    8: 'H',
    9: 'I',
    10: 'J',
    11: 'K',
    12: 'L',
}

# def create_objects_seat(cin_name, scr_number):
def create_objects_seat():
    # 생성할 좌석의 개수
    for i in range(1, 339):
        seat_number_list = list()
        # screen_object = Screen.objects.get(cinema_id_id__cinema_name="강남", screen_number=1)
        screen_max_seat = 120
        total_number = 0
        for index, value in seat_numbers.items():
            for number_index, j in enumerate(random.sample(range(1, 13), randint(1, 12)), start=1):
                seat_number_list.append(''.join(value + str(j)))
                total_number += (index + 1)
                if total_number > screen_max_seat:  # screen_object.total_seat:
                    break
        result = ','.join(seat_number_list)
        Seat.objects.create(schedule_time_id=i, seat_number=result)
        # 현재 좌석이 A1, A11, A12, A2, A3 이런식으로 오더링에 문제 있음
        # seat_numbers의 키값을 역순으로 배열하여 가중치를 이용한 좌석 배열로 생성하는 것을 고려

"""
# Python shell을 이용한 테스트 데이터 생성
# 최상단에 file import 
import create_db_data
# 영화 및 영화 디테일 생성
create_db_data.create_objects_movie_movie_detail()
# 영화관 및 스크린 생성
create_db_data.create_objects_screen()
# 스케줄 날짜 생성(오늘을 기준으로 3일로 생성됨)
create_db_data.create_objects_date()
# 시간 생성(랜덤함수로 시간 출력)
create_db_data.create_objects_time()
# 좌석 번호 생성(랜덤함수로 좌석 지정) 
create_db_data.create_objects_seat()
# 테이블의 pk가 꼬였을 때 사용 
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='table_name';
"""
if __name__ == '__main__':
    print('a')
    print(datetime.date)
