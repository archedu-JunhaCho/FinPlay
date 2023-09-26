<template>
  <div class="sign-up">
    <nav class="back my-nav" style="margin-bottom: 10%;">

    <router-link to="/home">Home</router-link> 
    </nav>
    <p class="title">회원가입</p>
    <div style="margin: 40px;">
      <input class="back5"  @keyup.enter="tryRegister" type="text" placeholder="id" v-model="user_id"><br>
      <input class="back5" @keyup.enter="tryRegister" type="text" placeholder="email" v-model="user_email"><br>
      <input class="back5" @keyup.enter="tryRegister" type="password" placeholder="password" v-model="user_password1"><br>
      <input class="back5" @keyup.enter="tryRegister" type="password" placeholder="password check" v-model="user_password2"><br>
    </div>
    <p class="error-message">다음을 확인하세요 <br>{{ error_msg }}</p>
    <button title="Button push black/gray"  class="back5 button btnBlackGray btnPush" style="margin: auto;" @click="tryRegister">가입하기</button>
    <span class="back">또는 <router-link to="/login">로그인</router-link>으로 돌아가기</span>
  </div>
</template>

<script>
  export default {
    name: 'signUp',
    data() {
      return {
        // 유저가 기입한 회원가입 정보
        user_id : '',
        user_email : '',
        user_password1 : '',
        user_password2 : '',
        userdata : null,

        // 에러메세지
        error_msg : '',
      }
    },
    methods: {
      // 회원가입 시도시
      tryRegister() {
        const formdata = {
          username : this.user_id,
          email : this.user_email,
          password1 : this.user_password1,
          password2 : this.user_password2
        }
        console.log(formdata)
        this.$axios.post('http://127.0.0.1:8000/accounts/signup/', formdata, {
          // 헤더정보는 CORS에 필요하다고하여 작성
          headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            },
          })
          // 회원가입 성공시
          .then(res => {  
              console.log(res)
              window.alert('회원가입에 성공하셨습니다.')
              this.user_id = ''
              this.user_email = ''
              this.user_password1 = ''
              this.user_password2 = ''

            // 로그인 창으로 바로 넘어가도록
            this.$router.push('/login');
            })
          // 회원가입 실패시
          .catch(err => {
            console.log(err)
            const error_msg = err.request.response
            console.log('에러메세지는', error_msg)
            const real_error = JSON.parse(error_msg)
            this.error_msg = real_error
            window.alert('오류 메세지를 확인하세요.')
          })
        },
      },
      watch : {
        // 에러메세지 받아올시 띄우기
        error_msg(){
          if (this.error_msg !='') {
            const e1 = document.querySelector('.error-message')
            e1.style.display = 'block'
          }
        }
      }
  }
</script>

<style scoped>
nav {
  padding: 20px;
  text-align : left ;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.title {
   font-family: 'Dovemayo_wild', sans-serif;
  font-size: 40px;
}

.sign-up {
  margin-top: 0px;
}
  input {
    margin: 10px 0;
    width: 20%;
    padding: 15px;
  }
  button {
    margin-top: 20px;
    width: 10%;
    cursor: pointer;
  }
  p {
    margin-top: 40px;
    font-size: 20px;
  }
  span {
    display: block;
    margin-top: 20px;
    font-size: 15px;
  }

  .error-message{
    display: none;
    color : red;
    width: 50%;
    margin: auto;
    font-size : 12px
  }

  .back {
     font-family: 'Dovemayo_wild', sans-serif;
  font-size: 20px;
  }
   .back5 {
     font-family: 'Dovemayo_wild', sans-serif;
  font-size: 15px;
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

.back5{
  font-family: 'Dovemayo_wild', sans-serif;
  font-size: 15px;
}
</style>