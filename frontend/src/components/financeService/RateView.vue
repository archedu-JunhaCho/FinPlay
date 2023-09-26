<template>
  <div>
    <nav class="my-nav">
      <router-link to="/home">Home</router-link>
    </nav>
    <!-- 환율 화면 내용 -->
    <h1 class="back" style="margin-top: 18%;"> 환율 계산기</h1>
    <div style="margin: auto; margin-top: 100px;">
      <div class='rateSearch' style="margin: auto;">
        <div>
          <select name="" id="selbox" @change="selChange"></select>
        </div>
        <div >
          <input type="text" id ='changevalue' disabled @input="letsChange" v-model="user_input"> <p class="back1" v-if="show" style="text-align: center;"> {{ select_shapes }}</p>
        </div>
        <div style="font-family: Dovemayo_wild;"> 
          <input type="text" name="" id="" v-model="chage_rate" readonly> 원
        </div>
      </div>
      <br>
      <p class="back1" style="font-size: 12px;">* 엔화, 인도네시아 루피아는 100단위 / 나머지는 모두 1단위</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RateView',
  data() {
    return {
      rate : null,
      user_select : null,
      user_input : null,
      chage_rate : null,
      select_shapes : null,
      aboutChange : {},
      show : false,
    }
  },
  methods :{
    selChange(e) {
      const cv = document.getElementById('changevalue')
      this.user_select = e.target.value
      if (e.target.value == '선택') {
        this.show = false
        cv.disabled = true
      } else {
        this.select_shapes = this.aboutChange[this.user_select][1]
        this.show = true
        cv.disabled = false
      }
      this.user_input = null
      this.chage_rate = null
    },
    letsChange() {
      this.chage_rate = Math.round(this.aboutChange[this.user_select][0] * this.user_input)
    }
  },
  mounted() {
    console.log('mounted')
    this.$axios
        .get('http://127.0.0.1:8000/api/v3/listAllrate/', {
            headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            },
          })
        .then(res => {
          this.rate = res.data
          for (let i = 0; i < this.rate.length; i++) {
            const country = this.rate[i].deal_bas_r.replace(',','')
            const shape = this.rate[i].cur_unit
            this.aboutChange[this.rate[i].cur_nm] = [country, shape]
          }
        })
        .then ( () => {
          const selBox = document.getElementById('selbox')
          const option = document.createElement('option')
          option.text = '선택'
          selBox.appendChild(option)
          for (let i = 0; i < this.rate.length; i++) {
            const option = document.createElement('option')
            option.text = this.rate[i].cur_nm
            selBox.appendChild(option)
          }
        })
        .catch(err => {
          console.log(err)
        })
  },
  // 페이지에 접근시 환율정보 업데이트
  created() {
    this.$axios
        .get('http://127.0.0.1:8000/api/v3/loadRatedata/', {
            headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            },
          })
        .then((res)=>{
          console.log(res)
          console.log(res.data.reload)
          if (res.data.reload == true) {
            return this.$router.go()
          }
        })
  }
};
</script>

<style scoped>
/* 스타일 정의 */
nav {
  padding: 10px;
  text-align : right ;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  font-family: 'Dovemayo_wild', sans-serif; 
}

nav a.router-link-exact-active {
  color: #42b983;
}

 .back {
     font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 40px;
  }
  .back1 {
     font-family: 'Dovemayo_wild', sans-serif;
  font-size: 20px;
  }


.rateSearch {
  
  display: flex;
  flex-direction: row;
  justify-content: center;
  /* align-items: center; */
  width: 600px;
}

@font-face {
    font-family: 'SUITE-Regular';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2304-2@1.0/SUITE-Regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
}
select {
  /* 배경색과 테두리 스타일 변경 */
  width: 200px;
  background-color: #2c3e50;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: azure;
  
  /* 폰트와 패딩 설정 */
  font-family: Dovemayo_wild;
  padding: 8px;
  
  /* 드롭다운 화살표 스타일 변경 */
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  /* background-image: url('arrow.png'); */
  background-repeat: no-repeat;
  background-position: right center;
  padding-right: 20px;
}

input{
  width: 200px;
  font-family: Dovemayo_wild;
  padding: 8px;
  background-color: #2c3e50;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: azure;
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
