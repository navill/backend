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


# class UserView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)


# class SomeView(SomeGenericView): # 회원가입 등등 인증 없이도 동작하도록 설정할 떄 해당 위치에 아래 코드 삽입
#     permission_classes = (AllowAny,)


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     renderer_classes = [JSONRenderer]  # 이 코드는 http://127.0.0.1:8000/user/?format=json 주소에 format 인자를 추가해 결정
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)


class UserUpdate(generics.UpdateAPIView):
    """
    UserUpdate

    계정을 수정합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDelete(generics.DestroyAPIView):
    """
    UserDelete

    계정을 삭제합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


# class UserListAPI(generics.ListAPIView):  # user list 값 받기?
#     queryset = get_user_model().objects.all()
#     serializer_class = UserListSerializer
#     # filterset_fields = ('id',)  # 필터 기능을 동작시키고 싶으면 해당 코드 이 위치에 작성
#     permission_classes = (AllowAny,)
#
#     # 본인에 관한 정보만 노출되도록 설정코드작성 - 관리자는 전체목록 확인 가능
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if not self.request.user.is_staff:
#             queryset = queryset.filter(pk=self.request.user.id)
#         return queryset


class UserCreateAPI(generics.CreateAPIView):  # user create 값 받기?
    """
    UserCreateAPI

    계정을 생성합니다.
    """
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


@swagger_auto_schema(method='get',
                     responses={200: BookingHistorySerializer(many=True)},
                     operation_id='bookingHistory',
                     operation_description="최근 예매 내역을 열람합니다.", )
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def bookingHistoryView(request):
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
def myPageView(request):
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
            # print('booking_date: ', b_date)
            # print('booking_start_time: ', b_start_time)
            # print('booking_datetime: ', b_datetime)
            # print('item: ', item)

            for obj in watchedObj:
                # 이미 본 영화에 추가되었다면 추가 안함
                # print('item.booking_number: ', item.booking_number)
                # print('watched.booking_history_id.booking_number: ', watched.booking_history_id.booking_number)
                if item.booking_number == obj.booking_history_id.booking_number:
                    watched = True

            if not watched and today > b_datetime:
                WatchedMovie.objects.create(
                    booking_history_id=item,
                    user=myUser,
                )

            watched = False

        serializer = MyPageSerializer(myUser)
        return Response(serializer.data)


@api_view(['GET'])
def create_star_rate_view(request):
    user_rate = int(request.GET.get('star_rate'))
    movie_id = request.GET.get('movie_id')
    # star_rate = get_rate['star_rate']
    # user_star_rate
    # movie.total_rate 를 받아와서 점수의 총합을 이용해 처리
    movie = Movie.objects.get(id=movie_id)
    total_rate = movie.total_star_rate
    # 영화에 표시될 데이터 처리(float으로 반환)
    # total_rate = total_rate//len(users)

    # database.serializer 에서 float 타입으로 변환하기 위해 movie model에 저장
    # 해당 유저가 입력한 별점을 모두 출력
    star_obj = StarRate.objects.filter(user=request.user, movie=movie_id)
    if 0 < user_rate < 6:
        if not star_obj:
            StarRate.objects.create(user=request.user, movie_id=movie_id, rate=user_rate)
            # total_rate += user_rate
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
            # for i in star_obj:
            obj.save()
        # star_obj.save()
    elif user_rate is '0':
        if star_obj:
            obj = StarRate.objects.get(user=request.user, movie=movie_id)
            # total_rate = total_rate - obj.rate
            # movie.total_star_rate = total_rate
            # movie.save()
            StarRate.objects.filter(id=obj.id).delete()
        else:
            pass
    serializer = UserStarRate(request.user)
    return Response(serializer.data)


class CustomObtainJSONWebToken(JSONWebTokenAPIView):
    """
    Login

    계정을 로그인합니다.
    """
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        # request.user.last_login = datetime.now()
        # request.user.save(update_fields=['last_login'])

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
    """
    UserUpdate

    계정을 수정합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDelete(generics.DestroyAPIView):
    """
    UserDelete

    계정을 삭제합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


# class UserListAPI(generics.ListAPIView):  # user list 값 받기?
#     queryset = get_user_model().objects.all()
#     serializer_class = UserListSerializer
#     # filterset_fields = ('id',)  # 필터 기능을 동작시키고 싶으면 해당 코드 이 위치에 작성
#     permission_classes = (AllowAny,)
#
#     # 본인에 관한 정보만 노출되도록 설정코드작성 - 관리자는 전체목록 확인 가능
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if not self.request.user.is_staff:
#             queryset = queryset.filter(pk=self.request.user.id)
#         return queryset


class UserCreateAPI(generics.CreateAPIView):  # user create 값 받기?
    """
    UserCreateAPI

    계정을 생성합니다.
    """
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
def user_create_in_prefer_list_view(request):
    serializer = UserCreateInPreferListSerializer(Region)
    return Response(serializer.data)


@swagger_auto_schema(method='post',
                     responses={200: UserCreateSerializer(many=True)},
                     operation_id='userCreate',
                     operation_description="계정을 생성합니다.", )
@api_view(['POST'])
def user_create_view(request):
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
def show_my_info_view(request):
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
def update_my_info_view(request):
    user = request.user  # 로그인 유저 정보를 담음.

    if not user:
        return False
    else:
        data = request.data  # 사용자 요청 데이터를 담음.

        # dictionary에 먼저 user 데이터를 담음.
        userData = {
            'phoneNumber': user.phoneNumber,
            'preferTheater': user.preferTheater
        }

        try:
            if data['preferTheater']:  # 선호영화관을 수정한다면
                data_pre = data['preferTheater']
                if user.preferTheater:
                    user_pre = eval(user.preferTheater)

                    for i in range(len(data_pre)):
                        user_pre[i].update(data_pre[i])

                    # print('data_pre: ', data_pre)
                    # print('user_pre: ', user_pre)
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

        # re = User.objects.get(pk=user.id)  # 값 확인용
        # serializer = UpdateMyInfoSerializer(re)  # 값 확인용
        # return Response(serializer.data)  # 값 확인용
        return Response(True)


@swagger_auto_schema(method='get',
                     responses={200: PreferTheaterSerializer(many=True)},
                     operation_id='showPreferTheater',
                     operation_description="선호 영화관 등록/수정에서 선호영화관 및 선택 리스트를 출력합니다.", )
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_prefer_theater_view(request):
    user = request.user

    if not user:
        return False
    else:
        serializer = PreferTheaterSerializer(user)
        return Response(serializer.data)


@swagger_auto_schema(method='post',
                     # responses={200: PreferTheaterSerializer(many=True)},
                     operation_id='updatePreferTheater',
                     operation_description="선호 영화관 등록/수정에서 선호영화관을 등록/수정합니다.", )
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_prefer_theater_view(request, id):
    user = request.user

    if not user:
        return False
    else:
        preferId = id
        userPrefer = eval(user.preferTheater)
        data = request.data
        userPrefer[preferId].update(data)

        # serializer = PreferTheaterSerializer(user, data=userPrefer[0], partial=True)
        # print('serializer: ', serializer)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)

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
def booking_history_view(request):
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
def my_page_view(request):
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
            # print('booking_date: ', b_date)
            # print('booking_start_time: ', b_start_time)
            # print('booking_datetime: ', b_datetime)
            # print('item: ', item)

            for obj in watchedObj:
                # 이미 본 영화에 추가되었다면 추가 안함
                # print('item.booking_number: ', item.booking_number)
                # print('watched.booking_history_id.booking_number: ', watched.booking_history_id.booking_number)
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
def show_watched_movies_info_view(request):
    movies = WatchedMovie.objects.filter(user=request.user)

    print(movies[0].booking_history_id.schedule_id.movie_id.title)

    serializer = ShowWatchedMoviesInfoSerializer(movies, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: UserStarRate()},
                     operation_id='createStarRate',
                     operation_description="유저 평점을 생성합니다.")
@api_view(['GET'])
def create_star_rate_view(request):
    user_rate = int(request.GET.get('star_rate'))
    movie_id = request.GET.get('movie_id')
    # star_rate = get_rate['star_rate']
    # user_star_rate
    # movie.total_rate 를 받아와서 점수의 총합을 이용해 처리
    movie = Movie.objects.get(id=movie_id)
    total_rate = movie.total_star_rate
    # 영화에 표시될 데이터 처리(float으로 반환)
    # total_rate = total_rate//len(users)

    # database.serializer 에서 float 타입으로 변환하기 위해 movie model에 저장
    # 해당 유저가 입력한 별점을 모두 출력
    star_obj = StarRate.objects.filter(user=request.user, movie=movie_id)
    if 0 < user_rate < 6:
        if not star_obj:
            StarRate.objects.create(user=request.user, movie_id=movie_id, rate=user_rate)
            # total_rate += user_rate
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
            # for i in star_obj:
            obj.save()
        # star_obj.save()
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
def check_email_view(request):
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
