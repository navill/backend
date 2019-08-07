from django.urls import path

from .views import *

app_name = 'database'
urlpatterns = [
    path('showMovies/', showMoviesView),
    path('reservationScheduleList/', reservationScheduleListView),

    path('reservationSecond/', reservationSecondView),
    path('movieDetail/', movie_detail_view),
    path('checkwish/', check_wishmovies_view),
    path('showregion/', show_region_view),
    path('showWishMovies/', show_wish_movies_info_view)
]
