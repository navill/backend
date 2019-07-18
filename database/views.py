from django.db.models import Q
from .models import *

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import *


@swagger_auto_schema(method='post', request_body=QuerySerializer,
                     responses={200: ReservationFirstStepSerializer(many=True)}, operation_id='reservationFirstView',
                     operation_description="예매 첫 번째 스텝에서 사용자에게 입력 받는 변수들과 응답되는 변수들입니다.")
@swagger_auto_schema(method='get',
                     responses={200: GetReservationFirstStepSerializer(many=True)}, operation_id='reservationFirstView',
                     operation_description="예매 첫 번째 스텝에서 영화 전체 목록 출력 때 응답되는 변수들입니다.")
# manual_parameters=[theater_param, movie_title_param, date_param],
@api_view(['POST', 'GET'])
def reservationFirstView(request):
    # 극장
    theaters = request.POST.getlist('theater', None)
    # 영화 타이틀
    movie_title = request.POST.getlist('movie', None)
    # 상영 날짜
    date = request.POST.get('date', None)

    # get 형식이라면~
    if request.method == "GET":
        movie = Movie.objects.all()
        serializer = GetReservationFirstStepSerializer(movie, many=True)

    # post 형식이라면~
    elif request.method == "POST":
        my_filter_qs = Q()
        for theater in theaters:
            my_filter_qs = my_filter_qs | Q(date_id__screen_id__cinema_id__cinema_name=theater)
        movie_schedules = Schedule_time.objects.filter(my_filter_qs, date_id__date__gte=date)

        # 영화를 선택했다면
        if movie_title:
            my_filter_qs = Q()
            for movie in movie_title:
                my_filter_qs = my_filter_qs | Q(movie_id__title=movie)

            queryset = movie_schedules.filter(my_filter_qs, date_id__date__gte=date).select_related(
                'schedule_time_seat')
            for i in queryset:
                e = queryset.select_related('schedule_time_seat').get(id=i.id)
                e.seat_count = len(str(e.schedule_time_seat.seat_number).split(','))
                # 아래의 함수는 사용자가 좌석을 입력했을 때 실행해야한다.
                e.numbering_seat_count(e.seat_count)
                e.save()

                print(e.id, e.movie_id, e.start_time, e.date_id_id, e.movie_id_id, "seat count:", e.seat_count,
                      e.schedule_time_seat.seat_number)

            serializer = ReservationFirstStepSerializer(queryset, many=True)
        else:
            serializer = ReservationFirstStepSerializer(movie_schedules, many=True)

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=ReservationSecondStepSerializer,
                     responses={200: Return_200, 404: Return_404}, operation_id='reservationSecondView',
                     operation_description="예매 두 번째 스텝에서 좌석 및 선택한 영화의 정보들을 서버에 넘길 변수들입니다.", )
@api_view(['POST'])
def reservationSecondView(request):
    # 사용자가 관람할(선택한) 영화의 스케줄 id
    schedule_id = request.POST.get('schedule_id', None)
    # 예매된 좌석 번호(배열)
    seat_number = request.POST.get('seat_number', None)
    # 영화의 가격
    price = request.POST.get('price', None)
    # 예매된 좌석 수
    st_count = request.POST.get('st_count', None)

    # db에 있는지 여부 + 기존의 st_count에 post된 좌석 추가
    #
    if request.method == "POST":
        pass
