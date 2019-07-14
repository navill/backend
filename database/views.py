from django.shortcuts import render
from django.db.models import Q
from .models import *

"""
0708_jh
* 현재 작성된 코드는 단계적으로 테스트하기 위해 기능이 단계별로 분리된 상태
-> 추가적으로 검색이나 필터링이 요구될 경우 filter(query) 함수를 수정하거나 추가하여 구현할 수 있음
-> 기능의 구현 및 큰 틀이 완성 될 경우, 분리된 코드를 병합하거나 더 나은 기능의 구조로 변경할 필요가 있음

* GET는 POST로 변경 될 수 있음
"""


# Create your views here.

# main query(3번)가 동작하기 전까지 사용자가 입력 : 지역, 극장, 영화(선택)
def index(request):
    # today = DateFormat(datetime.now()).format('YYYY-MM-DD')
    # test variable - 사용자가 선택 했다는 가정(7월 5일, 광주 지역)
    today = '2019-07-05'
    region = '광주'  # 서울, 제주
    user_select_cinema = 0  # 충장로(index:0)

    # 1. 모든 지역 출력 및 사용자가 선택
    # region = Region.objects.all()
    # GET['user_select_region'] from client
    # selected_region = Region.objects.filter(name=user_select_region)  # 지역 선택
    # 테스트를 위해 사용된 아래의 region은 selected_region과 동일하다고 생각하면 됨

    # 2. 해당 지역의 모든 영화관 출력(사용자가 지역을 선택하였을 경우 -> 극장, 영화, 스크린, 상영 일정 출력)
    cinema_from_region = Cinema.objects.filter(region_id__name=region)  # -> 지역에 해당하는 모든 극장
    # GET['user_select_cinema'] from client
    # target_cinema = cinema_from_region.filter(cinema_name=user_select_cinema)
    # 테스트를 위해 사용된 cinema_from_region[user_select_cinema]는 target_cinema와 동일하다고 생각하면 됨
    print(f'선택된 영화관 - {cinema_from_region[user_select_cinema]}')  # -> test: 극장 선택(충장점)

    # 2-1. 만일 사용자가 영화를 선택 할 경우
    movie = Movie.objects.all()  # -> megabox에서 상영중인 모든 영화 출력
    # GET['user_select_movie'] from client
    # selected_movie = Moive.objects.filter(title=user_select_movie)
    selected_movie = movie[0].title  # -> test : 한 개의 영화 선택(알라딘)

    # 3. 1,2번으로부터 전달받은 값을 이용해 영화 일정 출력 - main query 동작
    # 위에서 선택된 1.region(지역) 및 2.cinema(영화관)을 바탕으로 현재 극장에서 상영중인 모든 영화 출력
    movie_schedules = Schedule_time.objects.filter(
        date_id__date__gte=today, date_id__screen_id__cinema_id__cinema_name=cinema_from_region[user_select_cinema])

    # 3-1. 영화가 선택된 경우 -> 위 queryset(movie_schedules)에 영화 제목에 대한 filter(movie.title)를 적용한다.
    if selected_movie:
        movie_schedules_with_movie = movie_schedules.filter(movie_id__title=selected_movie)
        for movie_schedule in movie_schedules_with_movie:
            print(movie_schedule)
    # 3-2. 영화 선택이 없을 경우 -> 해당 극장의 모든 영화 및 일정 출력
    else:
        for movie_schedule in movie_schedules:
            print(movie_schedule)

    # 4. 사용자가 출력된 일정 및 시간 중 원하는 항목을 선택한다.
    # GET['select_movie_with_schedule'] from client

    # 5. 좌석 배정
    # GET['select_seat_number'] from client

    # 지점 : date_id.screen_id.cinema_id.cinema_name (pass)
    # 상영관 : date_id.screen_id.screen_number
    # 상영일 : date_id.date (pass = today를 기준)
    # 상영 시간 : start_time
    # 영화 movie_id.title

    return render(request, 'database/index.html')


############################################################################################################################################

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import Screen


class RegionCreateView(generics.CreateAPIView):
    serializer_class = RegionSerializer
    permission_classes = (AllowAny,)


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    search_fields = ('name', 'value')


class RegionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # 권한을 작성자, 관리자에 부여


############################################################################################################################################

class CinemaCreateView(generics.CreateAPIView):
    serializer_class = CinemaSerializer
    permission_classes = (AllowAny,)


class CinemaListView(generics.ListAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    search_fields = ('cinema_name',)


class CinemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # 권한을 작성자, 관리자에 부여


############################################################################################################################################

class ScreenCreateView(generics.CreateAPIView):
    serializer_class = ScreenSerializer
    permission_classes = (AllowAny,)


class ScreenListView(generics.ListAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer
    search_fields = ('cinema_id__cinemaname',)


class ScreenDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer
    renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # 권한을 작성자, 관리자에 부여


############################################################################################################################################

class Schedule_timeCreateView(generics.CreateAPIView):
    serializer_class = Schedule_timeSerializer
    permission_classes = (AllowAny,)


class Schedule_timeListView(generics.ListAPIView):
    queryset = Schedule_time.objects.all()
    serializer_class = Schedule_timeSerializer
    search_fields = ('movie_id__title',)


class Schedule_timeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule_time.objects.all()
    serializer_class = Schedule_timeSerializer
    renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # 권한을 작성자, 관리자에 부여


############################################################################################################################################

class Schedule_dateCreateView(generics.CreateAPIView):
    serializer_class = Schedule_dateSerializer
    permission_classes = (AllowAny,)


class Schedule_dateListView(generics.ListAPIView):
    queryset = Schedule_date.objects.all()
    serializer_class = Schedule_dateSerializer
    search_fields = ('screen_id__cinema_id',)


class Schedule_dateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule_date.objects.all()
    serializer_class = Schedule_dateSerializer
    renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # 권한을 작성자, 관리자에 부여


############################################################################################################################################

class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (AllowAny,)


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    search_fields = ('title',)


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # 권한을 작성자, 관리자에 부여


############################################################################################################################################

theater_param = openapi.Parameter('theater', openapi.IN_QUERY, description="극장을 입력받는 파라미터~", type=openapi.TYPE_ARRAY,
                                  items=openapi.Items(type=openapi.TYPE_STRING), required=True, )
movie_title_param = openapi.Parameter('movie_title', openapi.IN_QUERY, description="영화를 입력받는 파라미터~",
                                      type=openapi.TYPE_ARRAY,
                                      items=openapi.Items(type=openapi.TYPE_STRING), required=False, )


# date_param = openapi.Parameter('date', openapi.IN_QUERY, description="날짜를 입력받는 파라미터~", type=openapi.TYPE_STRING, required=True, )
@swagger_auto_schema(method='post', manual_parameters=[theater_param, movie_title_param],
                     responses={200: TestSerializer(many=True)}, operation_description="안녕? 나는 설명이라고해")
# manual_parameters=[theater_param, movie_title_param, date_param],
@api_view(['POST'])
def testDetailView(request):
    # 임시 json 데이터
    receive_from_client = {
        'region': '서울',
        'theaters': ['강남', '동대문'],
        'movie_title': ['알라딘', '토이스토리4', '존윅3']
    }
    region = request.POST.get('region', None)  # 지역
    theaters = request.POST.getlist('theater', None)  # 극장
    movie_title = request.POST.getlist('movie_title', None)  # 영화 타이틀
    date = request.POST.get('date', '2019-07-11')  # 상영 날짜

    # today = datetime.date.today()
    # end_day = datetime.date(today.year, today.month, today.day + 3)  # 오늘로부터 3일 까지
    # today = str(today)
    # end_day = str(end_day)
    # theaters = receive_from_client['theaters']  # type-list(str)
    # movie_title = receive_from_client['movie_title']  # type-list(str)

    # post 형식이라면~
    if request.method == "POST":
        my_filter_qs = Q()
        for theater in theaters:
            my_filter_qs = my_filter_qs | Q(date_id__screen_id__cinema_id__cinema_name=theater)
        # movie_schedules = Schedule_time.objects.filter(my_filter_qs, date_id__date__gte=today, date_id__date__lte=end_day)
        movie_schedules = Schedule_time.objects.filter(my_filter_qs, date_id__date__gte=date)
        # print(movie_schedules.values())
        # print(movie_schedules.schedule_time_seat.all())
        # test1 = Schedule_time.objects.all()
        # test2 = Seat.objects.get(schedule_time_id=test1)
        # test_result = movie_schedules.schedule_time
        for i in Schedule_time.schedule_time_seat.get_queryset():
            print(type(i), i.pk)
            print(i.seat_number)



        # movie_schedules.seat_set(id=user1.id).title
        # 영화를 선택했다면~
        if movie_title:
            my_filter_qs = Q()
            for movie in movie_title:
                my_filter_qs = my_filter_qs | Q(movie_id__title=movie)

            queryset = movie_schedules.filter(my_filter_qs, date_id__date__gte=date, )

            # seat_queryset = Seat.objects.filter(schedule_time_id=)
            serializer = TestSerializer(queryset, many=True)
        else:
            serializer = TestSerializer(movie_schedules, many=True)

    return Response(serializer.data)
