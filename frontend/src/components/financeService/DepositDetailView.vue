<template>
  <div>
    <nav class="my-nav">
      <div class="home">
        <router-link to="/home">Home</router-link>
      </div>
      <div class="bind">
      <a href="#" @click="goback">정기예금</a> |
      <router-link to="/finance/installment">정기적금</router-link> 
    </div>
    </nav>



  

    <!-- {{ userdepositlst }} <br>
    {{ btnValue }} <br> -->

    <h1 class="back">예금 Details</h1><br>

 

 <div  v-if="deposit">

  <div class="deposit-box">

    <p style="font-weight: bold;">은행이름 : <span style="font-weight: normal;">{{ deposit.kor_co_nm }}</span></p>
    <p style="font-weight: bold;"> 상품이름 : <span style="font-weight: normal;">{{ deposit.fin_prdt_nm }} </span> </p>
    <div class="sample">
      <p style="font-weight: bold;">SAMPLE : </p>
      <div v-for="(line, index) in deposit.etc_note.split('\n')" :key="'info1_'+index">
          <p >
          {{ line.includes(':') ? line.split(':')[0].trim() + ': ' + line.split(':')[1].trim() : line.trim() }}
          </p>
      </div>
    </div>

    <!-- <p> 뭐야 이건 : {{ deposit.join_deny }} </p> -->
    <p style="font-weight: bold;"> join_member : <span style="font-weight: normal;">{{ deposit.join_member }}</span> </p>
    <p style="font-weight: bold;"> join_way: <span style="font-weight: normal;">{{ deposit.join_way }}</span> </p>
    <p style="font-weight: bold;"> 특이사항 </p>

    <div v-for="(line, index) in deposit.spcl_cnd.split('\n')" :key="'info2_'+index">
        <p style="font-weight: normal;">
        {{ line.includes(':') ? line.split(':')[0].trim() + ': ' + line.split(':')[1].trim() : line.trim() }}
        </p>
    </div>
    <p style="font-weight: bold;"> 공시일자 : <span style="font-weight: normal;">{{ deposit.dcls_month.slice(0, 4) + '년 ' + deposit.dcls_month.slice(4, 6) + '월' }}</span> </p>
    <p style="font-weight: bold;"> 월별 이자율 </p>
        <div>
          <ul>
              <li style="font-weight: normal;" v-for="(option, index) in deposit.depositoptions_set" :key="'info3_'+index">
                  {{ option.save_trm }}개월 : {{ option.intr_rate }}%
              </li>
          </ul>
        </div>
  </div>
  </div>
   <div class="container">
    <div class="button-wrapper" >
      <button @click="joinDepoist()" title="Button push black/gray"  class="button btnBlackGray btnPush">{{ btnValue }}</button>
      <div class="clear"></div>
    </div>
  </div>
  
    <!-- Other deposit details here -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DepositDetailView',
  data() {
    return {
      deposit: null,
    };
  },
  methods: {
    goback(){
      this.$router.back();
    },
    joinDepoist() {
      if (this.btnValue == '가입하기') {
        window.alert('가입이 완료되었습니다')
      } else {
        window.alert('탈퇴 되었습니다')
      }
      // DB api요청 -> 스토어에 저장 -> 로컬스토리지 저장
      const token = localStorage.getItem('access_token');
      this.$axios
      .get(`http://127.0.0.1:8000/api/v2/deposit-products/${this.$route.params.id}/signin`, {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: 'Token ' + token,
            },
          })
          .then(res => {
            console.log(res)

            const userdata = res.data;
            this.$store.dispatch('SET_USER', userdata);
            
            
          }
          )
          .catch(err => {
            console.log(err)
          })
    }
  },
  async created() {
      try {
      const id = this.$route.params.id;
      const response = await axios.get(`http://127.0.0.1:8000/api/v2/deposit-products/${id}`);
      this.deposit = response.data;
    } catch (error) {
      console.log(error);
    }
  },
  computed : {
    // 가입정보 불러오기
    userdepositlst () {
      return this.$store.state.UserData.product_lst
    },
    // 가입여부 검증
    btnValue () {
      if (this.userdepositlst){
        if (this.userdepositlst.includes(`${this.$route.params.id}`) ) {
      
          return '탈퇴하기'
        } else {
        
          return '가입하기'
        }
      } else {
 
        return '가입하기'
      }
    }
  },
};
</script>

<style scoped>
@import url(https://fonts.googleapis.com/css?family=Josefin+Slab:100,300,400,600,700);





 .back {
     font-family: 'Dovemayo_wild', sans-serif; 
    font-size: 40px;
    margin-top: 40px;
  }

.container {
  padding-top: 0px;
  margin-top: 0px;
  margin-bottom: 1em;
 
  display: flex;
  align-items: center;
  justify-content: center;
   border-top: none;


}

.button-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.button {
  /* display: block;
  position: relative; */
  display: flex;
  justify-content: center;
  width: 100px;
  height: 50px;
  padding: 0;
  margin: 10px 0;
  font-weight: 600;
  text-align: center;
  line-height: 50px;
  color: #FFF;
  border-radius: 5px;
  transition: all 0.2s;
   font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;
  text-decoration: none;
  border: none;
 
}

.btnBlackGray.btnPush {
  box-shadow: 0px 5px 0px 0px rgba(0, 0, 0, 0.3);
}

.btnBlackGray.btnPush:hover {
  box-shadow: 0px 2px 0px 0px rgba(0, 0, 0, 0.3);
  transform: translateY(3px);
}



.btnBlackGray {
  background: gray;
}
.clear {
  clear: both;
}

.deposit-box {
  width: 800px;
  display: inline-block;
  padding: 10px;
  max-height: calc(100vh - 60px); /* 브라우저 창 높이에서 60px를 뺀 값 */
  text-align: left;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-top: 20px;
  margin-bottom: 20px;
  background-color: #FFFFFF;
  color: #333333;
  border: 1px solid #CCCCCC;
  margin-left: auto;
  margin-right: auto;
  font-family: 'Dovemayo_wild', sans-serif;
  font-size: 20px;
  border-radius: 10px; 
  overflow: auto;
}


.deposit-box:-webkit-scrollbar {
  width: 10px; /* 스크롤 막대 너비 */
}
.deposit-box:-webkit-scrollbar-thumb {
  background-color: grey; /* 스크롤 막대 색상 */
}

.deposit-box .header { font-size: 14px; padding: 15px 0; background: #464545; color: white; text-align: center; border-start-end-radius: 15px; border-top-left-radius: 15px;}




.sample {
  border: #CCC 2px solid;
  padding-block-start: 10px;
  padding-block-end: 5px;
  padding-inline-start: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
