from django.urls import path
from .views import UserView, UserDetail
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('', UserView.as_view()),
    path('detail/<int:pk>/', UserDetail.as_view()),
    path('login/', LoginView.as_view(template_name='accounts/accounts_login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/accounts_logout.html'), name='logout'),
]


