from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    # username -> email 변경 할당 부분
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # custom models fielda 부분
    preferTheater = models.CharField(verbose_name='선호 영화관', max_length=100, blank=True)  # CharField 선호 영화관 한개만
    phoneNumber = models.CharField(verbose_name='핸드폰 번호', max_length=15, blank=True, null=True)  # CharField
    birthDate = models.DateField(verbose_name='생년월일', null=True, blank=True)  # DateField
    name = models.CharField(verbose_name='이름', max_length=30)
    watchedMovie = models.CharField(verbose_name='본 영화', max_length=20, blank=True)  # CharField
    wishMovie = models.CharField(verbose_name='보고싶어', max_length=20, blank=True)  # CharField

