<template>
  <div>
    <nav class="my-nav">
      <router-link to="/home">Home</router-link>
    </nav>
    <h1 class="back" style="margin-top: 1.5%;">은행 검색</h1><br>
    <!-- 지도 화면 내용 -->
    <div class="map_wrap">
      <div id="menu-wrap" class="bg-white">
        <div class="option">
          <div >
            <div style="display: flex; justify-content: center;">
            <div class="selBox">
              <select @click='loadSelect' @change="changeSelect1" name="addressRegion" id="addressRegion2" style="width:100px ">
                <option>시/도 선택</option>
              </select>
            </div>
            <div class="selBox">
              <select @change="changeSelect2" name="addressDo" id="addressDo2" style="width:100px">
                <option>구/군 선택</option>
              </select>
            </div>
            <div class="selBox">
              <select @change="changeSelect3">
                <option>은행 선택</option>
                <option v-for="(item, index) in bank" :key="index">{{item}}</option>
              </select>
            </div>             
            <button  class="serBTN"  @click="searchPlaces">검색하기</button>
          </div>
          </div>
        </div><br>
        <hr>
        <ul id="placesList"></ul>
        <div id="pagination"></div>
      </div>
      <div id="map" style="width:80%;height:160%;position:relative;overflow:hidden; margin: auto;"></div>
    </div>
    
    

  </div>
</template>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script >
export default {
  name: 'MapView',
  data() {
      return {
          map:null,
          markers:[],
          infowindow : [],
          sel_city : null,
          sel_region : null,
          bank :  [
              "우리은행",
              "부산은행",
              "광주은행",
              "제주은행",
              "전북은행",
              "경남은행",
              "국민은행",
              "신한은행",
              "하나은행",
          ],
          banksel : '은행',
          area : {
            sel1 : ["서울특별시","인천광역시","대전광역시","광주광역시","대구광역시","울산광역시","부산광역시","경기도","강원도","충청북도","충청남도","전라북도","전라남도","경상북도","경상남도","제주특별자치도"],
            sel2 : {
              "서울특별시" : ['구/군 선택',"강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"],
              "인천광역시" : ['구/군 선택',"계양구","미추홀구","남동구","동구","부평구","서구","연수구","중구","강화군","옹진군"],
              "대전광역시" : ['구/군 선택',"대덕구","동구","서구","유성구","중구"],
              "광주광역시" : ['구/군 선택',"광산구","남구","동구","북구","서구"],
              "대구광역시" : ['구/군 선택',"남구","달서구","동구","북구","서구","수성구","중구","달성군"],
              "울산광역시" : ['구/군 선택',"남구","동구","북구","중구","울주군"],
              "부산광역시" : ['구/군 선택',"강서구","금정구","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구","기장군"],
              "경기도" : ['구/군 선택',"고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시","가평군","양평군","여주군","연천군"],
              "강원도" : ['구/군 선택',"강릉시","동해시","삼척시","속초시","원주시","춘천시","태백시","고성군","양구군","양양군","영월군","인제군","정선군","철원군","평창군","홍천군","화천군","횡성군"],
              "충청북도" : ['구/군 선택',"제천시","청주시","충주시","괴산군","단양군","보은군","영동군","옥천군","음성군","증평군","진천군","청원군"],
              "충청남도" : ['구/군 선택',"계룡시","공주시","논산시","보령시","서산시","아산시","천안시","금산군","당진군","부여군","서천군","연기군","예산군","청양군","태안군","홍성군"],
              "전라북도" : ['구/군 선택',"군산시","김제시","남원시","익산시","전주시","정읍시","고창군","무주군","부안군","순창군","완주군","임실군","장수군","진안군"],
              "전라남도" : ['구/군 선택',"광양시","나주시","목포시","순천시","여수시","강진군","고흥군","곡성군","구례군","담양군","무안군","보성군","신안군","영광군","영암군","완도군","장성군","장흥군","진도군","함평군","해남군","화순군"],
              "경상북도" : ['구/군 선택',"경산시","경주시","구미시","김천시","문경시","상주시","안동시","영주시","영천시","포항시","고령군","군위군","봉화군","성주군","영덕군","영양군","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군"],
              "경상남도" : ['구/군 선택',"거제시","김해시","마산시","밀양시","사천시","양산시","진주시","진해시","창원시","통영시","거창군","고성군","남해군","산청군","의령군","창녕군","하동군","함안군","함양군","합천군"],
              "제주특별자치도" : ['구/군 선택',"서귀포시","제주시",]
            }
          },
          
          
      };
  },
  methods: {
    loadSelect(){
      const insertSel = document.getElementById("addressRegion2");
      for (let i = 0; i < this.area.sel1.length; i++) {
        const option = document.createElement("option");
        option.innerText = this.area.sel1[i];
        insertSel.appendChild(option)
      }
    },
    changeSelect1(event){
      console.log(event.target.value);
      const insertSel = document.getElementById("addressDo2");
      if (event.target.value != '시/도 선택') {
        this.sel_city = event.target.value;
        insertSel.replaceChildren()
        for (let i = 0; i < this.area.sel2[event.target.value].length; i++) {
          const option = document.createElement("option");
          option.innerText = this.area.sel2[event.target.value][i];
          insertSel.appendChild(option)
        }
      } else {
        this.sel_city = null;
        insertSel.replaceChildren()
        const option = document.createElement("option")
        option.innerText = '구/군 선택'
        insertSel.appendChild(option)
      }
    },
    changeSelect2(event){
      if (event.target.value != '구/군 선택') {
        this.sel_region = event.target.value;
      } else {
        this.sel_region = null;
      }
    },
    changeSelect3(event){
      console.log(event.target.value)
      if (event.target.value == '은행 선택') {
        this.banksel = '은행'
      } else { this.banksel = event.target.value }
      
    },
    loadScript() {
      let script = document.createElement("script");
      script.src =
        "//dapi.kakao.com/v2/maps/sdk.js?appkey=7df4675970ee62f9b4ec6c45547d828c&autoload=false&libraries=services"; // &autoload=false api를 로드한 후 맵을 그리는 함수가 실행되도록 구현
      script.onload = () => window.kakao.maps.load(this.loadMap); // 스크립트 로드가 끝나면 지도를 실행될 준비가 되어 있다면 지도가 실행되도록 구현

      document.head.appendChild(script); // html>head 안에 스크립트 소스를 추가
    },
    loadMap() {
      let container = document.getElementById("map"); // 지도를 담을 DOM 영역
      let options = {
        // 지도를 생성할 때 필요한 기본 옵션
        center: new window.kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 3, // 지도의 레벨(확대, 축소 정도)
      };

      this.map = new window.kakao.maps.Map(container, options); // 지도 생성 및 객체 리턴
      this.ps = new window.kakao.maps.services.Places();
      this.infowindow = new window.kakao.maps.InfoWindow({zIndex:1});
      // console.log(this.map, ps);
      console.log('로드 완료')
    },
    searchPlaces() {
      let keyword = this.sel_city + ' ' + this.sel_region +' ' + this.banksel
      if (this.sel_city == null || this.sel_region == null) {
        window.alert('지역을 선택해주세요')
      } else {
        this.ps.keywordSearch(keyword, this.placesSearchCB);
      }
      console.log(keyword)
    },
    placesSearchCB (data, status){
      if (status === window.kakao.maps.services.Status.OK) {
          console.log('검색결과로 불러온 데이터는', data)
          // 정상적으로 검색이 완료됐으면
          // 검색 목록과 마커를 표출합니다
          this.displayPlaces(data);
          // 페이지 번호를 표출합니다
          // this.displayPagination(pagination);

      } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
          alert('검색 결과가 존재하지 않습니다.');
          return;
      } else if (status === window.kakao.maps.services.Status.ERROR) {
          alert('검색 결과 중 오류가 발생했습니다.');
          return;
      }
    },
    displayPlaces(places){
      let listEl = document.getElementById('placesList');
      const menuEl = document.querySelector('#menu-wrap');
      let fragment = document.createDocumentFragment();
      let bounds = new window.kakao.maps.LatLngBounds();
      // const listStr = '';
      this.removeAllChildNods(listEl)
      this.removeMarker();

      for ( var i=0; i<places.length; i++ ) {

        // 마커를 생성하고 지도에 표시합니다
        let placePosition = new window.kakao.maps.LatLng(places[i].y, places[i].x)
        this.marker = this.addMarker(placePosition, i)
        let itemEl = this.getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);
        const displayInfowindow= (marker, title) => {
            let content = '<div style="padding:5px;z-index:1;">' + title + '</div>';
            this.infowindow.setContent(content);
            this.infowindow.open(this.map, marker);
        };
        const tmpinfo = this.infowindow;
        (function(marker, title) {
            window.kakao.maps.event.addListener(marker, 'mouseover', function() {
              displayInfowindow(marker, title);
            });
            window.kakao.maps.event.addListener(marker, 'mouseout', function() {
              tmpinfo.close();
            });
            itemEl.onmouseover =  function () {
              displayInfowindow(marker, title);
            };
            itemEl.onmouseout =  function () {
              tmpinfo.close();
            };
        }) (this.marker, places[i].place_name);
        fragment.appendChild(itemEl);
      }
      listEl.appendChild(fragment);
      menuEl.scrollTop = 0;
      this.map.setBounds(bounds);
    },
    // displayPagination(pagination){
    //   let paginationEl = document.getElementById('pagination'),
    //     fragment = document.createDocumentFragment(),
    //     i; 

    //   // 기존에 추가된 페이지번호를 삭제합니다
    //   while (paginationEl.hasChildNodes()) {
    //       paginationEl.removeChild (paginationEl.lastChild);
    //   }

    //   for (i=1; i<=pagination.last; i++) {
    //       let el = document.createElement('a');
    //       el.href = "#";
    //       el.innerHTML = i;

    //       if (i===pagination.current) {
    //           el.className = 'on';
    //       } else {
    //           el.onclick = (function(i) {
    //               return function() {
    //                   pagination.gotoPage(i);
    //               }
    //           })(i);
    //       }

    //       fragment.appendChild(el);
    //   }
    //   paginationEl.appendChild(fragment);
    // },
    removeAllChildNods(el) {   
      while (el.hasChildNodes()) {
          el.removeChild (el.lastChild);
      }
    },
    removeMarker() {
      for ( var i = 0; i < this.markers.length; i++ ) {
          this.markers[i].setMap(null);
      }   
      this.markers = [];
    },
    addMarker(position, idx) {
      const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png' // 마커 이미지 url, 스프라이트 이미지를 씁니다
      const imageSize = new window.kakao.maps.Size(36, 37)  // 마커 이미지의 크기
      const imgOptions =  {
            spriteSize : new window.kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
            spriteOrigin : new window.kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
            offset: new window.kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        }
      
      const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions)
      const marker = new window.kakao.maps.Marker({
            position: position, // 마커의 위치
            image: markerImage 
        });

    marker.setMap(this.map); // 지도 위에 마커를 표출합니다
    this.markers.push(marker);  // 배열에 생성된 마커를 추가합니다
    return marker;
    },
    getListItem(index, places) { 
      /* eslint-disable */
      const el = document.createElement('li') 
      el.setAttribute('style','list-style: none; border: 1px solid black;')
      let itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                  '<div class="info" style="font-family: KyoboHandwriting2022khn; margin:auto;">' +
                  '   <p style="font-size: 12px">' + places.place_name + '</p>';          
      if (places.road_address_name) {
          itemStr += '    <span>' + places.road_address_name + '</span>' + 
                      '   <span class="jibun gray">' +  places.address_name  + '</span>';
      } else {
          itemStr += '    <span>' +  places.address_name  + '</span>'; 
      } 
                  
        itemStr  += '  <span class="tel">' + places.phone  + '</span>' + 
                  '</div>' ;            
      el.innerHTML = itemStr;
      el.className = 'item';

      return el;
    },
    displayInfowindow(marker, title) {
      let content = '<div style="padding:5px;z-index:1;">' + title + '</div>';
      this.infowindow.setContent(content);
      this.infowindow.open(map, marker);
    }
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      // 카카오 객체가 있고, 카카오 맵그릴 준비가 되어 있다면 맵 실행
      console.log('맵을 실행합니다.')
      this.loadMap();
    } else {
      console.log('스크립트를 추가합니다.')
      // 없다면 카카오 스크립트 추가 후 맵 실행
      this.loadScript();
    }
  }
};
</script>



<style scoped>
/* 스타일 정의 */



 .back {
     font-family: 'Dovemayo_wild', sans-serif; 
     font-size: 40px;
      font-weight: bold;
  }

nav {
  padding: 10px;
  text-align : right ;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.item {
  font-size: 140px;
  background-color: #009900 !important;
}

.map_wrap, .map_wrap * {margin:0;padding:0;font-family:'Malgun Gothic',dotum,'돋움',sans-serif;font-size:12px;}
.map_wrap a, .map_wrap a:hover, .map_wrap a:active{color:#000;text-decoration: none;}
.map_wrap {position:relative;width:100%;height:500px;}
#menu_wrap {position:absolute;top:0;left:0;bottom:0;width:250px;margin:10px 0 30px 10px;padding:5px;overflow-y:auto;background:rgba(255, 255, 255, 0.7);z-index: 1;font-size:12px;border-radius: 10px;}
.bg_white {background:#fff;}
#menu_wrap hr {display: block; height: 1px;border: 0; border-top: 2px solid #5F5F5F;margin:3px 0;}
#menu_wrap .option{text-align: center;}
#menu_wrap .option p {margin:10px 0;}  
#menu_wrap .option button {margin-left:5px;}

#placesList .item .marker_1 {background-position: 0 -10px;}
#placesList .item .marker_2 {background-position: 0 -56px;}
#placesList .item .marker_3 {background-position: 0 -102px}
#placesList .item .marker_4 {background-position: 0 -148px;}
#placesList .item .marker_5 {background-position: 0 -194px;}
#placesList .item .marker_6 {background-position: 0 -240px;}
#placesList .item .marker_7 {background-position: 0 -286px;}
#placesList .item .marker_8 {background-position: 0 -332px;}
#placesList .item .marker_9 {background-position: 0 -378px;}
#placesList .item .marker_10 {background-position: 0 -423px;}
#placesList .item .marker_11 {background-position: 0 -470px;}
#placesList .item .marker_12 {background-position: 0 -516px;}
#placesList .item .marker_13 {background-position: 0 -562px;}
#placesList .item .marker_14 {background-position: 0 -608px;}
#placesList .item .marker_15 {background-position: 0 -654px;}

/* #pagination {margin:10px auto;text-align: center;}
#pagination a {display:inline-block;margin-right:10px;}
#pagination .on {font-weight: bold; cursor: default;color:#777;} */

#placesList {
  /* background-color: #009900; */
  font-size: 10px;
  display: flex;
};

#placesList li{
  /* background-color: #233823; */
  width: 300px;
  text-align: center;
}
select{
  height: 30px;
  background-color: #ffffff;
  border: 1px solid rgb(57, 57, 57);
  border-radius: 10px;
  font-family: 'Dovemayo_wild'; 
  font-size: 40px;
  font-weight: bold;
}
option{
  font-family: 'Dovemayo_wild'; 
  font-size: 40px;
  font-weight: bold;
}
.selBox{
  margin: 5px;
}
.serBTN{
  border: 1px solid black;
  background-color: #ffffff;
  border-radius: 10px;
  width: 100px;
  height: 30px;

  margin-top: auto;
  margin-bottom: auto;
  font-weight: bold;
  margin-left: 8px;
}

.info{
  border: 1px solid black !important;
  margin: auto;
}
@font-face {
    font-family: 'KyoboHandwriting2022khn';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2304-2@1.0/KyoboHandwriting2022khn.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}
.my-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50;
  padding: 10px;
  height: 4rem;
}

.my-nav a {
    font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
  margin-right: 10px;
}

.my-nav a:hover {
  color: #42b983;
}
</style>
