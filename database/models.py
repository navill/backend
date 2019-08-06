from django.db import models
from multiselectfield import MultiSelectField

AGE_RATE = (
    (0, '전체 관람'),
    (1, '12세 관람가'),
    (2, '15세 관람가'),
    (3, '청소년 관람불가'),
)
TYPE = (
    (0, '디지털'),
    (1, '3D'),
    (2, '4D'),
    (3, 'ATMOS'),
    (4, '자막'),
    (5, '더빙'),
)


class Region(models.Model):
    name = models.CharField(max_length=100)

    # class Meta:

    def __str__(self):
        return self.name


class Cinema(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region_id')
    cinema_name = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    class Meta:
        ordering = ['cinema_name']

    def __str__(self):  # -> string
        return self.cinema_name


class Screen(models.Model):
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_id")
    screen_number = models.IntegerField()
    total_seat = models.IntegerField()

    # type = MultiSelectField(choices=TYPE, max_choices=4)

    class Meta:
        ordering = ['screen_number']

    def show_cinema(self):
        return self.cinema_id.cinema_name

    def __str__(self):
        return self.cinema_id.cinema_name + ' ' + str(self.screen_number) + '관'


class Movie(models.Model):
    img_url = models.CharField(max_length=200)
    thumbnail_url = models.CharField(max_length=200, null=True)
    release_date = models.DateField()
    booking_rate = models.FloatField()
    title = models.CharField(max_length=100)
    age = models.IntegerField(choices=AGE_RATE, default=0)
    # type = models.IntegerField(choices=TYPE, default=0)
    type = MultiSelectField(choices=TYPE, max_choices=5, max_length=50)
    wish_user = models.ManyToManyField('accounts.User', blank=True, related_name='wish_movie')

    # star_rate 추가해야함
    # sub_type = models.IntegerField(choices=SUB_TYPE, null=True)

    def __str__(self):
        return self.title


class Movie_detail(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='movie_id_detail')
    running_time = models.IntegerField()
    description = models.TextField()
    director = models.CharField(max_length=15)
    cast = models.TextField()
    genre = models.TextField()

    def __str__(self):
        return f"info: {self.movie.title}"


class Schedule_date(models.Model):
    screen_id = models.ForeignKey(
        Screen, on_delete=models.SET_NULL,
        related_name="screen_id_schedule", blank=True, null=True)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def show_cinema(self):
        return self.screen_id.cinema_id.cinema_name

    def show_screen(self):
        return self.screen_id.screen_number

    def call_date(self):
        return self.date

    def __str__(self):
        return f"{self.screen_id.cinema_id.cinema_name} screen {self.screen_id.screen_number} - 상영일자: {self.date} "


class Schedule_time(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_id_schedule", null=True)
    date_id = models.ForeignKey(Schedule_date, on_delete=models.CASCADE, related_name="date_id_schedule", null=True)
    seat_count = models.IntegerField(editable=False, default=0)  # 예매된 좌석의 수- Screen의 total_seat와 연산되어져야 한다.
    # available_seat = models.BooleanField(default=True)  # screen_id.total_seat - seat_count =>매진 여부
    start_time = models.TimeField()  # start_time + movie.running_time = end_time
    date = models.DateField()
    # 임시로 character field로 저장되기 위해 사용됨
    # type = models.CharField(max_length=15, null=True)
    type = MultiSelectField(choices=TYPE, max_choices=2, max_length=50, null=True)

    class Meta:
        ordering = ['start_time']

    # def show_item_schedule_detail(self):
    #     return self.screen_id.cinema_id.cinema_name
    # 
    def numbering_seat_count(self, length_count_list):
        self.seat_count = length_count_list

    # def save(self, *args, **kwargs):
    #     # convert date to string
    #     if not self.string_date:
    #         splited_date = list(map(int, str(self.date_id.date).split('-')))
    #         str_list_date = [str(a) for a in splited_date]
    #         str_date = ''.join(str_list_date)
    #         self.string_date = str_date
    #         self.date_id.save()
    #     super(Schedule_time, self).save(*args, **kwargs)

    def get_age_display(self):
        return self.movie_id.get_age_display()

    def __str__(self):
        return f"지점 : {self.date_id.screen_id.cinema_id.cinema_name}(screen:{self.date_id.screen_id.screen_number}), 상영일자: {self.date_id.date}, 시간: {self.start_time}" \
            f", 영화 제목: {self.movie_id.title}"


class Seat(models.Model):
    schedule_time = models.OneToOneField(Schedule_time, on_delete=models.CASCADE, related_name='schedule_time_seat',
                                         primary_key=True)
    # screen_id = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='screen_id_seat', null=True)
    seat_number = models.TextField(blank=True, default='')

    def save(self, *args, **kwargs):
        booked_list = str(self.seat_number).split(',')
        if not booked_list == ['']:
            seat_count = len(booked_list)
            self.schedule_time.seat_count = seat_count
            self.schedule_time.save()
        super(Seat, self).save(*args, **kwargs)
