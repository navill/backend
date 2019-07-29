from django.urls import path
from .views import *

app_name = 'database'
urlpatterns = [
    # path('', index, name='index'),
    # path('RegionCreate/', RegionCreateView.as_view()),
    # path('RegionList/', RegionListView.as_view()),
    # path('RegionDetail/<int:pk>', RegionDetailView.as_view()),
    #
    # path('ScreenCreate/', ScreenCreateView.as_view()),
    # path('ScreenList/', ScreenListView.as_view()),
    # path('ScreenDetail/<int:pk>', ScreenDetailView.as_view()),
    #
    # path('CinemaCreate/', CinemaCreateView.as_view()),
    # path('CinemaList/', CinemaListView.as_view()),
    # path('CinemaDetail/<int:pk>', CinemaDetailView.as_view()),
    #
    # path('Schedule_timeCreate/', Schedule_timeCreateView.as_view()),
    # path('Schedule_timeList/', Schedule_timeListView.as_view()),
    # path('Schedule_timeDetail/<int:pk>', Schedule_timeDetailView.as_view()),
    #
    # path('Schedule_dateCreate/', Schedule_dateCreateView.as_view()),
    # path('Schedule_dateList/', Schedule_dateListView.as_view()),
    # path('Schedule_dateDetail/<int:pk>', Schedule_dateDetailView.as_view()),
    #
    # path('MovieCreate/', MovieCreateView.as_view()),
    # path('MovieList/', MovieListView.as_view()),
    # path('MovieDetail/<int:pk>', MovieDetailView.as_view()),

    # path('reservationFirstView/', reservationFirstView), # 뷰 나누기 전 원본 url 남기기
    path('showMovies/', showMoviesView),
    path('reservationScheduleList/', reservationScheduleListView),
    path('reservationSecondView/', reservationSecondView),
    path('bookingHistoryView/', bookingHistoryView),
]

