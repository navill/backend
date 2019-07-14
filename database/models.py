from django.db import models


# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):  # -> string
        return self.name


class Cinema(models.Model):
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region_id')
    cinema_name = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    class Meta:
        ordering = ['cinema_name']

    def __str__(self):  # -> string
        return self.cinema_name


class Screen(models.Model):
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_id", null=True)
    screen_number = models.IntegerField()
    total_seat = models.IntegerField()

    class Meta:
        ordering = ['screen_number']

    def show_cinema(self):
        return self.cinema_id.cinema_name

    def __str__(self):  # -> string
        return self.cinema_id.cinema_name + ' ' + str(self.screen_number) + '관'


class Movie(models.Model):
    AGE_RATE = (
        (0, '전체 관람'),
        (12, '12세 관람가'),
        (15, '15세 관람가'),
        (19, '청소년 관람불가'),
    )
    TYPE = (
        (0, '2D'),
        (1, '3D'),
        (2, '4D'),
        (3, 'Digital'),
    )

    title = models.CharField(max_length=100)
    age = models.IntegerField(choices=AGE_RATE, default=0)
    type = models.IntegerField(choices=TYPE, default=0)

    def __str__(self):  # -> string
        return self.title


class Movie_detail(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='movie_id_detail')
    running_time = models.IntegerField()
    description = models.TextField()
    release_date = models.DateField()


#
class Schedule_date(models.Model):
    screen_id = models.ForeignKey(Screen, on_delete=models.SET_NULL, related_name="screen_id_schedule", blank=True,
                                  null=True)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def show_cinema(self):
        return self.screen_id.cinema_id.cinema_name

    def show_screen(self):
        return self.screen_id.screen_number

    def __str__(self):  # -> string
        return f"{self.screen_id.cinema_id.cinema_name} screen {self.screen_id.screen_number} - 상영일자: {self.date} "


class Schedule_time(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_id_schedule", null=True)
    date_id = models.ForeignKey(Schedule_date, on_delete=models.CASCADE, related_name="date_id_schedule", null=True)
    # seat_count = models.IntegerField()  # 예매된 좌석의 수- Screen의 total_seat와 연산되어져야 한다.
    # available_seat = models.BooleanField(default=True)  # screen_id.total_seat - seat_count =>매진 여부
    start_time = models.TimeField()  # start_time + movie.running_time = end_time

    class Meta:
        ordering = ['start_time']

    def show_item_schedule_detail(self):
        return self.screen_id.cinema_id.cinema_name

    def __str__(self):  # -> string
        return f"지점 : {self.date_id.screen_id.cinema_id.cinema_name}(screen:{self.date_id.screen_id.screen_number}), 상영일자: {self.date_id.date}, 시간: {self.start_time}" \
            f", 영화 제목: {self.movie_id.title}"

    def get_type_display(self):
        return self.movie_id.get_type_display()


class Seat(models.Model):
    schedule_time = models.OneToOneField(Schedule_time, on_delete=models.CASCADE, primary_key=True,
                                         related_name='schedule_time_seat')
    # screen_id = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='screen_id_seat', null=True)
    seat_number = models.TextField()
    # available = models.BooleanField(default=True)  # 예매 될 경우 false
    # git test를 위한 수정사항 입니다.
    # def __str__(self):  # -> string
    #     return f"좌석 번호: {self.seat_number}"
