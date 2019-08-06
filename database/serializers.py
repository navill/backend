from rest_framework import serializers
from rest_framework.fields import ListField

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
        temp_list = list()
        if ('자막' or '더빙') in list_:
            for i in range(0, len(list_), 2):
                temp_list.append(list_[i:i + 2])
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
    types = TypesArrayField(source='type', help_text='0: 디지털 / 1: 3D / 2: 4D / 3: ATMOS / 4: 자막 / 5: 더빙')
    running_time = serializers.SerializerMethodField('running_time_display')
    selected = serializers.BooleanField(default=False, help_text='예매 모달 표시 여부에 사용되는 변수')
    is_wished = serializers.SerializerMethodField()

    # wish_user에 로그인 유저가 포함되어있는지 여부를 판단할 수 있는 boolean type 필드 생성
    # -> get_wish_user() 생성
    class Meta:
        model = Movie
        fields = (
            'movie_id', 'img_url', 'release_date', 'booking_rate', 'title', 'age', 'types', 'running_time', 'selected', 'is_wished')

    def get_is_wished(self, obj):
        # check_wish = obj.filter(wish_user=req_user)
        # return check_wish
        user = self.context['request'].user
        wish_users = obj.wish_user.all()
        if user in wish_users:
            return True
        else:
            return False

    def running_time_display(self, obj):
        return obj.movie_id_detail.running_time

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
    types = StringArrayField(source='type', help_text='0: 디지털 / 1: 3D / 2: 4D / 3: ATMOS / 4: 자막 / 5: 더빙')  # 타입
    total_seat = serializers.IntegerField(source='date_id.screen_id.total_seat')  # 총좌석 수
    st_count = serializers.IntegerField(source='seat_count', help_text='예매된 좌석 수')  # 예매된 좌석 수
    seat_number = StringArrayField(source='schedule_time_seat.seat_number', help_text='예매된 좌석 번호')  # 예매된 좌석 번호(배열)
    age = serializers.CharField(source='get_age_display')  # 영화 연령 제한
    running_time = serializers.IntegerField(
        source='movie_id.movie_id_detail.running_time')  # 영화 러닝 타임, related_name으로 oneToone 불러오기

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
    schedule_id = serializers.IntegerField(source='id',
                                           help_text='사용자가 시청할 영화 스케줄의 고유 id 값')  # 사용자가 관람할(선택한) 영화의 스케줄 id
    # seat_number = serializers.CharField(source='schedule_time_seat.seat_number', help_text='예매된 좌석 번호')  # 예매된 좌석 번호(배열)
    seat_number = StringArrayField(source='schedule_time_seat.seat_number', help_text='예매된 좌석 번호')  # 예매된 좌석 번호(배열)
    price = serializers.IntegerField(help_text='예매 최종 가격')  # 영화의 가격
    st_count = serializers.IntegerField(source='seat_count', help_text='예매된 좌석 수')  # 예매된 좌석 수

    class Meta:
        model = Schedule_time
        fields = ('schedule_id', 'seat_number', 'price', 'st_count')


class MovieDetailSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField('img_url_display')
    thumbnail_url = serializers.SerializerMethodField('thumbnail_url_display')
    title = serializers.SerializerMethodField('title_display')
    booking_rate = serializers.SerializerMethodField('booking_rate_display')
    age = serializers.SerializerMethodField('age_display')
    types = TypesArrayField(source='movie.type')
    release_date = serializers.SerializerMethodField('release_date_display')
    director = serializers.SerializerMethodField('director_display')
    cast = serializers.SerializerMethodField('cast_display')
    genre = serializers.SerializerMethodField('genre_display')
    description = serializers.SerializerMethodField('description_display')

    class Meta:
        model = Movie
        fields = ('img_url', 'thumbnail_url', 'title', 'age', 'booking_rate', 'types', 'release_date', 'director', 'cast', 'genre', 'description')

    def img_url_display(self, obj):
        return obj.movie.img_url

    def thumbnail_url_display(self, obj):
        return obj.movie.thumbnail_url

    def title_display(self, obj):
        return obj.movie.title

    def age_display(self, obj):
        return obj.movie.get_age_display()

    def booking_rate_display(self, obj):
        return obj.movie.booking_rate

    def release_date_display(self, obj):
        return obj.movie.release_date

    def genre_display(self, obj):
        genre = f"{obj.genre} / {obj.running_time} 분"
        return genre

    def director_display(self, obj):
        return obj.director

    def cast_display(self, obj):
        return obj.cast

    def description_display(self, obj):
        return obj.description


class CheckWishMovieSerializer(serializers.Serializer):
    is_wished = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_is_wished(self, obj):
        user_mail = obj.user
        # movie = Movie.objects.get(id=obj.query_params['movie_id'])  # method is get
        movie = Movie.objects.get(id=obj.data['movie_id'])  # method is get
        if user_mail in movie.wish_user.all():
            movie.wish_user.remove(user_mail)
            return False
        else:
            movie.wish_user.add(user_mail)
            return True


class ShowWishMoviesInfoSerializer(serializers.Serializer):
    img_url = serializers.SerializerMethodField()
    age = serializers.CharField(source='get_age_display', help_text='0: 전체 관람, 1: 12세 관람가, 2: 15세 관람가, 3: 청소년 관람불가')
    title = serializers.SerializerMethodField()
    booking_rate = serializers.SerializerMethodField()

    class Meta:
        fields = ('img_url', 'age', 'title', 'booking_rate')

    def get_img_url(self, obj):
        return obj.img_url

    def get_title(self, obj):
        return obj.title

    def get_booking_rate(self, obj):
        return obj.booking_rate


class ShowRegionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    theater = serializers.SerializerMethodField()
    selected = serializers.BooleanField(default=False, help_text='지역 모달 표시 여부에 사용되는 변수')

    class Meta:
        model = Region
        fields = ('id', 'region', 'theater', 'selected')

    def get_id(self, obj):
        return obj['index']

    def get_region(self, obj):
        return obj['item'].region.name

    def get_theater(self, obj):
        return obj['item'].cinema_name


class Return_200(serializers.Serializer):
    status = serializers.CharField(allow_blank=True, required=False, default='ok')


class Return_404(serializers.Serializer):
    error = serializers.CharField(allow_blank=True, required=False, default='404 Not Found')


class Return_error(serializers.Serializer):
    error = serializers.CharField(allow_blank=True, required=False, default='필요한 요청이 충분하지 않습니다.')
