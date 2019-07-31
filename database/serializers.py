from rest_framework.fields import ListField
from rest_framework import serializers

from .models import *


class StringArrayField(ListField):
    def to_representation(self, obj):
        list_ = str(obj).replace(', ', ',').split(",")
        return list_


class TypesArrayField(ListField):
    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        # get_type_display = str('get_type_display'.format(field_name=self.field_name))
        # retrieve instance method
        # method = getattr(value, 'get_type')
        # finally use instance method to return result of get_XXXX_display()
        list_ = str(value).replace(', ', ',').split(',')
        # list_ = value.get_type_display().replace(', ', ',').split(',')
        temp_list = list()
        if ('자막' or '더빙') in list_:
            for i in range(0, len(list_), 2):
                temp_list.append(list_[i:i + 2])
            # type_result = ','.join(list[0])
            # print(type_result)
        else:
            for i in range(0, len(list_)):
                temp_list.append(list_[i:i + 1])
        return temp_list


class QuerySerializer(serializers.ModelSerializer):
    theater = serializers.ListField(source='date_id.screen_id.cinema_id.cinema_name',
                                    help_text='지점을 배열 형식으로 입력 받습니다.')  # 지점
    movie = serializers.ListField(source='movie_id.title', required=False, help_text='영화 이름을 배열 형식으로 입력 받습니다.')  # 영화
    date = serializers.DateField(source='date_id.date', help_text='날짜를 입력 받습니다.')  # 날짜

    class Meta:
        model = Schedule_time
        fields = ('theater', 'movie', 'date')


class ShowMoviesSerializer(serializers.HyperlinkedModelSerializer):
    movie_id = serializers.IntegerField(source='id', help_text='영화 고유의 id 값')  # 영화 id
    age = serializers.CharField(source='get_age_display', help_text='0: 전체 관람, 1: 12세 관람가, 2: 15세 관람가, 3: 청소년 관람불가')
    # type = serializers.SerializerMethodField('type_display', help_text='0: 디지털 / 1: 3D / 2: 4D / 3: ATMOS / 4: 자막 / 5: 더빙')
    types = TypesArrayField(source='type', help_text='0: 디지털 / 1: 3D / 2: 4D / 3: ATMOS / 4: 자막 / 5: 더빙')
    selected = serializers.BooleanField(default=False, help_text='예매 모달 표시 여부에 사용되는 변수')

    class Meta:
        model = Movie
        fields = ('movie_id', 'img_url', 'release_date', 'booking_rate', 'title', 'age', 'types', 'selected')

    # type_ = serializers.MultipleChoiceField(choices=TYPE)  # 타입

    # def type_display(self, obj):
    #     # sample: 'get_XXXX_display'
    #     # get_type_display = str('get_type_display'.format(field_name=self.field_name))
    #     # retrieve instance method
    #     # method = getattr(value, 'get_type')
    #     # finally use instance method to return result of get_XXXX_display()
    #     list_ = obj.get_type_display().replace(', ', ',').split(',')
    #     # list_ = value.get_type_display().replace(', ', ',').split(',')
    #     temp_list = list()
    #     if ('자막' or '더빙') in list_:
    #         for i in range(0, len(list_), 2):
    #             temp_list.append(list_[i:i + 2])
    #         # type_result = ','.join(list[0])
    #         # print(type_result)
    #     else:
    #         for i in range(0, len(list_)):
    #             temp_list.append(list_[i:i + 1])
    #     return temp_list


class ReservationScheduleListSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='id', help_text='스케줄 고유 id 값')  # 사용자가 관람할(선택한) 영화의 스케줄 id
    theater = serializers.CharField(source='date_id.screen_id.cinema_id.cinema_name')  # 지점
    screen = serializers.IntegerField(source='date_id.screen_id.screen_number', help_text='상영관 번호')  # 상영관
    # date = serializers.DateField(source='date_id.date')  # 날짜
    date = serializers.CharField(source='date_id.date', help_text='상영 날짜, ex)2019-08-23')  # 2019 11 1 vs 2019 1 12
    start_time = serializers.SerializerMethodField('time_display', help_text='상영 시작 시간, ex)15:30')  # 상영 시간
    movie = serializers.CharField(source='movie_id.title')  # 영화
    # type = serializers.SerializerMethodField('type_display', help_text='0: 디지털 / 1: 3D / 2: 4D / 3: ATMOS / 4: 자막 / 5: 더빙')  # 타입
    types = StringArrayField(source='type', help_text='0: 디지털 / 1: 3D / 2: 4D / 3: ATMOS / 4: 자막 / 5: 더빙')  # 타입
    total_seat = serializers.IntegerField(source='date_id.screen_id.total_seat')  # 총좌석 수
    st_count = serializers.IntegerField(source='seat_count', help_text='예매된 좌석 수')  # 예매된 좌석 수
    seat_number = StringArrayField(source='schedule_time_seat.seat_number', help_text='예매된 좌석 번호')  # 예매된 좌석 번호(배열)
    age = serializers.CharField(source='get_age_display')  # 영화 연령 제한
    running_time = serializers.IntegerField(source='movie_id.movie_id_detail.running_time')  # 영화 러닝 타임, related_name으로 oneToone 불러오기

    class Meta:
        model = Schedule_time
        fields = (
            'schedule_id', 'theater', 'screen', 'age', 'running_time', 'date', 'start_time', 'movie', 'types',
            'st_count', 'total_seat', 'seat_number')

    def time_display(self, obj):
        time = None
        try:
            time = obj.start_time.strftime('%H:%M')
        except AttributeError:
            time = obj.show_time.strftime('%H:%M')
        finally:
            return time


class ReservationSecondStepSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='id', help_text='사용자가 시청할 영화 스케줄의 고유 id 값')  # 사용자가 관람할(선택한) 영화의 스케줄 id
    # seat_number = serializers.CharField(source='schedule_time_seat.seat_number', help_text='예매된 좌석 번호')  # 예매된 좌석 번호(배열)
    seat_number = StringArrayField(source='schedule_time_seat.seat_number', help_text='예매된 좌석 번호')  # 예매된 좌석 번호(배열)
    price = serializers.IntegerField(help_text='예매 최종 가격')  # 영화의 가격
    st_count = serializers.IntegerField(source='seat_count', help_text='예매된 좌석 수')  # 예매된 좌석 수

    class Meta:
        model = Schedule_time
        fields = ('schedule_id', 'seat_number', 'price', 'st_count')


class Return_200(serializers.Serializer):
    status = serializers.CharField(allow_blank=True, required=False, default='ok')


class Return_404(serializers.Serializer):
    error = serializers.CharField(allow_blank=True, required=False, default='404 Not Found')


class Return_error(serializers.Serializer):
    error = serializers.CharField(allow_blank=True, required=False, default='필요한 요청이 충분하지 않습니다.')


