from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from database.models import Schedule_time, Movie


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


import json


class User(AbstractUser):
    """User model."""
    # username -> email 변경 할당 부분
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # custom models fielda 부분
    preferTheater = models.TextField(verbose_name='선호 영화관', blank=True)  # CharField 선호 영화관 한개만
    phoneNumber = models.CharField(verbose_name='핸드폰 번호', max_length=15, blank=True, null=True)  # CharField
    birthDate = models.DateField(verbose_name='생년월일', null=True, blank=True)  # DateField
    name = models.CharField(verbose_name='이름', max_length=30)
    mileage = models.IntegerField(default=0)
    # wishMovie = models.CharField(verbose_name='보고싶어', max_length=20, blank=True)  # CharField, 불필요한 필드로 판단

    def set_preferTheater(self, x):
        self.preferTheater = json.dumps(x)

    def get_preferTheater(self):
        return json.loads(self.preferTheater)


# 테이블 재설계 필요
# -> 이유 : 현재 이 테이블은 삭제 될 가능성이 있는 스케줄 id에 상당히 의존적임
# -> 문제 : 스케줄 id가 지워지면 따로 영화 정보를 저장하는 것이 아니기 때문에 조회가 불가능해짐
# -> 해결1 : 스케줄 id에 의존하는 것이 아닌 이 테이블에 예매한 영화 정보를 저장함.
# -> 해결2 : 스케줄 id가 지워질 일이 없다고 가정하면 굳이 안고쳐도 됨.
class BookingHistory(models.Model):
    booking_number = models.CharField(editable=False, max_length=50, primary_key=True)  # 예매 번호, 랜덤하게 생성
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', null=True)  # 예매한 유저
    schedule_id = models.ForeignKey(Schedule_time, on_delete=models.SET_NULL, null=True)  # 예매한 영화 스케줄
    seat_number = models.CharField(max_length=200)  # 예매한 좌석 번호들
    booking_date = models.DateTimeField(editable=False, auto_now_add=True)  # 예매한 날짜, 시간
    canceled = models.BooleanField(default=False)  # 예매 취소 여부
    total_price = models.IntegerField(default=0)
    
# BookingHistory만 참조하는 거면 따로 테이블 생성 없이 BookingHistory 이용해서 본영화를 출력할 때 날짜 비교해서 예매날짜 지난 것만 출력하게 하면 됨
# 하지만 예매 내역에 없는 영화를 등록할 수 있음(오프라인 예매를 했을 경우 가능)
# --> 이 기능이 필요하다면 오프라인 예매 정보만을 등록할 수 있는 기능이 필요함
# 또 본 영화를 삭제도 가능하므로 테이블을 생성을 하는게 맞다고 판단
# --> 오프라인 예매 등록, 삭제 기능 활용하지 않을 경우 굳이 테이블 생성이 필요 없을듯
class WatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_movie_users')
    booking_history_id = models.ForeignKey(BookingHistory, on_delete=models.SET_NULL, null=True)


class StarRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
