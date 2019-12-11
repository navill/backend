from django.urls import path

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomObtainJSONWebToken.as_view()),  # 로그인 URL
    path('update/<int:pk>/', UserUpdate.as_view()),  # 기본 rest_framework 디테일 URL
    path('delete/<int:pk>/', UserDelete.as_view()),  # 기본 rest_framework 디테일 URL
    path('showCreate/', user_create_in_prefer_list),
    path('create/', user_create, name='user_create'),  # views 에 유저 생성 URL
    path('bookingHistory/', booking_history),
    path('myPage/', my_page),
    path('showWatchedMovies/', show_watched_movies_info),
    path('showMyInfo/', show_my_info),
    path('updateMyInfo/', update_my_info),
    path('updatePreferTheater/', show_prefer_theater),
    path('updatePreferTheater/<int:id>', update_prefer_theater),
    # 별점 추가
    path('star_rate/', create_star_rate),
    path('check_email/', check_email),
    path('canceled/', canceled)
]
