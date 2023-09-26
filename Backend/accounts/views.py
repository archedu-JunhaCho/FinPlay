from django.shortcuts import render
from .serializers import UserSerializer, UserdetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User, Avatar
from rest_framework.authtoken.models import Token as Tokenmodel
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.authentication import TokenAuthentication
import requests, random
from rest_framework.authentication import TokenAuthentication
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
import os
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# 유저 정보 받아오기
@api_view(['GET'])
def userdetail(request):
    print('유저정보를 불러옵니다.')
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    serializer = UserdetailSerializer(user)
    return Response(
          {'detail': '유저정보를 전송합니다.',
          'userdata' : serializer.data},
          status=status.HTTP_200_OK,
        )

# 유저정보 업데이트
@api_view(['PUT'])
def userUpdate(request):
  token_auth = TokenAuthentication()
  user, _ = token_auth.authenticate(request)
  print()
  print('유저정보를 업데이트 합니다. 유저는', user,'받아온 정보는', request.data, request.POST)
  form = UserSerializer(user, data=request.data)
  print('폼미쳤다',form)
  if form.is_valid(raise_exception=True):
    print('유효합니다')
    form.save()
    return Response(
      {'detail': ('Successfully update account.')},
      status=status.HTTP_200_OK,
    )

# 팔로우 
@api_view(['POST'])
def follow(request, pk):
      # URL PK는 팔로우 대상
      token_auth = TokenAuthentication()
      user, _ = token_auth.authenticate(request)
      # print('로그인 유저는',request.user)
      check = User.objects.filter(follow = user)
      print('로그인 유저가 팔로우하는 사람은', check)
      if User.objects.get(pk=pk) in check:
          print('이미 팔로우 중이니 언팔합니다')
          User.objects.get(pk=pk).follow.remove(user)
          return Response(
          {'detail': ('Unfollowed')},
            status=status.HTTP_200_OK,
          )
      else:
          print('아직 팔로우 중이 아니므로 팔로우합니다')
          User.objects.get(pk=pk).follow.add(user)
          return Response(
            {'detail': ('followed')},
            status=status.HTTP_200_OK,
          )
      
## 아바타 관련
# 랜덤 아바타 생성
@csrf_exempt
@api_view(['GET','POST'])
def createAvatar(request):
    hair = [f'variant0{i}' if i < 10 else f'variant{i}' for i in range(1,49)]
    hairColor = [
    "000000",  # 블랙
    "FFB6C1",  # 라벤더 핑크 (Lavender Pink)
    "87CEEB",  # 스카이 블루 (Sky Blue)
    "FFDAB9",  # 피치 (Peach)
    "98FB98",  # 파스텔 그린 (Pastel Green)
    "FFA07A",  # 라이트 코랄 (Light Coral)
    "FFC0CB",  # 로즈 (Rose)
    "ADD8E6",  # 연보라 (Lavender)
    "FFD700",  # 골드 (Gold)
    "FFB5C5",  # 블러쉬 핑크 (Blush Pink)
    "00FA9A",  # 민트 크림 (Mint Cream)
    "D8D8D8"   # 화이트
    ]
    skinColor = [
    "F8D9D3",  # 연한 로즈 (Light Rose)
    "E9CBBE",  # 라이트 베이지 (Light Beige)
    "D6BAA5",  # 밝은 갈색 (Light Brown)
    "BEA58E",  # 자연스러운 베이지 (Natural Beige)
    "A8937A",  # 중간 갈색 (Medium Brown)
    "FFFFFF"   # 화이트
    ]
    head = [f'variant0{i}'for i in range(1,5)]
    eyes = [f'variant0{i}' if i < 10 else f'variant{i}'for i in range(1,25)]
    eyebrows = [f'variant0{i}' if i < 10 else f'variant{i}' for i in range(1,14)]
    nose = [f'variant0{i}'for i in range(1,7)]
    mouth = [f'happy0{i}' if i < 10 else f'happy{i}'for i in range(1,19)] + [f'sad0{i}'for i in range(1,10)]
    glasses = [f'variant0{i}'for i in range(1,6)]
    glassesProbability = [0, 100]

    # 사용자 요청
    if request.method == 'POST':
        pass
    # 랜덤 생성
    elif request.method == 'GET':
        print('아바타를 랜덤 생성합니다')
        URL = "https://api.dicebear.com/6.x/lorelei/png"
        params = {
           "hair" : random.choice(hair),  
           "hairColor" : random.choice(hairColor), 
           "skinColor" : random.choice(skinColor),  
           "head" : random.choice(head),   
           "eyes" : random.choice(eyes),  
           "eyebrows" : random.choice(eyebrows), 
           "nose" : random.choice(nose), 
           "mouth" : random.choice(mouth), 
           "glasses" : random.choice(glasses), 
           "glassesProbability" : random.choice(glassesProbability), 
        }
        personality_lst = ['건방진','온순한','개구쟁이의','우울한','쾌활한','똑똑한','전문가의', '연인의']
        response = requests.get(URL, params=params)
        # 생성
        token_auth = TokenAuthentication()
        user, _ = token_auth.authenticate(request)
        personality = random.choice(personality_lst)
        print(user.avatar.all())
        if user.avatar.all():
            print('이미 존재함')
            remove_item = user.avatar.get(user=user)
            print(remove_item.img_file)
            os.remove(f'media/{remove_item.img_file}')
            remove_item.delete()
            print('삭제 완료')
        with open(f"media/{user.username}_avatar.jpg", "wb") as file:
            file.write(response.content)
        with open(f"../../{user.username}_avatar.jpg", "wb") as file:
            file.write(response.content)
        savefile = File(open(f"media/{user.username}_avatar.jpg", 'rb'))
        Avatar.objects.create(personality=personality, user=user, img_file=savefile)
        print("이미지 저장 완료")
        return FileResponse(savefile, content_type='image/jpeg')

# 회원 탈퇴시 아바타 삭제
@api_view(['GET'])
def delavatar(request):
    print('hi')
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    remove_item = user.avatar.get(user=user)
    os.remove(f'media/{remove_item.img_file}')
    os.remove(f'{remove_item.img_file}')
    remove_item.delete()
    return Response(
            {'detail': '아바타까지 삭제 완료'},
            status=status.HTTP_200_OK,
          )
    
