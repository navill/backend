# CopySite(Megabox) Project

### 패스트캠퍼스에서 진행한 팀프로젝트입니다(2019.07~2019.08).

Live: [http://megabox.website](http://www.megabox.website/)


- 영화 예매 사이트인 Megabox 사이트의 기능을 구현한 프로젝트입니다.

- 이 프로젝트는 Front-end(**AngularJs & iOS**) 및 **Back-end** 팀으로 구성되었습니다.

- 이 repository는 **Back-end** 구성원인 제가 참여한 프로젝트 저장소입니다.

- 저는 사이트에서 제공하는 **영화 예매, 평점 및 영화 정보 제공** 기능과 **DB 모델링**을 주로 맡아 진행하였습니다.

  **예매**

  - [views.show_movies](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L21): 예매 및 메인 페이지에서 제공하기 위한 영화의 기본 정보
  - [views.reservation_schedule_list](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L46): 예매 시 날짜와 극장, 상영관 및 영화 정보 제공
  - [views.reservation_second](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L105): 좌석 배정 및 가상 결제 페이지
  - [serializers.CheckWishMovieSerializer](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/serializers.py#L219): 보고싶은 영화 기능 구현
  - [serializers.ShowWishMoviesInfoSerializer](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/serializers.py#L238): 유저가 등록한 보고싶은 영화 정보 제공

  **평점**

  - [views.create_star_rate](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/accounts/views.py#L281): 영화에 유저가 입력한 평점 반영

  **영화 정보**

  - [views.movie_detail](https://github.com/navill/backend/blob/3c6461a1bb1fdc8330ba5c9cb61552e3c5c16b92/database/views.py#L32): 영화 상세 정보를 제공

  데이터베이스 모델링

- 사용자 DB 모델링

![account_megabox](/README_image/account_megabox.png)

- 영화 및 예매 모델링

![booking_megabox](/README_image/booking_megabox.png)