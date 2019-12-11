from django.urls import path

from .views import *

app_name = 'database'
urlpatterns = [
    path('showMovies/', show_movies),
    path('reservationScheduleList/', reservation_schedule_list),
    path('reservationSecond/', reservation_second),
    path('movieDetail/', movie_detail),
    path('checkwish/', check_wish_movies),
    path('showregion/', show_region),
    path('showWishMovies/', show_wish_movies_info)
]
