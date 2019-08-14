from datetime import *
from random import *
import random
from database.models import *

# import create_db_data
age = {
    0: '전체 관람가',
    1: '12세 관람가',
    2: '15세 관람가',
    3: '19세 관람가',
    4: '미정'
}
type_ = {
    0: '디지털',
    1: '3D',
    2: '4D',
    3: 'ATMOS',
    4: '자막',
    5: '더빙'
    # 4: '디지털(자막)',
    # 5: '3D(자막)',
    # 6: '4D(자막)',
    # 7: 'ATMOS(자막)',
    # 8: 'Digital(더빙)',
    # 9: '3D(더빙)',
    # 10: '4D(더빙)',
    # 11: 'ATMOS(더빙)'
}

# 0/4, 0/5
# [
#   [디지털,자막],
#   [디지털,더빙],
# ]

data = [
    {
        "id": 1,
        "title": "스파이더맨: 파프 롬 홈",
        "age": 1,
        "booking_rate": 9.5,
        "type": "0,4,3,4,1,4",
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
        "type": "0,4,3,4,0,5,1,4,1,5",
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
        "type": "0,4,3,4,0,4,1,4,1,5",
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
        "type": "0,4,0,5,1,4,1,5,3,4",
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
        "type": "0,3",
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
        "type": "0,4",
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
        "type": "0",
        "release_date": "2019-07-10",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/89/E48867-C962-41A8-A796-63544421A8A7.large.jpg',
        "director": "남대중",
        "cast": "이준호, 정소민, 최귀화, 예지원, 공명",
        "genre": "/",
        "running_time": 110,
        "description": " ",
    },
    {
        "id": 8,
        "title": "47미터 2",
        "age": 4,
        "booking_rate": 0.0,
        "type": "0,4",
        "release_date": "2019-08-28",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/9D/329586-077A-4B78-B651-AB0F625FB9C1.large.jpg',
        "director": "요하네스 로버츠",
        "cast": "시스틴 로즈 스탤론, 소피 넬리스",
        "genre": "스릴러, 공포(호러)",
        "running_time": 0,
        "description": " ",
    },
    {
        "id": 9,
        "title": "동키 킹",
        "age": 4,
        "booking_rate": 0.0,
        "type": "0,4",
        "release_date": "2019-08-28",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/06/CF86A0-8311-4D9A-8302-BBD7CBEDEE85.large.jpg',
        "director": "",
        "cast": "",
        "genre": "애니메이션",
        "running_time": 85,
        "description": "",
    },
    {
        "id": 10,
        "title": "유열의 음악앨범",
        "age": 1,
        "booking_rate": 0.0,
        "type": "0,4",
        "release_date": "2019-08-28",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/FA/9B72EE-C684-478F-9FF6-FA9DD99C4673.large.jpg',
        "director": "정지우",
        "cast": "김고은, 정해인",
        "genre": "멜로, 로맨스",
        "running_time": 122,
        "description": " ",
    },
    {
        "id": 11,
        "title": "인비저블 위트니스",
        "age": 2,
        "booking_rate": 0.0,
        "type": "0,4",
        "release_date": "2019-08-28",
        "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/1E/28B5B0-7E2E-410C-820D-908BBBA3B90C.large.jpg',
        "director": "스테파노 모르디니",
        "cast": "리카르도 스카마르치오, 파브리지오 벤티보글리오",
        "genre": "스릴러",
        "running_time": 102,
        "description": " ",
    }
    # # 추가 영화
    # {
    #     "id": 8,
    #     "title": "나랏말싸미",
    #     "age": 0,
    #     "booking_rate": 0.8,
    #     "type": "0",
    #     "release_date": "2019-07-24",
    #     "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/F5/A1A99E-025A-4874-B479-1597994D94A8.large.jpg',
    #     "director": "조철현",
    #     "cast": "송강호, 박해일, 전미선",
    #     "genre": "드라마",
    #     "running_time": 109,
    #     "description": " ",
    # },
    # {
    #     "id": 9,
    #     "title": "기방도령",
    #     "age": 2,
    #     "booking_rate": 0.4,
    #     "type": "0",
    #     "release_date": "2019-07-10",
    #     "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/89/E48867-C962-41A8-A796-63544421A8A7.large.jpg',
    #     "director": "남대중",
    #     "cast": "이준호, 정소민, 최귀화, 예지원, 공명",
    #     "genre": "/",
    #     "running_time": 110,
    #     "description": " ",
    # },
    # {
    #     "id": 10,
    #     "title": "기방도령",
    #     "age": 2,
    #     "booking_rate": 0.4,
    #     "type": "0",
    #     "release_date": "2019-07-10",
    #     "img_url": 'http://image2.megabox.co.kr/mop/poster/2019/89/E48867-C962-41A8-A796-63544421A8A7.large.jpg',
    #     "director": "남대중",
    #     "cast": "이준호, 정소민, 최귀화, 예지원, 공명",
    #     "genre": "/",
    #     "running_time": 110,
    #     "description": " ",
    # },
    # 상영 예정작(8월 23일 기준)
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


def create_region():
    region_list = ['서울', '경기', '부산/대구/경상']
    for i in region_list:
        Region.objects.create(name=i)


# Movie & Movie_detail 객체 생성
def create_objects_movie_movie_detail():
    for index, _ in enumerate(data):
        # print(index, movie_data)
        Movie.objects.create(title=data[index]['title'],
                             age=data[index]['age'],
                             type=data[index]['type'],
                             booking_rate=data[index]['booking_rate'],
                             release_date=data[index]['release_date'],
                             img_url=data[index]['img_url'])
        Movie_detail.objects.create(movie_id=data[index]['id'], director=data[index]['director'],
                                    cast=data[index]['cast'], genre=data[index]['genre'],
                                    running_time=data[index]['running_time'])
    return 1


# Screen 객체 생성
# fields : screen_number, total_seat, cinema_id_id
def create_objects_screen():
    total_seat = [36, 82, 150, 140, 130]
    random.shuffle(total_seat)
    cinema = [{1: '강남'}, {1: '신촌'}, {1: '코엑스'}, {2: '고양스타필드'}, {3: '해운대(장산)'}]
    for i, value_ in enumerate(cinema):
        region_id, cinema_name = value_.popitem()
        Cinema.objects.create(cinema_name=cinema_name, region_id=region_id)
        # for i in range(1, 6):
        for j in range(1, 6):
            random.shuffle(total_seat)
            # id_number = i + j
            Screen.objects.create(screen_number=j, total_seat=total_seat[0], cinema_id_id=i + 1)
    return 1


# date 객체 생성
# fields : date, screen_id_id
def create_objects_date():
    screen_objects = Screen.objects.all().order_by('id')
    for index, screen_object in enumerate(screen_objects, start=1):
        newDay = 1
        for i in range(0, 5):
            try:
                temp_date = datetime.today().replace(day=datetime.today().day + i).date()
            except ValueError:
                temp_date = datetime.today().replace(month=datetime.today().month + 1, day=newDay).date()
                newDay += 1
            finally:
                Schedule_date.objects.create(date=temp_date, screen_id_id=index)
    return 1


# fields : seat_count, start_time, string_date, date_id_id, movie_id_id
def create_objects_time():
    date_objects = Schedule_date.objects.all().order_by('id')
    for index, date_object in enumerate(date_objects, start=1):
        date = date_object.date
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
            movie_object = Movie.objects.get(id=movie_id)
            type_str = movie_object.type
            # a = type_str.__dict__.items()
            key_list = list()
            type_list = list()
            for i in type_str:
                key_list.append(i)

            key_list = list(map(str, key_list))
            # print(key_list)
            if ('4' or '5') in key_list:
                for i in range(0, len(key_list), 2):
                    type_list.append(key_list[i:i + 2])
                random.shuffle(type_list)
                type_result = ','.join(type_list[0])
                print(type_result)
                temp = Schedule_time.objects.create(seat_count=0, date=date, start_time=temp_time,
                                             date_id_id=date_object.id, type=type_result, movie_id_id=movie_id)

                # 8일 좌석 생성을 위한 코드
                Seat.objects.create(schedule_time_id=temp.id, seat_number='')

            else:
                random.shuffle(key_list)
                type_result = str(key_list[0])
                print(type_result)
                temp = Schedule_time.objects.create(seat_count=0, date=date, start_time=temp_time,
                                             date_id_id=date_object.id, type=type_result, movie_id_id=movie_id)
                # 8일 좌석 생성을 위한 코드
                Seat.objects.create(schedule_time_id=temp.id, seat_number='')
            # type_list.append(key_list[i:i + 2])
            # random.shuffle(type_list)

    return 1
    # import create_db_data
    # create_db_data.create_objects_time()


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


def create_objects_seat():
    # screen_max_seat = [36, 82, 150, 140, 130]
    # 생성할 좌석의 개수
    scheduled_list = Schedule_time.objects.all().order_by('id')
    # print('length', len(scheduled_list))
    for i in range(1, len(scheduled_list) + 1):
        # print('len', i)
        seat_number_list = list()
        schedule_object = Schedule_time.objects.get(id=i)
        total_seat = schedule_object.date_id.screen_id.total_seat
        # random.shuffle(screen_max_seat)
        # screen_mx_seat = int(screen_max_seat[0])
        # screen_object = Screen.objects.get(cinema_id_id__cinema_name="강남", screen_number=1)
        for index, value in seat_numbers.items():
            for number_index, j in enumerate(random.sample(range(1, 9), randint(1, 8)), start=1):
                if len(seat_number_list) >= total_seat:  # screen_object.total_seat:
                    break
                else:
                    seat_number_list.append(''.join(value + str(j)))

        result = ','.join(seat_number_list)
        # print(f"seat:{result}, seat_count:{len(seat_number_list)}, total_seat:{screen_max_seat[0]}")
        # Seat.objects.create(schedule_time_id=i, seat_number=result)

        # 8일 좌석 생성을 위한 코드
        Seat.objects.create(schedule_time_id=i, seat_number='')
        # 현재 좌석이 A1, A11, A12, A2, A3 이런식으로 오더링에 문제 있음
        # seat_numbers의 키값을 역순으로 배열하여 가중치를 이용한 좌석 배열로 생성하는 것을 고려
    return 1


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

# print('a')
# print(datetime.date)

# 영화 및 영화 디테일 생성
# create_db_data.create_objects_movie_movie_detail()
temp = True
# if temp:
#     movie_mark = create_objects_movie_movie_detail()
#     create_region()
#     if movie_mark:
#         screen_mark = create_objects_screen()
#         if screen_mark:
#             date_mark = create_objects_date()
#             if date_mark:
#                 time_mark = create_objects_time()
#                 if time_mark:
#                     create_objects_seat()

# 8월 8일 데이터 생성 코드
if temp:
    date_mark = create_objects_date()
    if date_mark:
        time_mark = create_objects_time()
        # if time_mark:
        #     create_objects_seat()




# 영화관 및 스크린 생성
# create_db_data.create_objects_screen()

# 스케줄 날짜 생성(오늘을 기준으로 3일로 생성됨)
# create_db_data.create_objects_date()
# 시간 생성(랜덤함수로 시간 출력)
# create_db_data.create_objects_time()
# 좌석 번호 생성(랜덤함수로 좌석 지정)
# create_db_data.create_objects_seat()
