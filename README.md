# Megabox Project

### 패스트캠퍼스에서 진행한 팀프로젝트입니다(2019.07~2019.08).

**Live**: [http://megabox.website](http://www.megabox.website/)(AWS Free Service가 만료되면서 서버가 닫혔습니다.)

### 카테고리

- [사용 기술](#사용-기술)
- [요약](#요약)
- [주요기능](#주요-기능)
- [데이터베이스 모델링](#데이터베이스-모델링)
- [문서화 - yasg](#yasg)



## 사용 기술

**Language & Framework**

- Python
- Django
- Django REST Framework

**Library**

- Django REST Framework - JWT
- Boto3
- Debug Tool Bar
- Swagger & yasg

**Cloud Platform(AWS)**

- EC2(ubuntu)
- RDS(PostgreSQL)
- S3(Static & Media)



## 요약


- 영화 예매 사이트인 Megabox 사이트의 기능을 구현한 프로젝트입니다.

- 이 프로젝트는 **Front-end**(**Angular.Js) & iOS** 및 **Back-end** 팀으로 구성되었습니다.

- 이 저장소는 제가 맡은 **Back-end** 코드가 저장된 저장소입니다.

- 사이트에 제공하는 **영화 예매, 평점 및 영화 정보 제공** 기능과 **DB 모델링, 더미 데이터 생성 스크립트**를 맡아 진행하였습니다.

  

## 주요 기능

### JWT를 이용한 인증

**[주요코드]**

- [views.CustomObtainJSONWebToken](https://github.com/navill/backend/blob/a8ba11933aaf9e5204db9d9d4744015536fa8aa6/accounts/views.py#L17): 로그인 성공 시, jwt serializer를 이용해 Token 생성

![jwt](/README_image/jwt.png)

- 사용자 인증을 위해 jwt를 이용한 token 인증
- 로그인 시 생성된 token을 이용해 사이트에 접근



### 영화 스케줄 & 예매

**[주요코드]**

- [views.show_movies](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L21): 예매 및 메인 페이지에서 제공하기 위한 영화의 기본 정보
- [views.reservation_schedule_list](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L46): 예매 시 날짜와 극장, 상영관 및 영화 정보 제공
- [views.reservation_second](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L105): 좌석 배정 및 가상 결제 페이지

![schedule_list](/README_image/schedule_list.png)

- 지역 및 영화를 선택할 경우, 해당 시간과 날짜에 등록된 극장 및 영화 리스트 출력



![ticketing](/README_image/ticketing.png)

- 좌성 지정 및 결제 기능



### 영화 상세 정보

**[주요코드]**

- [views.movie_detail](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L32): 영화 상세 정보 제공

![movie_detail](/README_image/movie_detail.png)



### 이외 기능

**[주요 코드]**

- [serializers.CheckWishMovieSerializer](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/serializers.py#L219): 보고싶은 영화 기능 구현
- [serializers.ShowWishMoviesInfoSerializer](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/serializers.py#L238): 유저가 등록한 보고싶은 영화 정보 제공

- [views.create_star_rate](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/accounts/views.py#L281): 영화에 유저가 입력한 평점 반영

* [create_db_data](https://github.com/navill/backend/blob/master/create_db_data.py): 테스트에 필요한 데이터를 자동으로 생성



## 데이터베이스 모델링

- 사용자 DB 모델링

![account_megabox](/README_image/account_megabox.png)

- 영화 및 예매 모델링

![booking_megabox](/README_image/booking_megabox.png)



## yasg - 자동 문서화를 위한 라이브러리

![account_megabox](/README_image/yasg.png)

- yasg(Yet another Swagger generator)를 이용해 자동 문서화 
- Front-End 및 iOS 팀과 협업을 위해 사용





