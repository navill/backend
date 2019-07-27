from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from accounts.models import User
from .models import *

#
# class RegionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Region
#         fields = '__all__'

from rest_framework.fields import ListField


class StringArrayField(ListField):
    """
    String representation of an array field.
    """
    def to_representation(self, obj):
        myStr = str(obj).replace(', ', ',')
        myList = myStr.split(",")
        return myList

    # def to_internal_value(self, data):
    #     data = data.split(",")  # convert string to list
    #     return super().to_internal_value(self, data)


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


# MultipleChoiceField 출력시 value 값을 배열로 출력
class TypeChoicesSerializerField(serializers.SerializerMethodField):
    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        get_type_display = str('get_type_display'.format(field_name=self.field_name))
        # retrieve instance method
        method = getattr(value, get_type_display)
        # finally use instance method to return result of get_XXXX_display()
        list_ = method().replace(', ',',').split(',')
        temp_list = list()
        if ('자막' or '더빙') in list_:
            for i in range(0, len(list_), 2):
                temp_list.append(list_[i:i + 2])
            # type_result = ','.join(list[0])
            # print(type_result)
        else:
            for i in range(0, len(list_)):
                temp_list.append(list_[i:i+1])
        return temp_list


class GetReservationFirstStepSerializer(serializers.HyperlinkedModelSerializer):
    movie_id = serializers.IntegerField(source='id')  # 영화 id
    age = serializers.ChoiceField(choices=AGE_RATE,
                                  help_text='0: 전체 관람, 1: 12세 관람가, 2: 15세 관람가, 3: 청소년 관람불가')
    # type = StringArrayField(source='get_type_display')  # 타입
    # type = serializers.MultipleChoiceField(choices=TYPE,
    #                                        help_text='0: 2D, 1: 3D, 2: 4D, 3: Digital')
    type = TypeChoicesSerializerField(source='type')
    selected = serializers.BooleanField(default=False)

    class Meta:
        model = Movie
        fields = ('movie_id', 'img_url', 'release_date', 'booking_rate', 'title', 'age', 'type', 'selected')

    def get_type(self, obj):
        return obj

    # type_ = serializers.MultipleChoiceField(choices=TYPE)  # 타입

class StartTimeSerializerField(serializers.SerializerMethodField):
    def to_representation(self, obj):
        time = None
        try:
            time = obj.start_time.strftime('%H:%M')
        except AttributeError:
            time = obj.show_time.strftime('%H:%M')
        finally:
            return time

class ReservationFirstStepSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='id')  # 사용자가 관람할(선택한) 영화의 스케줄 id
    theater = serializers.CharField(source='date_id.screen_id.cinema_id.cinema_name')  # 지점
    screen = serializers.IntegerField(source='date_id.screen_id.screen_number')  # 상영관
    # date = serializers.DateField(source='date_id.date')  # 날짜
    date = serializers.CharField(source='string_date')  # 2019 11 1 vs 2019 1 12
    show_time = StartTimeSerializerField(source='start_time')  # 상영 시간
    movie = serializers.CharField(source='movie_id.title')  # 영화
    type = TypeChoicesSerializerField(source='type')  # 타입
    total_seat = serializers.IntegerField(source='date_id.screen_id.total_seat')  # 총좌석 수
    st_count = serializers.IntegerField(source='seat_count')  # 예매된 좌석 수
    seat_number = StringArrayField(source='schedule_time_seat.seat_number')  # 예매된 좌석 번호(배열)
    age = serializers.CharField(source='get_age_display')  # 영화 연령 제한

    class Meta:
        model = Schedule_time
        fields = (
            'schedule_id', 'theater', 'screen', 'date', 'start_time', 'movie', 'type',
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

class BookingHistorySerializer(serializers.ModelSerializer):
    img_url = serializers.CharField(source='schedule_id.movie_id.img_url')  # 포스터 이미지
    title = serializers.CharField(source='schedule_id.movie_id.title')  # 영화 타이틀
    theater = serializers.CharField(source='schedule_id.date_id.screen_id.cinema_id.cinema_name')  # 지점
    screen_number = serializers.IntegerField(source='schedule_id.date_id.screen_id.screen_number')  # 상영관 번호
    show_date = serializers.DateField(source='schedule_id.date_id.date')  # 상영 일시
    show_time = StartTimeSerializerField(source='schedule_id.start_time')  # 상영 시간

    class Meta:
        model = BookingHistory
        fields = ('booking_number', 'title', 'img_url', 'theater', 'screen_number', 'show_date', 'show_time',
                  'booking_date')


class Return_200(serializers.Serializer):
    status = serializers.CharField(allow_blank=True, required=False, default='ok')


class Return_404(serializers.Serializer):
    error = serializers.CharField(allow_blank=True, required=False, default='404 Not Found')


class Return_error(serializers.Serializer):
    error = serializers.CharField(allow_blank=True, required=False, default='필요한 요청이 충분하지 않습니다.')
