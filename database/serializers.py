from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers, fields

from .models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'


class Schedule_timeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule_time
        fields = '__all__'


class Schedule_dateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule_date
        fields = '__all__'


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class TypeChoicesSerializerField(serializers.SerializerMethodField):
    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        get_type_display = str('get_type_display'.format(field_name=self.field_name))
        # retrieve instance method
        method = getattr(value, get_type_display)
        # finally use instance method to return result of get_XXXX_display()
        return method()


    # type_ = serializers.MultipleChoiceField(choices=TYPE)  # 타입



class ReservationFirstStepSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='id')  # 사용자가 관람할(선택한) 영화의 스케줄 id
    cinema = serializers.CharField(source='date_id.screen_id.cinema_id.cinema_name')  # 지점
    screen = serializers.CharField(source='date_id.screen_id.screen_number')  # 상영관
    # date = serializers.DateField(source='date_id.date')  # 날짜
    date = serializers.CharField(source='string_date')  # 2019 11 1 vs 2019 1 12
    movie = serializers.CharField(source='movie_id.title')  # 영화
    # type = serializers.IntegerField(source='movie_id.type')  # 타입

    total_seat = serializers.IntegerField(source='date_id.screen_id.total_seat')  # 총좌석 수
    st_count = serializers.IntegerField(source='seat_count')  # 예매된 좌석 수
    seat_number = serializers.CharField(source='schedule_time_seat.seat_number')  # 예매된 좌석 번호(배열)

    class Meta:
        model = Schedule_time
        fields = (
            'schedule_id', 'cinema', 'screen', 'date', 'start_time', 'movie', 'type_',
            'st_count', 'total_seat', 'seat_number')

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_type_name(self, obj):
        return TypeChoicesSerializerField().data


class QuerySerializer(serializers.ModelSerializer):
    theater = serializers.ListField(source='date_id.screen_id.cinema_id.cinema_name',
                                    help_text='지점을 배열 형식으로 입력 받습니다.')  # 지점
    movie = serializers.ListField(source='movie_id.title', required=False, help_text='영화 이름을 배열 형식으로 입력 받습니다.')  # 영화
    date = serializers.DateField(source='date_id.date', help_text='날짜를 입력 받습니다.')  # 날짜

    class Meta:
        model = Schedule_time
        fields = ('theater', 'movie', 'date')


class ReservationSecondStepSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='id')  # 사용자가 관람할(선택한) 영화의 스케줄 id
    seat_number = serializers.CharField(source='schedule_time_seat.seat_number')  # 예매된 좌석 번호(배열)
    price = serializers.IntegerField()  # 영화의 가격
    st_count = serializers.IntegerField(source='seat_count')  # 예매된 좌석 수

    class Meta:
        model = Schedule_time
        fields = ('schedule_id', 'seat_number', 'price', 'st_count')


class Return_200(serializers.Serializer):
    status = serializers.CharField(allow_blank=True, required=False, default='ok')


class Return_404(serializers.Serializer):
    error = serializers.CharField(allow_blank=True, required=False, default='404 Not Found')
