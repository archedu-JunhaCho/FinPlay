<template>
    <!-- <h4>고객님을 위한 추천상품 리스트입니다</h4> -->
    <div style="font-family: Dovemayo_wild;">
        <nav class="my-nav" style="margin-bottom: 3%;">
            <router-link to="/home">Home</router-link> |
            <router-link to="/profileupdate" style="font-size: 20px;">상세프로필</router-link>
        </nav>
        <div v-if="!aretrue" style="margin-top: 20%; font-size: 40px;">
            <p>※ 프로필에 상세정보를 업데이트할시 추천상품을 받아보실 수 있습니다 <br> 프로필 업데이트후 추천까지 최소 1분의 시간의 소요됩니다. <br> 기다리는동안 그 외 다양한 서비스들을 이용해보세요 ※</p>
        </div>
        <div v-if="aretrue">
            <p>※ 프로필에 상세정보를 많이 입력할수록 정확한 추천상품을 받아보실수 있습니다 ※</p>
            <h3>당신의 아바타가 분석한 결과</h3>
            <div class="make_article" id="hello" style="width: 80%; margin: auto;">
                <!-- {{ answer_html }} -->
                1
            </div>
        </div>
        <!-- <button @click="showRecommend(), loadRecommend()">{{ recommendBtn }}</button> -->
        <div style="width: 80%; margin: auto;" v-if="aretrue">
            <hr>
            <h3>추천상품</h3>
            <p>※ 상품을 클릭하면 해당 상품 상세 페이지로 이동합니다 ※</p>
            <div class='rec_box bounce'>
                <div @click="gotoRecProduct(item[1], item[3].fin_prdt_cd)" class = 'rec_items shadow-drop-2-center' v-for="(item, index) in recommend_lst" :key="index">
                    <h5>{{item[3].kor_co_nm}}</h5>
                    <h5>{{item[3].fin_prdt_nm}}</h5>
                    <div>{{item[1]}}</div>
                    <!-- <div>{{item[0]}}</div>
                    <div>{{item[3]}}</div> -->
                </div>
            </div>
        </div>

    </div>




</template>

<script>
import axios from 'axios'
export default {
    name : "recommend-view",
    data() {
        return {
            answer : "사용자 정보를 분석해 상품을 추천중입니다. ",
            answer_html : null,
            rec_txt : null,
            aretrue : false,
            areRecommend : false,
            recommendBtn : '상품 추천 받기',
            recommend_lst : null
        }
    },
    methods : {
        showRecommend(){
            this.areRecommend = true
            this.recommendBtn = '다시 추천받기'
        },
        loadRecommend(){
            console.log('가자')

        },
        gotoRecProduct(kind, idd){
            console.log('추천상품 클릭, 이동합니다', kind, idd)
            
            if (kind == '예금') {
                this.$router.push(`/finance/deposit/detail/${idd}`)
            } else {
                this.$router.push(`/finance/installment/detail/${idd}`)
            }

        }
    },
    mounted() {
        console.log('추천 요청')
        const token = localStorage.getItem('access_token');
        console.log(token)
        axios.defaults.headers.common.Authorization = `Token ${token}`
        axios.get('http://127.0.0.1:8000/api/v2/recommend-products/1/', {
            headers: {
                "Content-Type": "multipart/form-data",
                Authorization: 'Token ' + token,
            },
        })
        .then((res)=>{
            this.answer_html = res.data.answer
            console.log('추천내용 저장',this.answer_html)
        })
        .then(()=>{
            const rec_inner = document.querySelector('.make_article')
            rec_inner.innerHTML = this.answer_html
        })
        .catch((err)=>{
            console.log(err)
        })

        // 나만의 추천상품 불러오기
        axios.get('http://127.0.0.1:8000/api/v2/recommend-products/top3/', {
            headers: {
                "Content-Type": "multipart/form-data",
                Authorization: 'Token ' + token,
            },
        })
        .then((res)=>{
            console.log(res)
            console.log(res.data.recommend)
            this.recommend_lst = res.data.recommend
        })
        .catch((err)=>{
            console.log(err)
        })
        
    },
    created() {
        /* eslint-disable */
    },
    watch : {
        answer_html(){
            if (this.answer_html){
                this.aretrue = true
            } else {
                this.aretrue = false
            }
        }
    }
}
</script>
<style scoped>
@keyframes bounce {
  0%, 100%, 20%, 53%, 80% {
    transition-timing-function: cubic-bezier(0.215, .61, .355, 1);
    transform: translate3d(0, 0, 0)
  }
  40%,
  43% {
    transition-timing-function: cubic-bezier(0.755, .050, .855, .060);
    transform: translate3d(0, -200px, 0)
  }
  70% {
    transition-timing-function: cubic-bezier(0.755, .050, .855, .060);
    transform: translate3d(0, -50px, 0)
  }
  90% {
    transform: translate3d(0, -4px, 0)
  }
}

.bounce {
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
  animation-name: bounce;
  transform-origin: center bottom
}
.rec_box{
    /* border: 1px solid black; */
    display: flex;
    justify-content: space-between;
}
.rec_items{
    border: 4px solid #2c3e50;
    margin: 1%;
    width: 25%;
    height: 200px;
    padding: 50px;
    background-color: #2c3e50;
    color: white;
    border-radius: 14px;
}


.make_article{
    min-height: 300px;
    border: 1px solid #2c3e50;
    margin: 1%;
    padding: 50px;
    font-family: Dovemayo_wild;
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

.shadow-drop-2-center:hover {
	-webkit-animation: shadow-drop-2-center 0.4s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
	        animation: shadow-drop-2-center 0.4s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}


@keyframes shadow-drop-2-center {
  0% {
    -webkit-transform: translateZ(0);
            transform: translateZ(0);
    -webkit-box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  }
  100% {
    -webkit-transform: translateZ(50px);
            transform: translateZ(50px);
    -webkit-box-shadow: 0 0 50px 20px rgba(0, 0, 0, 0.35);
            box-shadow: 0 0 50px 20px rgba(0, 0, 0, 0.35);
  }
}


</style>
