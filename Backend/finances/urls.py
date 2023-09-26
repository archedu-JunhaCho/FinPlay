from django.urls import path
from . import views


urlpatterns = [
    ## 예금
    # 정기 예금 상품 목록 DB에 저장
    path('save-deposit-products/', views.sdp, name='sdp'),
    # 전체 예금 상품 목록 출력 & 데이터 삽입
    path('deposit-products/', views.dp, name='dp'),
    # 특정 예금 상품의 출력
    path('deposit-products/<str:PK>/', views.dpd, name='dpd'),
    # 예금 상품 가입
    path('deposit-products/<str:PK>/signin', views.in_dp, name='in_dp'),


    ## 적금
    # 정기 적금 상품 목록 DB에 저장
    path('save-saving-products/', views.ssp, name='ssp'),
    # 전체 적금 상품 목록 출력 & 데이터 삽입
    path('saving-products/', views.sp, name='sp'),
    # 특정 적금 상품의 출력
    path('saving-products/<str:PK>/', views.spd, name='spd'),
    # 적금 상품 가입
    path('saving-products/<str:PK>/signin', views.in_sp, name='in_dp'),
    
    ## 추천상품
    path('recommend-products/', views.recommend, name='recommend'),
    path('recommend-products/<int:pk>/', views.recommend_list, name='recommend-list'),
    path('recommend-products/top3/', views.top3, name='top3'),

    ## 키워드 저장
    path('create-keyword/', views.createKeyword, name='createKeyword'),
    path('create-keyword2/', views.createKeyword2, name='createKeyword2'),
    path('user-keyword/', views.userkeyword, name='userkeyword'),
    
]
