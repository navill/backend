from django.shortcuts import render
from django.db.models import Q
from .models import *


# Create your views here.
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
    theaters = request.POST.getlist('theater', None)  # 극장
    movie_title = request.POST.getlist('movie_title', None)  # 영화 타이틀
    date = request.POST.get('date', None)  # 상영 날짜

    # post 형식이라면~
    if request.method == "POST":
        my_filter_qs = Q()
        for theater in theaters:
            my_filter_qs = my_filter_qs | Q(date_id__screen_id__cinema_id__cinema_name=theater)
        movie_schedules = Schedule_time.objects.filter(my_filter_qs, date_id__date__gte=date)
        # movie_schedules.numbering_seat_count()
        # print(dir(movie_schedules))
        # 영화를 선택했다면~
        if movie_title:
            my_filter_qs = Q()
            for movie in movie_title:
                my_filter_qs = my_filter_qs | Q(movie_id__title=movie)

            queryset = movie_schedules.filter(my_filter_qs, date_id__date__gte=date).select_related(
                'schedule_time_seat')
            print(queryset.values('id'))
            for i in queryset:
                e = queryset.select_related('schedule_time_seat').get(id=i.id)
                e.seat_count = len(str(e.schedule_time_seat.seat_number).split(','))
                # 아래의 함수는 사용자가 좌석을 입력했을 때 실행해야한다.
                # e.numbering_seat_count(seat_count)
                print(e.id, e.movie_id, e.start_time, e.date_id_id, e.movie_id_id, "seat count:", e.seat_count,
                      e.schedule_time_seat.seat_number)
            serializer = TestSerializer(queryset, many=True)
        else:
            serializer = TestSerializer(movie_schedules, many=True)

    return Response(serializer.data)
