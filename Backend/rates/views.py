from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse, HttpResponse
from django.http import HttpRequest
from .models import *
from .serializers import *
import requests
import schedule
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from django.shortcuts import get_object_or_404, get_list_or_404
import datetime
from dateutil.relativedelta import relativedelta

# 환율 정보 불러오기
sched = BackgroundScheduler()
# @sched.scheduled_job('cron', hour='12', minute='04', second='45', id='test')
@api_view(['GET'])
def loadRatedata(request):
  cdate = datetime.datetime.today()
  yday = cdate - datetime.timedelta(days=1)
  yesterday = str(cdate - datetime.timedelta(days=1))[:10]
  change_yd = yesterday.replace('-','')
  print('어제 날짜 폼체인지전', yesterday)
  print('어제 날짜 폼체인지',change_yd)
  print('어제날짜의 요일', yday.weekday())
  URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
  params = {
              'authkey' : settings.API_KEY2,
              'data' : 'AP01',
              'searchdate' : change_yd
          }
  # if yday.weekday() in [5,6]:
  #   print("주말은 데이터를 불러올수 없습니다")
  #   return Response({'detail': '주말은 데이터를 불러올수 없습니다'}, status=status.HTTP_200_OK)
  # else:
  try:
    sample = str(Ratechange.objects.all()[0].dataDate)
    if change_yd == sample:
      print('이미 정보가 불러와 있습니다.')
      return Response({'detail': '이미 정보가 불러와 있습니다.',
                       'reload' : False}, status=status.HTTP_200_OK)
    else:
      print('환율 정보를 업데이트합니다.')
      # 기존 환율 정보 지우고
      # 현재 시각으로 다시 불러옴
      if yday.weekday()  == 5:    # 토요일
        return Response({'detail': '주말인 토요일에 대해서는 불러올 수 없습니다.'}, status=status.HTTP_200_OK)
      elif yday.weekday()  == 6:  # 일요일
        return Response({'detail': '주말인 일요일에 대해서는 불러올 수 없습니다.'}, status=status.HTTP_200_OK)
      else:
        alldata = Ratechange.objects.all()
        alldata.delete()
        response = requests.get(URL, params=params).json()
        for item in response:
          form = RateChangeSerializer(data=item)
          if form.is_valid():
            form.save(dataDate=change_yd)
        return Response({'detail': '환율 정보를 업데이트했습니다.',
                         'reload' : True}, status=status.HTTP_200_OK)
  except:
    print('환율 정보를 불러옵니다.')
    if yday.weekday() in [5,6]:
      change_yd = newyesterday.replace('-','')
      newyesterday = str(cdate - datetime.timedelta(days=3))[:10]
      print('폼체인지',change_yd)
      params["searchdate"] = change_yd
    response = requests.get(URL, params=params).json()
    print('받아온 정보입니다',response)
    for item in response:
      form = RateChangeSerializer(data=item)
      print(form)
      if form.is_valid():
        form.save(dataDate=change_yd)
    print('환율 정보를 성공적으로 불러왔습니다.')
    return Response({'detail': 'DB에 성공적으로 데이터를 불러 왔습니다.',
                     'reload' : True},status=status.HTTP_200_OK)
  
# def main():
#   sched = BackgroundScheduler()
#   sched.add_job(loadRatedata, 'cron', hour='11', minute='54', second='25', id='doit', args=(HttpRequest(),))
#   sched.start()
# sched.start()

@api_view(['GET'])
def listAllrate(request):
  print('DB에 저장된 환율 정보를 불러옵니다.')
  all_rates = get_list_or_404(Ratechange)
  serializer = RateChangeSerializer(all_rates, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def detailrate(request):
  find = request.data["cur_nm"]
  print(f'{find} 환율 정보를 불러옵니다.')
  find_one_rate = Ratechange.objects.get(cur_nm = find)
  serializer = RateChangeSerializer(find_one_rate)
  return Response(serializer.data)
