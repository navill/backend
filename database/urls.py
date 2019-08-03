from django.urls import path

from .views import *

app_name = 'database'
urlpatterns = [
    path('showMovies/', showMoviesView),
    path('reservationScheduleList/', reservationScheduleListView),
    path('reservationSecondView/', reservationSecondView),
    path('checkwish', check_wishmovies_view),
    path('showregion', show_region_view),
]
