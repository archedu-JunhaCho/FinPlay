from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse, HttpResponse
from .models import *
from .serializers import *
import requests
from django.db.models import Max
from rest_framework.authentication import TokenAuthentication
from accounts.serializers import *
import openai
from django.core import serializers as TOJSON
import json
import re

pattern = r"\[(.*?)\]"
k_lst = ['안정적인', '공격적인', '신뢰성', '수익성', '유동성', '성장', '저리스크', '고수익', '장기', '단기', '다각화', '저비용', '고수익률', '유연성', '저변동성', '현금흐름', '안전성', '탄력성', '혁신적인', '청년', '중년', '장년', '다양한 옵션', '이벤트', '기본 자금이 많은', '기본 자금 이 적은', '꼼꼼한 조건', '쉬운 가입', '고급화', '오프라인', '온라인', '안정적인 직장', '노후', '인터넷', '체계적인', '단순한', '쉬운', '여성특화', '남성특화', '청소년의', '스마트', '대중적인', '보너스가 많은', '특별상품', '다계좌', '해지가 자유로운']
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
model = "gpt-3.5-turbo"



API_KEY = settings.API_KEY
BASE_URL = 'http://finlife.fss.or.kr/'
api1_url = 'companySearch.json'                         # 금융회사 API
api2_url = 'finlifeapi/depositProductsSearch.json'      # 정기예금 API
api3_url = 'finlifeapi/savingProductsSearch.json'       # 적금 & 연금저축 API
api4_url = 'mortgageLoanProductsSearch.json'            # 주택담보대출 API
api5_url = 'rentHouseLoanProductsSearch.json'           # 전세자금대출 API
api6_url = 'creditLoanProductsSearch.json'              # 개인신용대출 API

# 정기예금 상품 목록 저장
@api_view(['GET'])
def sdp(request):
    print('정기예금 상품 목록 저장 진입')
    URL = BASE_URL + api2_url
    for how in ['020000','030300']:
        for num in range(1, 20):
            params = {
                'auth' : settings.API_KEY,
                'topFinGrpNo' : how,
                'pageNo' : num
            }
            response = requests.get(URL, params=params).json()
            # 1. Products
            print('검증할 프로덕 데이터 갯수', len(response['result']['baseList']))
            for item in response['result']['baseList']:
                form = DPSerializer(data=item)
                if form.is_valid():
                    form.save()
            # 2. Options
            print('검증할 옵션 데이터 갯수', len(response['result']['optionList']))
            for item in response['result']['optionList']:
                try:
                    fin_prdt_cd = DepositProducts.objects.get(fin_prdt_cd=item['fin_prdt_cd'])
                    form2 = DOSerializer(data=item)
                    if form2.is_valid():
                        search = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
                        dup = False
                        for check in search:
                            if check.intr_rate_type_nm == item['intr_rate_type_nm']:
                                if check.intr_rate  == item['intr_rate']:
                                    if check.intr_rate2 == item['intr_rate2']:
                                        if int(check.save_trm) == int(item['save_trm']):
                                            # print('빼액 중복값발견!!')
                                            dup = True
                                            break
                        if dup == False:
                            form2.save(fin_prdt_cd=fin_prdt_cd)
                except:
                    pass
    print('저장종료!!')
    return JsonResponse({'데이터로딩':'완료'})

# 전체 예금 상품 목록 출력, 정기예금 상품 추가하기
@api_view(['GET','POST'])
def dp(request):
    if request.method == 'GET':     # 목록 출력
        all_items= DepositProducts.objects.all()
        form = DPSerializer(all_items, many=True)
        return Response(form.data)
    elif request.method == 'POST':  # 데이터 삽입
        form = DPSerializer(data=request.data)
        if form.is_valid():
            form.save()
        return Response(form.data)

# 특정 예금 상품 출력
@api_view(['GET'])
def dpd(request, PK):
    product = DepositProducts.objects.get(fin_prdt_cd=PK)
    form = DPSerializer(product)
    return Response(form.data)



# 정기적금 상품 목록 저장
@api_view(['GET'])
def ssp(request):
    print('정기예금 상품 목록 저장 진입')
    URL = BASE_URL + api3_url
    for how in ['020000','030300']:
        for num in range(1, 20):
            params = {
                'auth' : settings.API_KEY,
                'topFinGrpNo' : how,
                'pageNo' : num
            }
            response = requests.get(URL, params=params).json()
            # 1. Products
            print('검증할 프로덕 데이터 갯수', len(response['result']['baseList']))
            for item in response['result']['baseList']:
                form = SPSerializer(data=item)
                if form.is_valid():
                    form.save()
            # 2. Options
            print('검증할 옵션 데이터 갯수', len(response['result']['optionList']))
            for item in response['result']['optionList']:
                try:
                    fin_prdt_cd = SavingProducts.objects.get(fin_prdt_cd=item['fin_prdt_cd'])
                    form2 = SOSerializer(data=item)
                    if form2.is_valid():
                        search = SavingOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
                        dup = False
                        for check in search:
                            if check.intr_rate_type_nm == item['intr_rate_type_nm']:
                                if check.intr_rate  == item['intr_rate']:
                                    if check.intr_rate2 == item['intr_rate2']:
                                        if int(check.save_trm) == int(item['save_trm']):
                                            # print('빼액 중복값발견!!')
                                            dup = True
                                            break
                        if dup == False:
                            form2.save(fin_prdt_cd=fin_prdt_cd)
                except:
                    pass
    print('저장종료!!')
    return JsonResponse({'데이터로딩':'완료'})

# 전체 적금 상품 목록 출력, 정기적금 상품 추가하기
@api_view(['GET','POST'])
def sp(request):
    if request.method == 'GET':     # 목록 출력
        all_items= SavingProducts.objects.all()
        form = SPSerializer(all_items, many=True)
        return Response(form.data)
    elif request.method == 'POST':  # 데이터 삽입
        form = SPSerializer(data=request.data)
        if form.is_valid():
            form.save()
        return Response(form.data)
    
# 특정 적금 상품 출력
@api_view(['GET'])
def spd(request, PK):
    product = SavingProducts.objects.get(fin_prdt_cd=PK)
    form = SPSerializer(product)
    return Response(form.data)

# 예금 상품 가입
@api_view(['GET'])
def in_dp(request, PK):
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    print(request.data, user ,user.product_lst, PK)
    if not user.product_lst:
        user.product_lst = [PK]
        print(type(user.product_lst))
        user.save()
        print('아무 상품에도 가입되어 있지 않습니다.')
    else:
        user_product = eval(user.product_lst)
        if PK in user_product:  # 이미 가입했을시
            print('이미 가입되어있으므로 가입 취소합니다.')
            print('기존', user_product)
            print(type(user.product_lst))
            user_product.remove(PK)
            print('이후', user_product)
            user.product_lst = user_product
            user.save()
        else:                       # 가입을 하지 않았을시
            print('가입합니다.')
            print('기존', user_product)
            print(type(user.product_lst))
            user_product.append(PK)
            print('이후', user_product)
            user.product_lst = user_product
            user.save()

    serializer = UserdetailSerializer(user)
    return Response({'detail': '해당 상품 가입/탈퇴을 완료했습니다.',"userdata" : serializer.data}, status=status.HTTP_200_OK)

# 적금 상품 가입
@api_view(['GET'])
def in_sp(request, PK):
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    print(request.data, user ,user.product_lst_saving, PK)
    if not user.product_lst_saving:
        user.product_lst_saving = [PK]
        print(type(user.product_lst_saving))
        user.save()
        print('아무 상품에도 가입되어 있지 않습니다.')

    else:
        user_product = eval(user.product_lst_saving)
        if PK in user_product:  # 이미 가입했을시
            print('이미 가입되어있으므로 가입 취소합니다.')
            print('기존', user_product)
            print(type(user.product_lst_saving))
            user_product.remove(PK)
            print('이후', user_product)
            user.product_lst_saving = user_product
            user.save()

        else:                       # 가입을 하지 않았을시
            print('가입합니다.')
            print('기존', user_product)
            print(type(user.product_lst_saving))
            user_product.append(PK)
            print('이후', user_product)
            user.product_lst_saving = user_product
            user.save()
    
    serializer = UserdetailSerializer(user)
    return Response({'detail': '해당 상품 가입/탈퇴을 완료했습니다.',"userdata" : serializer.data}, status=status.HTTP_200_OK)



## 추천 
# 추천데이터 불러오기
@api_view(['GET'])
def recommend(request):
    print('추천상품 api 요청')
    
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    add_options = request.data
    
    userinfo = f"한국의 {user.age}세의 {add_options} 투자성향"
    query = f"{userinfo}을 가진 사람에서 예적금 상품을 추천하고 싶어. 해당 사람이 금융 예적금 상품을 고를때 고려해야하는 것들을 그 사람에 대한 정보에 기반해서 알려줘. 이것은 하나의 게시글처럼 html태그로 디자인해서 보여줘"
    messages = [
        {"role": "system", "content": "You are a helpful assistant.게시판에 쓸 글 형식에 맞춰서 대답할 것. 줄바꿈과 형태에 유의할것."},
        {"role": "user", "content": query}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    if Recommendation.objects.filter(user=user).exists():
        remove_rec = Recommendation.objects.get(user=user)
        remove_rec.delete()
    Recommendation.objects.create(user=user, content = answer)
    
    print(answer)
    return Response({'detail': '추천 문구를 저장합니다.', 'answer':answer}, status=status.HTTP_200_OK)

@api_view(['GET'])
def recommend_list(request, pk):
    print('추천 문구 존재여부 확인요청')
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    recommend = Recommendation.objects.get(user=user)
    print(recommend)

    return Response({'detail': '추천 문구를 전송합니다.', 'answer':recommend.content}, status=status.HTTP_200_OK)

# 금융 데이터에 대해 키워드 추출
# 예금 정보 키워드 지정
@api_view(['GET'])
def createKeyword(requset):
    print('키워드 저장 요청')
    all_Dproduct = DepositProducts.objects.all()
    all_Dproduct_Json = json.loads(TOJSON.serialize('json', all_Dproduct))

    pattern = r"\[(.*?)\]"
    for i in zip(all_Dproduct, all_Dproduct_Json):
        # 키워드 존재하지 않을시 ChatGpt에게 요청
        if not Dkeyword.objects.filter(product=i[0]).exists():
            # p_info = str(i[1]).replace('"',"'")
            p_info = i[1]
            
            query = f"상품정보는 {p_info} 이고 키워드 리스트는 {k_lst}야."
            messages = [
                {"role": "system", "content": "상품의 정보와 키워드 리스트를 받으면 상품의 정보에 적합한 키워드들을 []형태의 리스트로 반환한다. 대답의 형식은 다른 말은 제외하고 키워드들을 담은 []만."},
                {"role": "user", "content": query}
            ]

            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages
                )
                answer = response['choices'][0]['message']['content']
                answer_form = str(re.findall(pattern, answer)[0]).replace('"','')
                print(answer, answer_form)
                Dkeyword.objects.create(product = i[0], keyword=answer_form)
                print(i[0],'에 대해 저장완료')
            except:
                print('에러발생 다음으로')

    return Response({'detail': '키워드를 모두 저장했습니다.'}, status=status.HTTP_200_OK)

# 적금 정보 키워드 지정
@api_view(['GET'])
def createKeyword2(requset):
    print('키워드 저장 요청')
    all_Sproduct = SavingProducts.objects.all()
    all_Sproduct_Json = json.loads(TOJSON.serialize('json', all_Sproduct))

    for i in zip(all_Sproduct, all_Sproduct_Json):
        # 키워드 존재하지 않을시 ChatGpt에게 요청
        if not Skeyword.objects.filter(product=i[0]).exists():
            # p_info = str(i[1]).replace('"',"'")
            p_info = i[1]
            query = f"상품정보는 {p_info} 이고 키워드 리스트는 {k_lst}야."
            messages = [
                {"role": "system", "content": "상품의 정보와 키워드 리스트를 받으면 상품의 정보에 적합한 키워드들을 []형태의 리스트로 반환한다. 대답의 형식은 다른 말은 제외하고 키워드들을 담은 []만."},
                {"role": "user", "content": query}
            ]

            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages
                )
                answer = response['choices'][0]['message']['content']
                answer_form = str(re.findall(pattern, answer)[0]).replace('"','')
                print(answer, answer_form)
                Skeyword.objects.create(product = i[0], keyword=answer_form)
                print(i[0],'에 대해 저장완료')
            except:
                print('에러발생 다음으로')

    return Response({'detail': '키워드를 모두 저장했습니다.'}, status=status.HTTP_200_OK)

# 유저 키워드 생성
@api_view(['GET'])
def userkeyword(request):
    print('유저 키워드 생성')

    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    print(user)
    userdata = UserkeywordSerializer(user).data
    select = request.data.get('select')
    userdata['성향'] = select
    print(userdata)

    
    u_info = userdata
    query = f"유저정보는 {u_info} 이고 키워드 리스트는 {k_lst}야."
    messages = [
        {"role": "system", "content": "유저 정보와 키워드 리스트를 받으면 유저의 정보에 적합한 키워드들을 []형태의 리스트로 반환한다. 대답의 형식은 다른 말은 제외하고 키워드들을 담은 []만."},
        {"role": "user", "content": query}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    answer_form = str(re.findall(pattern, answer)[0]).replace('"','')
    Personality.objects.create(user = user, content=answer_form)
    # answer = 1
    print(answer, answer_form)

    return Response({'detail': '유저 키워드를 생성했습니다.', 'answer':answer_form}, status=status.HTTP_200_OK)

# 유저에게 상품 추천
@api_view(['GET'])
def top3(request):
    print('키워드에 맞는 상품 추천받기')
    # 1. 유저 키워드 불러오기
    token_auth = TokenAuthentication()
    user, _ = token_auth.authenticate(request)
    user_keyword = user.personality_set.all()

    # 2. 예금, 적금 상품 pk와 키워드 통합하기
    all_list = []
    DP = Dkeyword.objects.all()
    for dp_item in DP:
        all_list += [[dp_item, '예금']]
    SP = Skeyword.objects.all()
    for sp_item in SP:
        all_list += [[sp_item, '적금']]
    # print('여기까지',all_list)

    # 3. 리스트 순찰하며 유사도 높은 상품을 추리기
    # print(user_keyword[0])
    u_key = user_keyword[0].content.replace("'",'').replace(' ', '').split(',')
    # print(u_key)
    for i in range(len(all_list)):
        p_key = all_list[i][0].keyword.replace("'",'').replace(' ', '').split(',')
        add_key = all_list[i][0].product_id
        # print(add_key, all_list[i][1])
        if all_list[i][1] == '적금':
            what_product = SavingProducts.objects.get(id=add_key)
            serial = SPSerializer(what_product)
        else:
            what_product = DepositProducts.objects.get(id=add_key)
            serial = DPSerializer(what_product)
        # print(what_product, serial.data, serial.data["id"])
        
        # print(p_key)
        # print('확인',list(set(p_key)), list(set(u_key)), list(set(p_key)&set(u_key)), len(list(set(p_key)&set(u_key))))
        all_list[i].append(len(list(set(p_key)&set(u_key))))
        all_list[i].append(serial.data)
        all_list[i][0] = add_key

    all_list.sort(key=lambda x:x[2])
    # print(all_list[::-1][:5])
    result = all_list[::-1][:5]

    return Response({'detail': '5개의 추천상품입니다', 'recommend': result}, status=status.HTTP_200_OK)
    