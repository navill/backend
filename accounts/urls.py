from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomObtainJSONWebToken.as_view()),  # 로그인 URL
    # path('logout/', LogoutView.as_view(template_name='accounts/accounts_logout.html'), name='logout'),  # 로그아웃 URL
    # path('', UserView.as_view()),  # 기본 rest_framework URL
    # path('detail/<int:pk>/', UserDetail.as_view()),  # 기본 rest_framework 디테일 URL
    path('update/<int:pk>/', UserUpdate.as_view()),  # 기본 rest_framework 디테일 URL
    path('delete/<int:pk>/', UserDelete.as_view()),  # 기본 rest_framework 디테일 URL
    # path('create/', UserCreateAPI.as_view(), name='user_create'),  # views 에 유저 생성 URL
    path('showCreate/', user_create_in_prefer_list_view),
    path('create/', user_create_view, name='user_create'),  # views 에 유저 생성 URL
    # path('list/', UserListAPI.as_view(), name='user_list'),  # views 에 유저 list URL
    path('bookingHistory/', booking_history_view),
    path('myPage/', my_page_view),
    path('showWatchedMovies/', show_watched_movies_info_view),
    path('showMyInfo/', show_my_info_view),
    path('updateMyInfo/', update_my_info_view),
    path('updatePreferTheater/', show_prefer_theater_view),
    path('updatePreferTheater/<int:id>', update_prefer_theater_view),
    # 별점 추가
    path('star_rate/', create_star_rate_view),
    path('check_email/', check_email_view),
    path('canceled/', canceled_view)
]
