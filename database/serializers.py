from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import Screen, Schedule_time, Schedule_date, Cinema, Region, Movie

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

class TestSerializer(serializers.ModelSerializer):
    cinema = serializers.CharField(source='date_id.screen_id.cinema_id.cinema_name') # 지점
    screen = serializers.CharField(source='date_id.screen_id.screen_number') # 상영관
    date = serializers.DateField(source='date_id.date') # 날짜
    movie = serializers.CharField(source='movie_id.title') # 영화
    type = serializers.IntegerField(source='movie_id.type')  # 타입
    type_name = TypeChoicesSerializerField()  # 타입
    total_seat = serializers.IntegerField(source='date_id.screen_id.total_seat') # 총좌석

    class Meta:
        model = Schedule_time
        fields = ('cinema', 'screen', 'date', 'start_time', 'movie', 'type', 'type_name', 'seat_count', 'total_seat')

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_type_name(self, obj):
        return TypeChoicesSerializerField().data