<template>

  <div> <!-- 이 div는 루트 요소입니다 -->
    <nav class="my-nav">
    <router-link to="/home">Home</router-link>
    </nav>
    <div v-if="this.before">
      <h1 class="back" style="margin-top: 10%;">MY 아바타 뽑기</h1>
      <img src="../../assets/question.gif" alt="" id="randomBox" ><br><br>

      <div class="container">
        <div class="button-wrapper" >
          <button @click="change" title="Button push black/gray"  class="back1 button btnBlackGray btnPush">지금 바로 뽑기</button>
          <div class="clear"></div>
        </div>
      </div>


     
      <br><p class="back1" v-if="lm">{{ loadingmessage }}</p>
    </div>
    <div v-if="this.after">
      <h2 class="back2" style="margin-top: 10%;">뽑기 결과</h2><br>
      <h5 class="back1">캐릭터 성격 : {{ userdata.avatar[0].personality }} </h5><br>
      <!-- <img src='../../../../Backend/media/media/whwnsgk830_avatar.jpg' alt="" id="randomBox"><br><br> -->
      <div style="border-radius: 20px;" class="test">
        <img :src="getImageUrl(`${this.userdata.username}_avatar.jpg`)" alt="캐릭터를 뽑는중입니다." id="randomBox"><br><br>
      </div><br><br><br>

      <div class="container">
      <div class="button-wrapper" >
        <button @click="change" title="Button push black/gray"  class="button btnBlackGray btnPush">Again</button>
        <div class="clear"></div>
        </div>
    </div>

      <p style="display: none;">{{imageUrl}}</p><br><br>
    </div>
  </div>

</template>

<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<script>
import axios from 'axios'
export default {
  name : 'avatar-view',
  data() {
    return {
      before : true,
      after : false,
      imageUrl : null,
      imageUrl2 : null,
      userdata : JSON.parse(localStorage.getItem('userdata')),
      loadingmessage : "캐릭터를 뽑는 중입니다.",
      lm : false
    }
  },
  methods : {
    getImageUrl(fileName){
      const random_num =  Math.random()
      return process.env.VUE_APP_BACKEND_API_URL + '/media/' + fileName + `?v=${random_num}`;
    },
    change() {
      /* eslint-disable */
      console.log('change');
      this.lm = !this.lm;
      
      const token = localStorage.getItem('access_token');
      if ( this.before==true ) {
        setTimeout(() =>{
          this.before = !this.before;
          this.after = !this.after;
          // this.lm = !this.lm;
        }, 2000)
        this.$axios
        .get('http://127.0.0.1:8000/useravatar/', {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: 'Token ' + token,
              // 'Access-Control-Allow-Origin': '*',
            },
            responseType: 'blob'
          })
        .then(res => {
            const imageUrl = URL.createObjectURL(res.data);
            this.imageUrl = imageUrl;

            const token = localStorage.getItem('access_token'); 
            // 회원정보 업데이트
            const config = {
              headers: {
                Authorization: 'Token ' + token,
              },
            }
            axios.get('http://127.0.0.1:8000/detailuser/', config)
            .then((response) => {
                const userdata = response.data;
                this.$store.dispatch('SET_USER', userdata);
                this.userdata = userdata.userdata;
                console.log(userdata.userdata)
              }
            )
        })
        .catch(err => {
          console.log(err)
        })
      } else {
        this.before = !this.before;
        this.after = !this.after;
      }
    },
  },

}
</script>
<style lang="scss">
@import "../../assets/scss/effect1.scss";
#randomBox {
  width: 300px;
  height: 300px;
  // border: 1px solid black;
  border-radius: 10px;
  margin-top: 50px;
  margin-bottom: 20px;
}


.container {
  padding-top: 1em;
  margin-top: 1em;
  margin-bottom: 1em;
  border-top : none;
  display: flex;
  align-items: center;
  justify-content: center;


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
  width: 150px;
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



 .back {
     font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 40px;
  }

     .back1 {
     font-family: 'Dovemayo_wild', sans-serif;
  font-size: 20px;
  }
.back2 {
     font-family: 'Dovemayo_wild', sans-serif;
  font-size: 30px;
  font-weight: bold;
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