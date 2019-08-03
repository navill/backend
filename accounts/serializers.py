from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import BookingHistory, WatchedMovie, User


class UserSerializer(serializers.ModelSerializer):  # rest_framework list 에 뜨는 정보
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password', 'birthDate', 'phoneNumber', 'preferTheater', ]


# class UserListSerializer(serializers.ModelSerializer):  # 유저 목록 출력을 위한 시리얼 라이저
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'email', 'name', 'password', 'birthDate', 'phoneNumber', 'preferTheater', ]


# 회원 가입 할 때 필요한 필드들에 관한 시리얼라이저
# 유저 생성 할때 입력받을 필드
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'birthDate', 'phoneNumber', 'preferTheater', ]

    # password 암호화 = 회원가입 기능 실행 시 리스트 목록에 password 암호화 되어 나타남
    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.is_active = True
        user.save()

        return user


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


class MyPageSerializer(serializers.ModelSerializer):
    booking_history = serializers.SerializerMethodField('booking_history_display', help_text='최근 예매 내역')
    # booking_history = StringArrayField(source='', help_text='최근 예매 내역')
    watchedMovieNumber = serializers.SerializerMethodField('watched_movie_number_display', help_text='본 영화 개수')

    class Meta:
        model = User
        fields = ('phoneNumber', 'preferTheater', 'booking_history', 'watchedMovieNumber',)

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
