import random
import string
import time
from datetime import datetime

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *


# @swagger_auto_schema(method='get',
#                      responses={200: ReservationFirstStepSerializer(many=True)},
#                      operation_id='reservationFirstView',
#                      operation_description="예매 첫 번째 스텝에서 영화 전체 목록 출력 때 응답되는 변수들입니다.")
# # manual_parameters=[theater_param, movie_title_param, date_param],
# @api_view(['GET'])
# def reservationFirstView(request):
#     # 극장
#     theater_list = request.GET.get('theater', None)  # list type
#     # 영화 타이틀
#     movie_title = request.GET.get('movie', None)  # list type
#     # 상영 날짜
#     date = request.GET.get('date', None)  # -> 2019-07-06
#
#     # 쿼리 하나에 값을 3개를 초과해서 받지 않음.
#     # 3개 이상 입력 받을 시 에러를 반환
#     if (theater_list != None and theater_list.count('_') > 2) or (movie_title != None and movie_title.count('_') > 2) :
#         serializer = Return_error('1')
#         return Response(serializer.data)
#
#     # get 형식이라면~
#     if theater_list and date:  # get_queryset에 세 가지 중 두 가지(theater, date) 있을 경우
#         theaters = theater_list.split('_')
#         my_filter_qs = Q()
#         for theater in theaters:
#             my_filter_qs = my_filter_qs | Q(date_id__screen_id__cinema_id__cinema_name=theater)
#         movie_schedules = Schedule_time.objects.filter(my_filter_qs, date_id__date=date).order_by('date',
#                                                                                                        'start_time')  # 날짜, 시간 순으로 정렬
#         # movie_schedules = Schedule_time.objects.filter(date_id__screen_id__cinema_id__cinema_name=theater, date_id__date__gte=date).order_by('string_date',                                                                                  'start_time')
#
#         # 영화를 선택했다면
#         if movie_title:  # get_queryset에 영화가 포함되어 있을 경우(세 변수 모두 포함) -> 극장에서 상영중인 영화 리스트 출력
#             movie_title = movie_title.split('_')
#             my_filter_qs = Q()
#             for movie in movie_title:
#                 my_filter_qs = my_filter_qs | Q(movie_id__title=movie)
#
#             queryset = movie_schedules.filter(my_filter_qs, date_id__date=date).select_related(
#                 'schedule_time_seat')
#             for i in queryset:
#                 e = queryset.select_related('schedule_time_seat').get(id=i.id)
#                 e.seat_count = len(str(e.schedule_time_seat.seat_number).split(','))
#                 # 아래의 함수는 사용자가 좌석을 입력했을 때 실행해야한다.
#                 e.numbering_seat_count(e.seat_count)
#                 e.save()
#                 # print(e.id, e.movie_id, e.start_time, e.date_id_id, e.movie_id_id, "seat count:", e.seat_count,
#                 #       e.schedule_time_seat.seat_number)
#             serializer = ReservationFirstStepSerializer(queryset, many=True)
#             return Response(serializer.data)
#         else:
#             serializer = ReservationFirstStepSerializer(movie_schedules, many=True)
#             return Response(serializer.data)
#
#     # elif movie_title:  # GET query_set이 없을 경우 : 모든 영화 리스트 출력
#     if not (theater_list or movie_title or date):
#         movie = Movie.objects.all().order_by('-booking_rate')  # 예매율 순으로 정렬됨
#         serializer = GetReservationFirstStepSerializer(movie, many=True)
#         return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: ShowMoviesSerializer(many=True)},
                     operation_id='showMovies',
                     operation_description="예매 첫 번째 스텝에서 영화 목록 정보를 리턴합니다.")
@api_view(['GET'])
def showMoviesView(request):
    movie = Movie.objects.all().order_by('-booking_rate')  # 예매율 순으로 정렬됨
    serializer = ShowMoviesSerializer(movie, many=True, context={'request': request})
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: MovieDetailSerializer()},
                     operation_id='movieDetail',
                     operation_description="영화 포스터를 클릭하면 나오는 영화 디테일 정보입니다")
@api_view(['GET'])
def movie_detail_view(request):
    movie_detail_id = request.GET.get('movie')  # 영화 id를 받음
    queryset = Movie_detail.objects.get(pk=movie_detail_id)
    serializer = MovieDetailSerializer(queryset, context={'request': request})

    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: ReservationScheduleListSerializer(many=True)},
                     query_serializer=QuerySerializer,
                     operation_id='reservationScheduleList',
                     operation_description="예매 첫 번째 스텝에서 영화 스케줄 목록 정보를 리턴합니다.")
@api_view(['GET'])
def reservationScheduleListView(request):
    movie_schedules = Schedule_time.objects.none()
    # 극장
    theaters = request.GET.getlist('theater')  # list type
    # 영화 타이틀
    movie_title = request.GET.getlist('movie')  # list type
    # 상영 날짜
    date = request.GET.get('date')  # -> 2019-07-06

    # 쿼리 하나에 값을 3개를 초과해서 받지 않음.
    # 3개 초과 입력 받을 시 에러를 반환
    if (len(theaters) > 3) or (len(movie_title) > 3):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    today = datetime.today().strftime('%Y-%m-%d')  # 오늘 날짜
    time = datetime.now().strftime('%H:%M')  # 현재 시간
    # get 형식이라면~
    if theaters and date:  # get_queryset에 세 가지 중 두 가지(theater, date) 있을 경우
        for theater in theaters:
            query = Q(
                date_id__screen_id__cinema_id__cinema_name=theater,
                date_id__date=date)
            if today == date:
                query &= Q(start_time__gte=time)  # 현재 시간 이후의 스케줄 필터링

            movie_schedules |= Schedule_time.objects.filter(
                query
            ).order_by('date', 'start_time')  # 날짜, 시간 순으로 정렬

        # movie_schedules = Schedule_time.objects.filter(date_id__screen_id__cinema_id__cinema_name=theater, date_id__date__gte=date).order_by('string_date',                                                                                  'start_time')
        # 영화를 선택했다면
        if movie_title:  # get_queryset에 영화가 포함되어 있을 경우(세 변수 모두 포함) -> 극장에서 상영중인 영화 리스트 출력
            my_filter_qs = Q()
            for movie in movie_title:
                my_filter_qs |= Q(movie_id__title=movie)

            queryset = movie_schedules.filter(my_filter_qs, date_id__date=date).select_related('schedule_time_seat')
            for i in queryset:
                e = queryset.select_related('schedule_time_seat').get(id=i.id)
                e.seat_count = len(str(e.schedule_time_seat.seat_number).split(','))
                # 아래의 함수는 사용자가 좌석을 입력했을 때 실행해야한다.
                # e.numbering_seat_count(e.seat_count)
                # e.save()
                # print(e.id, e.movie_id, e.start_time, e.date_id_id, e.movie_id_id, "seat count:", e.seat_count,
                #       e.schedule_time_seat.seat_number)
            serializer = ReservationScheduleListSerializer(queryset, many=True)
        else:
            serializer = ReservationScheduleListSerializer(movie_schedules, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post',
                     request_body=ReservationSecondStepSerializer,
                     responses={200: Return_200}, operation_id='reservationSecond',
                     operation_description="예매 두 번째 스텝에서 좌석 및 선택한 영화의 정보들을 서버에 넘길 변수들입니다.", )
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reservationSecondView(request):
    # 사용자가 관람할(선택한) 영화의 스케줄 id
    booking_data = request.data
    # print(booking_data)
    # print(booking_data['schedule_id'])
    # print(booking_data['seat_number'])
    # print(booking_data['price'])
    # print(booking_data['st_count'])

    if not booking_data['schedule_id']:
        serializer = Return_error(1)
        return Response(serializer.data)

    # db에 있는지 여부 + 기존의 st_count에 post된 좌석 추가
    # 아래의 코드는 Post.get(st_count)를 사용하지 않음 -> 기존 seat_number의 배열 수로 계산해서 처리함
    if request.method == "POST":
        selected_schedule = Schedule_time.objects.get(
            id=booking_data[
                'schedule_id'])  # .update(seat_number=seat_number, schedule_time_seat__seat_number=seat_number)
        # 예약 되어있는 좌석 리스트
        booked_seat_numbers = selected_schedule.schedule_time_seat.seat_number
        # print('booked_seat_numbers:', booked_seat_numbers)
        # seat_number, booked_list.split() : 클라이언트로부터 넘어온 str data -> list data로 변환
        if booked_seat_numbers:
            booked_list = booked_seat_numbers.split(',')
        else:
            booked_list = list()
        # print("booking_data['seat_number']:", booking_data['seat_number'])
        if booking_data['seat_number']:
            for seat in booking_data['seat_number']:
                if seat not in booked_list:
                    booked_list.append(seat)
            booked_list.sort()
            # 좌석 list -> string 좌석 list로 변환
            update_seat = ','.join(booked_list)
            # update된 좌석 수
            st_count = len(booked_list)
            # update된 좌석 번호
            selected_schedule.schedule_time_seat.seat_number = update_seat

            selected_schedule.numbering_seat_count(st_count)
            # save Schedule_time
            selected_schedule.save()
            # save Seat table
            selected_schedule.schedule_time_seat.save()
            seat_numbers = ','.join(booking_data['seat_number'])
            bookingHistory(request, selected_schedule, seat_numbers, booking_data['price'])  # 예매 내역에 저장

            serializer = Return_200(selected_schedule)
            # print(booked_seat_numbers)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = Return_error(selected_schedule)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


def bookingHistory(request, selected_schedule, seat_numbers, total_price):
    # def booking_history
    booking_number = random_booking_number()

    BookingHistory.objects.create(
        booking_number=booking_number,
        user=request.user,
        schedule_id=selected_schedule,
        seat_number=seat_numbers,
        total_price=total_price
    )


def random_booking_number():
    booking_number = ''
    alphabets = string.ascii_letters

    for i in range(0, 19):
        num = int(random.randrange(1, 10))
        if i == 4 or i == 9 or i == 14:
            booking_number += '-'
        elif num % 2 == 0:
            booking_number += random.choice(alphabets)
        elif num % 2 == 1:
            booking_number += str(int(random.randrange(1, 10) * time.time() / 3.5 + 1))[1]

    return booking_number


@swagger_auto_schema(method='post',
                     responses={200: CheckWishMovieSerializer()},
                     operation_id='checkWishMovie',
                     operation_description="영화를 보고싶어 목록에 추가합니다.")
@api_view(['POST'])
def check_wishmovies_view(request):
    # get = 'movie_id'
    # a = request.query_params['movie_id']
    serializer = CheckWishMovieSerializer(request)
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: ShowWishMoviesInfoSerializer()},
                     operation_id='showWishMoviesInfo',
                     operation_description="보고싶어를 누른 영화 정보를 출력합니다.")
@api_view(['GET'])
def show_wish_movies_info_view(request):
    wishMovies = request.user.wish_movie.all()
    serializer = ShowWishMoviesInfoSerializer(wishMovies, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: ShowRegionSerializer()},
                     operation_id='showRegion',
                     operation_description="지역 정보를 출력합니다.")
@api_view(['GET'])
def show_region_view(request):  # 지역-상영관 정보를 출력하는 뷰
    regions = Region.objects.all()  # 지역의 모든 정보를 가져옴.
    theaterList = list()  # 모든 상영관의 정보를 저장할 리스트.
    queryset = list()  # serializer에 넘길 인덱스와 상영관이 딕셔너리로 저장된 리스트.

    for region in regions:
        theaters = Region.objects.get(name=region).region_id.all()  # 지역에 해당하는 모든 상영관을 가져옴.
        for theater in theaters:
            theaterList.append(theater)  # 상영관 하나씩 리스트에 추가.

    # queryset 리스트에 딕셔너리 형태로 인덱스가 포함된 상영관 하나씩 넣음.
    # QuerySets in Django are actually generators, not lists(https://docs.djangoproject.com/en/dev/ref/models/querysets/#ref-models-querysets)
    # 위를 근거하여 serializer에서 하나의 쿼리당 index 값을 불러올 수 없어서 아래처럼 직접 index 값을 생성하여 넘겨줌.
    for index, item in enumerate(theaterList):
        queryset.append({'index': index, 'item': item})

    serializer = ShowRegionSerializer(queryset, many=True)
    return Response(serializer.data)

#
# def show_star_rate(reqeust):
#     return Response(0)
#
