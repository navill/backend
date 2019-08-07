import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from database.models import *
from database.serializers import Return_error
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
