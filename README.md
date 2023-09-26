
# 2023_1_PJT
- projectname : FinPlay
  - 개요 : 딱딱한 금융 상품을 사용자 정보를 기반으로 좀 더 재밌게 추천받아보자. 
  - 핵심 : 개성을 가진 아바타를 통해 인공지능 ChatGPT와 연동된 추천 알고리즘을 제작한다.
  - 기술 및 활용 : 금융감독원 api, ChatGpt api, DiceBear api, KaKao map api / Vue.js, Javascript, Django, Python, 

- member : {'임서희' : [팀장, 프론트앤드], '조준하': [팀원, 백앤드]}

- 업무 분담은 하단 일일 작업기록 참고
  - 구글 독스를 활용한 세부일정표 작성
  - 일일 작업 기록을 통한 작업 공유
  - 08:30 ~ 09:00 / 12:30 ~ 13:00  주기적인 회의를 통해 흐름이 끊기는 소통을 줄이고자 노력 

- 서비스 대표 기능
  - 기본 기능 : 계정생성 및 권한을 통한 작업 ( 토큰 기반 ) / 게시글 및 댓글 / 카카오맵 기반의 지도상의 은행 찾기 / 환율 계산기 / 예적금 상품 조회
  - 부가 기능 : 좋아요 팔로우 구현
  - 핵심 기능 : ChatGpt를 연동한 금융상품추천 챗봇 구현, ChatGpt와 연동된 추상화 키워드를 바탕으로한 추천 시스템, DiceBear을 활용한 다양한 아바타 생성

- 설계
  - 프론트엔드 : 컴포넌트를 구조화하여 페이지간의 연동에 초점을 두어 설계를 진행
  - 백엔드 : 프론트에서 수행가능한 api도 백엔드에서 구조화하여 처리하고 DB에 저장할 수 있게 설계

- 구현
  - 프론트엔드 : 백엔드와 기능연동을 우선시하며, 디자인은 최대한 간략하게 진행, 기본교육과정에서 습득한 모든 기본 기능을 탑재하는 것을 우선시
  - 백엔드 : 많은 api를 사용하는 만큼 모델 설계와, api 요청 구조화 및 순서정렬에 심혈을 기울임 

- 금융 상품 추천 알고리즘
  - 요약 :  기존의 금융상품 추천 시스템과 다르게 인공지능을 적극 활용하되, 판단의 척도로 추상화된 다양한 키워드들을 기반으로 한다.
  - 1단계 : 예적금 데이터에 새롭게 생성한 키워드 모델 연결한다
  - 2단계 : 샘플 데이터를 기반으로 chatGpt + 리서치를 통해 금융상품을 판단할 수 있는 키워드들을 생성한다 ex. 안정적인, 디지털화
  - 3단계 : 금융상품 분석 프롬프트로 세팅된 chatGpt에서 `상품정보`와 `키워드리스트`를 전달하여 적합한 키워드 리스트를 반환 받는다.
  - 4단계 : 유저정보를 업데이트 받을시 chatGpt에서 `유저정보`와 `키워드리스트`를 매치하여 선호도가 높은 키워드 리스트를 반환 받는다.
  - 5단계 : 예적금 데이터에 저장된 키워드들과 유저정보로 기록된 키워드를 상호 매치하여 유사도가 높은 예적금을 5개까지 추천하도록 구성한다.
  - etc : 참고를 위한 `사용자 정보`에 기반한 포괄적인 금융상품 선정기준 메세지를 첨부한다.

- 보완점
  - 비밀번호 변경시 토큰 변경을 위해 로그아웃-로그인 
  - 로컬스토리지 일정 시간 이흐 비우기
  - 키워드 생성 폼 select 필드로 다양화 하기
  - 가입한 금융 상품에 대한 차트생성

- 느낀점 및 후기
  - 임서희 : 처음 진행하는 팀프로젝트에서 많은 것을 배워갑니다.
  - 조준하 : 인생 최초로 프론트엔드와 백엔드로 구분되어 협업하는 과정을 겪어 남다르다. 각자 장단점이 다른 팀원과 조율해나가며 프로젝트를 진행하여 프로그래밍 협업능력을 기를수 있었다.

<hr>

# 작업 일지

> 준하
### 2023.05.16 백앤드 작업
- [ Accounts , Article, Finance ] 필드 구성
- 각 앱별 api 요청 구축
  1. Accounts / 로그인, 로그아웃, 회원가입, 유저디테일, 비밀번호 변경 (dj-rest-auth)
  2. Article / 게시글 전체 조회 + 개별조회, 작성, 수정, 삭제 & 댓글 전체 조회 + 개별조회, 댓글 작성, 수정, 삭제
  3. Finance / 미구축


> 서히
### 2023.05.16 프론트 작업
1. 각 component 작업
2. component에 대한 router 경로 설정 
3. 로그인/회원가입 페이지 router 연동


## 2023.05.17

> 서히
### 2023.05.17 프론트 작업
1. component 연결 (라우팅까지 할 수 있으면 하기) --
2. url, history 모드 변경
- user부분
3. 로그인 포멧 바꾸기 => id 
4. 로그아웃 store,,,
  - 서버에서도 token 제거하기
5. 로그인 했으면 보이는 화면 -> 프로필 template 부분

> 준하
### 2023.05.17 백앤드 작업
- 회원 가입 + 로그인 > Vue와 연동
- 각 앱별 api 요청 추가
  1. Accounts / 팔로우
  2. Article / 좋아요
  3. Finance / 금융데이터 내려받기, 금융데이터 조회, 금융데이터 세부 조회


## 2023.05.18

- 서히
### 2023.05.18 프론트 작업
1. user정보 업데이트( 정보 업데이트, 비밀번호 업데이트)
2. 탈퇴 -> 버튼누르면 탈퇴되도록 구현해놓기
- user부분
3. 게시판 목록 template 구현
1. 로그아웃 store,,,
  - 서버에서도 token 제거하기
2. 로그인 했으면 보이는 화면 -> 프로필 template 부분
> 준하
### 2023.05.18 백앤드 작업
- 금융 데이터 모델 추가 및 변경
- 환율 계산기 api 생성
- 다음 지도 Vue
- 각 앱별 api 요청 구축
  1. Accounts / 유저 업데이트 뷰 변경
  2. Article / 완료
  3. Finance / 환율 정보 받아오기, 환율 리스트 조회, 환율 세부 조회


## 2023.05.19

> 준하
### 2023.05.19 백앤드 작업
1. 유저 데이터 프론트 백 구성
2. 환율 계산기 뷰 구성 (완료)
3. 지도 뷰 구성  (완료)
4. 정기적금 로딩/리스트업 api 구성
5. 예금 적금 디테일 리스트 api
- 각 앱별 api 요청 구축
  1. Accounts / 유저 데이터 몽땅 불러오기, 디테일 (작업필요)
  2. Article / 뷰랑 연동 필요
  3. Finance / 환율 완성

> 서히
### 2023.05.19 프론트 작업
하나 구현하는데 너무 오래 걸렸슴니다.... 암쏘리


예적금 페이지 만들었습니다.
공시 제출 월 -> 수정(완료)
div class='show-' 수정(완료)
옵션 오빠가 수정해주면 -> 6, 12, 24, 36 개월 수정하기(완료)
검색 조건 필터,, 환율 필터보고 수정하기(완료)
로그인 access_token 수정하기(오빠가 해주기로 했나?)

그래서 할일은
-> 예적금 검색, 완료하기
-> 디테일페이지까지해야함


> 서히
### 2023.05.21 프론트 작업

-1. 게시글 컴포넌트 구성 및 백엔드와 연동 확인(완료)
1-1. post(create)(완료)
1-2. put(수정)(미완료)
1-3. delete(미완료)
1. 예적금 API -> 주소 아니고 formdata로 보내기(검색 조건-은행, 예치기간)
2. 클릭하면 탈퇴 되도록 -> axios

## 2023.05.22

> 준하
### 2023.05.22 백앤드 작업
- 아바타 만들기 프론트 백 구축



## 2023.05.23

> 준하
### 2023.05.23 백앤드 작업
- 팔로우 구현
- 좋아요 수정
- 아바타 이미지 연동

> 서히
### 2023.05.23 프론트 작업


## 2023.05.24

> 준하
### 2023.05.24 백앤드 작업
- ChatGpt api 연결
- ChatGpt로 채팅하기 구현
- 추천 페이지 구상완료 -> api및 추천 알고리즘 구현필요
- map view 은행 목록 추가

> 서히
### 2023.05.24 프론트 작업
