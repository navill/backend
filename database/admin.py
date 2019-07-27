from django.contrib import admin
from .models import *


#
#
# # Register your models here.
#
# class ScheduleInline(admin.TabularInline):
#     model = Schedule
#     raw_id_fields = ['screen']
#
#
# class SeatInline(admin.TabularInline):
#     model = Seat
#     raw_id_fields = ['screen']
#
#
# class ScreenOption(admin.ModelAdmin):
#     list_display = ['theater', 'screen_number', 'total_seat']
#     inlines = [ScheduleInline, SeatInline]

# class RegionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']


# admin.site.register(Region, RegionAdmin)


class CinemaAdmin(admin.ModelAdmin):
    list_display = ['cinema_name']


admin.site.register(Cinema, CinemaAdmin)


class ScreenAdmin(admin.ModelAdmin):
    list_display = ['show_cinema', 'screen_number', 'total_seat']


admin.site.register(Screen, ScreenAdmin)


class Schedule_dateAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_cinema', 'show_screen', 'date']


class Schedule_timeAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'date_id', 'seat_count', 'start_time', 'string_date']


admin.site.register(Schedule_date, Schedule_dateAdmin)
admin.site.register(Schedule_time, Schedule_timeAdmin)


class SeatAdmin(admin.ModelAdmin):
    list_display = ['schedule_time', 'seat_number']


admin.site.register(Seat, SeatAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'age', 'type', 'img_url', 'release_date', 'booking_rate']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Movie_detail)

class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'user', 'schedule_id', 'seat_number', 'booking_date', 'canceled')

admin.site.register(BookingHistory, BookingHistoryAdmin)