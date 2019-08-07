import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from database.models import Region, Movie
from .models import BookingHistory, WatchedMovie, StarRate


class UserSerializer(serializers.ModelSerializer):  # rest_framework list 에 뜨는 정보
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password', 'birthDate', 'phoneNumber', 'preferTheater']


# class UserListSerializer(serializers.ModelSerializer):  # 유저 목록 출력을 위한 시리얼 라이저
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'email', 'name', 'password', 'birthDate', 'phoneNumber', 'preferTheater', ]


class UserCreateInPreferListSerializer(serializers.Serializer):
    getPreferList = serializers.SerializerMethodField('prefer_list_display', help_text='DB에서 선호상영관 선택 리스트를 불러옵니다.')

    class Meta:
        fields = ('getPreferList',)

    def prefer_list_display(self, obj):
        regions = Region.objects.all()
        preferList = list()

        for region in regions:
            theaters = Region.objects.get(name=region).region_id.all()
            for theater in theaters:
                preferList.append({region.name: theater.cinema_name})

        return preferList


# 회원 가입 할 때 필요한 필드들에 관한 시리얼라이저
# 유저 생성 할때 입력받을 필드
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'birthDate', 'phoneNumber', 'preferTheater']

    # password 암호화 = 회원가입 기능 실행 시 리스트 목록에 password 암호화 되어 나타남
    # def create(self, validated_data):
    #     print('validated_data: ', validated_data)
    #     print('type: ', validated_data)

    # user = get_user_model().objects.create(**validated_data)
    # user.set_password(validated_data.get('password'))
    # user.is_active = True
    # user.save()

    # return user
    # return user


class UpdateMyInfoSerializer(serializers.ModelSerializer):
    preferTheater = serializers.SerializerMethodField('string_to_array')
    password = serializers.SerializerMethodField('password_display', required=False)

    class Meta:
        model = get_user_model()
        fields = ('phoneNumber', 'preferTheater', 'password')

    def string_to_array(self, obj):
        data = obj.preferTheater
        if data:
            list_ = eval(data)
            return list_
        else:
            return None

    def password_display(self, obj):
        return obj.password


class PreferTheaterSerializer(serializers.ModelSerializer):
    preferTheater = serializers.SerializerMethodField('string_to_array')
    getPreferList = serializers.SerializerMethodField('prefer_list_display', help_text='DB에서 선호상영관 선택 리스트를 불러옵니다.')

    class Meta:
        model = get_user_model()
        fields = ('preferTheater', 'getPreferList')

    def string_to_array(self, obj):
        data = obj.preferTheater
        if data:
            list_ = eval(data)
            return list_
        else:
            return None

    def prefer_list_display(self, obj):
        regions = Region.objects.all()
        preferList = list()

        for region in regions:
            theaters = Region.objects.get(name=region).region_id.all()
            for theater in theaters:
                preferList.append({region.name: theater.cinema_name})

        return preferList


from pytz import timezone


class ShowMyInfoSerializer(serializers.ModelSerializer):
    preferTheater = serializers.SerializerMethodField('string_to_array')
    getPreferList = serializers.SerializerMethodField('prefer_list_display', help_text='DB에서 선호상영관 선택 리스트를 불러옵니다.')
    last_login = serializers.SerializerMethodField(help_text='마지막 로그인 시간')

    class Meta:
        model = get_user_model()
        fields = (
        'email', 'name', 'birthDate', 'phoneNumber', 'preferTheater', 'getPreferList', 'last_login', 'mileage')

    def string_to_array(self, obj):
        data = obj.preferTheater
        if data:
            list_ = eval(data)
            return list_
        else:
            return None

    def prefer_list_display(self, obj):
        regions = Region.objects.all()
        preferList = list()

        for region in regions:
            theaters = Region.objects.get(name=region).region_id.all()
            for theater in theaters:
                preferList.append({region.name: theater.cinema_name})

        return preferList

    def get_last_login(self, obj):
        KST = timezone('Asia/Seoul')
        last_login = obj.last_login.astimezone(KST)

        return last_login.strftime('%Y-%m-%d %H:%M:%S')


class BookingHistorySerializer(serializers.ModelSerializer):
    img_url = serializers.CharField(source='schedule_id.movie_id.img_url')  # 포스터 이미지
    title = serializers.CharField(source='schedule_id.movie_id.title', help_text='영화 제목')  # 영화 타이틀
    theater = serializers.CharField(source='schedule_id.date_id.screen_id.cinema_id.cinema_name')  # 지점
    screen_number = serializers.IntegerField(source='schedule_id.date_id.screen_id.screen_number',
                                             help_text='상영관 번호')  # 상영관 번호
    show_date = serializers.DateField(source='schedule_id.date_id.date', help_text='상영 일시')  # 상영 일시
    start_time = serializers.SerializerMethodField('time_display', help_text='상영 시작 시간, ex)15:30')  # 상영 시간
    booking_date = serializers.SerializerMethodField('booking_date_display', help_text='상영 시작 시간, ex)15:30')  # 상영 시간

    class Meta:
        model = BookingHistory
        fields = ('booking_number', 'title', 'img_url', 'theater', 'screen_number', 'show_date', 'start_time',
                  'booking_date', 'canceled')

    def time_display(self, obj):
        time = obj.schedule_id.start_time.strftime('%H:%M')
        return time

    def booking_date_display(self, obj):
        datetime = obj.booking_date.strftime('%Y-%m-%d %H:%M')
        return datetime


class ShowWatchedMoviesInfoSerializer(serializers.Serializer):
    img_url = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    schedule_date = serializers.SerializerMethodField()
    theater_headcount = serializers.SerializerMethodField()

    class Meta:
        fields = ('img_url', 'age', 'title', 'schedule_date', 'theater_headcount',)

    def get_img_url(self, obj):
        return obj.booking_history_id.schedule_id.movie_id.img_url

    def get_age(self, obj):
        return obj.booking_history_id.schedule_id.movie_id.get_age_display()

    def get_title(self, obj):
        return obj.booking_history_id.schedule_id.movie_id.title

    def get_schedule_date(self, obj):
        running_time = obj.booking_history_id.schedule_id.movie_id.movie_id_detail.running_time
        start_time = obj.booking_history_id.schedule_id.start_time
        schedule_date = obj.booking_history_id.schedule_id.date
        timeToDatetime = datetime.datetime(schedule_date.year, schedule_date.month, schedule_date.day, start_time.hour,
                                           start_time.minute, start_time.second)
        end_time = timeToDatetime + datetime.timedelta(0, running_time * 60)
        return f"{timeToDatetime.strftime('%Y-%m-%d %H:%M')}-{end_time.strftime('%H:%M')}"

    def get_theater_headcount(self, obj):
        theater = obj.booking_history_id.schedule_id.date_id.screen_id.__str__()
        headcount = f"{obj.booking_history_id.schedule_id.seat_count}명"
        return theater + ' / ' + headcount


class MyPageSerializer(serializers.ModelSerializer):
    booking_history = serializers.SerializerMethodField('booking_history_display', help_text='최근 예매 내역')
    # booking_history = StringArrayField(source='', help_text='최근 예매 내역')
    watchedMovieNumber = serializers.SerializerMethodField('watched_movie_number_display', help_text='본 영화 개수')
    wishMovieNumber = serializers.SerializerMethodField('wish_movie_number_display', help_text='선호 영화 개수')
    preferTheater = serializers.SerializerMethodField('string_to_array')

    class Meta:
        model = get_user_model()

        fields = (
            'phoneNumber', 'preferTheater', 'booking_history', 'watchedMovieNumber', 'wishMovieNumber', 'mileage')

    def booking_history_display(self, obj):
        data = obj.watched_movie_users.filter(user=obj)
        list_ = list()

        for item in data.values():
            b_obj = BookingHistory.objects.get(booking_number=item['booking_history_id_id'])
            schedule = b_obj.schedule_id

            theater = f"{schedule.date_id.screen_id.cinema_id} ({schedule.date_id.screen_id.screen_number}관)"

            dict_ = {
                'img_url': schedule.movie_id.img_url,
                'title': schedule.movie_id.title,
                'booking_date': b_obj.booking_date.strftime('%Y-%m-%d %H:%M'),
                'theater': theater,
            }

            list_.append(dict_)
        return list_

    def watched_movie_number_display(self, obj):
        data = WatchedMovie.objects.filter(user=obj)
        return len(data)

    def wish_movie_number_display(self, obj):
        data = Movie.objects.filter(wish_user=obj)
        return len(data)

    def string_to_array(self, obj):
        data = obj.preferTheater
        if data:
            list_ = eval(data)
            return list_
        else:
            return None


class UserStarRate(serializers.Serializer):
    star_rate = serializers.SerializerMethodField()

    class Meta:
        model = StarRate
        fields = '__all__'

    def get_star_rate(self, obj):
        # user = get_user_model().objects.get(user=obj.user)
        results = list()
        user_rate = StarRate.objects.filter(user=obj)
        for star_rate in user_rate:
            rate_info = {
                str(star_rate.movie): int(star_rate.rate)
            }
            results.append(rate_info)
        return results
