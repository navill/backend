from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from pytz import utc
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView

from database.serializers import Return_error
from .models import *
from .serializers import *


class CustomObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        jwt = serializer.validated_data
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        jwt['user'].last_login = utc.localize(now).astimezone(KST)
        jwt['user'].save(update_fields=['last_login'])
        return Response({'token': jwt['token'], 'user': jwt['user'].email, 'name': jwt['user'].name},
                        status=status.HTTP_200_OK)


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserCreateAPI(generics.CreateAPIView):  # user create 값 받기?
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        print('preferTheater: ', self.request.data['preferTheater'])

        return Response(self)


@swagger_auto_schema(method='get',
                     responses={200: UserCreateInPreferListSerializer(many=True)},
                     operation_id='userCreateInPreferTheaterList',
                     operation_description="유저 생성시 선택할 수 있는 선호영화관의 리스트를 출력합니다.", )
@api_view(['GET'])
def user_create_in_prefer_list(request):
    serializer = UserCreateInPreferListSerializer(Region)
    return Response(serializer.data)


@swagger_auto_schema(method='post',
                     responses={200: UserCreateSerializer(many=True)},
                     operation_id='userCreate',
                     operation_description="계정을 생성합니다.", )
@api_view(['POST'])
def user_create(request):
    data = request.data
    data_str = None

    try:
        if data['preferTheater']:
            for i in range(len(data['preferTheater'])):
                data['preferTheater'][i]['id'] = i
            data_str = str(data['preferTheater'])
    except KeyError:
        data_str = \
            "[{'id': 0, 'theater': '', 'region': ''}," \
            "{'id': 1, 'theater': '', 'region': ''}, " \
            "{'id': 2, 'theater': '', 'region': ''}]"

    user = User.objects.create_user(
        email=data['email'],
        password=data['password'],
        name=data['name'],
        birthDate=data['birthDate'],
        phoneNumber=data['phoneNumber'],
        preferTheater=data_str
    )

    serializer = UserCreateSerializer(user)
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: ShowMyInfoSerializer(many=True)},
                     operation_id='myInfo',
                     operation_description="수정할 개인 정보를 출력합니다.", )
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def show_my_info(request):
    user = request.user

    if not user:
        return False
    else:
        serializer = ShowMyInfoSerializer(user)
        return Response(serializer.data)


@swagger_auto_schema(method='post',
                     responses={200: UpdateMyInfoSerializer(many=True)},
                     operation_id='updateMyInfo',
                     operation_description="개인 정보를 수정합니다.", )
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def update_my_info(request):
    user = request.user
    if not user:
        return False
    else:
        data = request.data
        userData = {
            'phoneNumber': user.phoneNumber,
            'preferTheater': user.preferTheater
        }

        try:
            if data['preferTheater']:
                data_pre = data['preferTheater']
                if user.preferTheater:
                    user_pre = eval(user.preferTheater)
                    for i in range(len(data_pre)):
                        user_pre[i].update(data_pre[i])

                    data['preferTheater'] = str(user_pre)
        except KeyError:
            pass

        try:
            if data['password']:  # 패스워드도 수정한다면
                userData.update({'password': user.password})
                userData.update(data)

                User.objects.filter(pk=user.id).update(
                    password=make_password(userData['password']),
                    phoneNumber=userData['phoneNumber'],
                    preferTheater=userData['preferTheater']
                )
        except KeyError:  # 패스워드는 수정 안한다면
            userData.update(data)
            User.objects.filter(pk=user.id).update(
                phoneNumber=userData['phoneNumber'],
                preferTheater=userData['preferTheater']
            )

        return Response(True)


@swagger_auto_schema(method='get',
                     responses={200: PreferTheaterSerializer(many=True)},
                     operation_id='showPreferTheater',
                     operation_description="선호 영화관 등록/수정에서 선호영화관 및 선택 리스트를 출력합니다.", )
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_prefer_theater(request):
    user = request.user

    if not user:
        return False
    else:
        serializer = PreferTheaterSerializer(user)
        return Response(serializer.data)


@swagger_auto_schema(method='post',
                     operation_id='updatePreferTheater',
                     operation_description="선호 영화관 등록/수정에서 선호영화관을 등록/수정합니다.", )
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_prefer_theater(request, id):
    user = request.user

    if not user:
        return False
    else:
        preferId = id
        userPrefer = eval(user.preferTheater)
        data = request.data
        userPrefer[preferId].update(data)
        user.preferTheater = str(userPrefer)
        print('user.preferTheater: ', user.preferTheater)

        User.objects.filter(pk=user.id).update(
            preferTheater=user.preferTheater
        )

        serializer = PreferTheaterSerializer(user)
        return JsonResponse(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: BookingHistorySerializer(many=True)},
                     operation_id='bookingHistory',
                     operation_description="최근 예매 내역을 열람합니다.", )
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def booking_history(request):
    myUser = request.user
    if not myUser:
        serializer = Return_error('1')
        return Response(serializer.data)
    else:
        queryset = BookingHistory.objects.filter(user=myUser)
        serializer = BookingHistorySerializer(queryset, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: MyPageSerializer(many=True)},
                     operation_id='myPage',
                     operation_description="마이페이지를 열람합니다.", )
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def my_page(request):
    myUser = request.user
    watched = False  # 봤던 영화 체크에 필요한 변수

    if not myUser:
        serializer = Return_error('1')
        return Response(serializer.data)
    else:
        bookingObj = BookingHistory.objects.filter(user=myUser)
        watchedObj = WatchedMovie.objects.filter(user=myUser)
        today = datetime.datetime.now()

        # 상영일이 지났다면 본 영화에 추가
        for item in bookingObj:
            b_date = item.schedule_id.date
            b_start_time = item.schedule_id.start_time
            b_datetime = datetime.datetime.strptime(str(b_date) + ' ' + str(b_start_time), '%Y-%m-%d %H:%M:%S')

            for obj in watchedObj:
                if item.booking_number == obj.booking_history_id.booking_number:
                    watched = True

            if not watched and today > b_datetime:
                WatchedMovie.objects.create(
                    booking_history_id=item,
                    user=myUser,
                )
                myUser.mileage = item.total_price * 0.1
                myUser.save()
            watched = False

        serializer = MyPageSerializer(myUser)
        return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: ShowWatchedMoviesInfoSerializer()},
                     operation_id='showWatchedMoviesInfo',
                     operation_description="본 영화 정보를 출력합니다.")
@api_view(['GET'])
def show_watched_movies_info(request):
    movies = WatchedMovie.objects.filter(user=request.user)

    print(movies[0].booking_history_id.schedule_id.movie_id.title)

    serializer = ShowWatchedMoviesInfoSerializer(movies, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: UserStarRate()},
                     operation_id='createStarRate',
                     operation_description="유저 평점을 생성합니다.")
@api_view(['GET'])
def create_star_rate(request):
    user_rate = int(request.GET.get('star_rate'))
    movie_id = request.GET.get('movie_id')
    movie = Movie.objects.get(id=movie_id)
    total_rate = movie.total_star_rate
    star_obj = StarRate.objects.filter(user=request.user, movie=movie_id)

    if 0 < user_rate < 6:
        if not star_obj:
            StarRate.objects.create(user=request.user, movie_id=movie_id, rate=user_rate)
            movie.total_star_rate = user_rate + total_rate
            movie.save()
            serializer = UserStarRate(request.user)
            return Response(serializer.data)
        else:
            obj = StarRate.objects.get(user=request.user, movie=movie_id)
            if obj.rate <= user_rate:
                rate = int(user_rate) - obj.rate
                total_rate += rate
                movie.total_star_rate = total_rate
                movie.save()
            else:
                rate = obj.rate - int(user_rate)
                total_rate -= rate
                if total_rate <= 0:
                    total_rate = 0
                movie.total_star_rate = total_rate
                movie.save()
            obj.rate = user_rate
            obj.save()
    elif user_rate is 0:
        if star_obj:
            obj = StarRate.objects.get(user=request.user, movie=movie_id)
            movie.total_star_rate = total_rate - obj.rate
            movie.save()
            StarRate.objects.filter(id=obj.id).delete()
        else:
            pass
    serializer = UserStarRate(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def check_email(request):
    users = User.objects.all()
    emails = [email for email in users.values('email')]
    target_email = request.data['email']
    temp_list = list()
    for i in emails:
        _, email = i.popitem()
        temp_list.append(email)
    if target_email in temp_list:
        result = False
    else:
        result = True
    return Response(result)


@api_view(['POST'])
def canceled(request):
    booking_number = request.data['booking_number']
    user = request.user
    booking_obj = BookingHistory.objects.get(booking_number=booking_number, user=user)
    booking_obj.canceled = False
    booking_obj.save()
    return Response(booking_obj.canceled)
