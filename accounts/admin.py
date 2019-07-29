from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


# 화면 필드 정하기
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'birthDate', 'phoneNumber', 'preferTheater')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'birthDate', 'phoneNumber', 'preferTheater'),
        }),
    )
    list_display = ('id', 'email', 'name', 'is_staff')
    search_fields = ('email', 'name', 'birthDate')
    ordering = ('email',)

# # Register your models here.
# username -> email 변경 전 코드
#
# class CustomUserAdmin(UserAdmin):  # models.py 에 추가한 필드를 admin에 나타나게 해줌
#     UserAdmin.fieldsets[1][1]['fields'] += (
#         'name', 'preferTheater', 'watchedMovie', 'wishMovie', 'phoneNumber', 'birthDate')
#     UserAdmin.add_fieldsets += (
#         (('Additional Info'),
#          {'fields': ('name', 'preferTheater', 'watchedMovie', 'wishMovie', 'phoneNumber', 'birthDate')}),
#     )
#
#
# admin.site.register(User, CustomUserAdmin)
