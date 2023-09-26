<template>
  <div class="login">
    <nav class="my-nav" style="margin-bottom: 10%;">
      <router-link to="/home">Home</router-link>
    </nav>
    <div>
      <h3 class="title">Login</h3>
      <div style="margin: 40px;">

        <input class="back5" @keyup.enter="tryLogin" type="text" placeholder="id" v-model="username"><br>
        <input class="back5" @keyup.enter="tryLogin" type="password" placeholder="password" v-model="password"><br>
        
      </div>
    </div>
    <p class="error-message">다음을 확인하세요 <br>{{ error_msg }}</p>
    <button title="Button push black/gray"  class="back5 button btnBlackGray btnPush" style="margin: auto;" @click="tryLogin({username, password})">로그인</button><br><br>
    <span class="back">만약 계정이 없다면, <router-link to="/register">회원가입</router-link>을 먼저 진행해주세요!</span>
  </div>
</template>

<script>
// import { mapState, mapActions } from 'vuex'
import axios from 'axios'



  export default {
    name: 'LoginView',
    data() {
      return {
        // 유저가 기입한 로그안 정보
        username : '',
        password : '',
        // 에러메세지
        error_msg : ''
      }
    },
    // conputed : {
    //   ...mapState(['isLogin', 'isLoginError'])
    // },
    methods: {
      // 로그인 시도시
      tryLogin() {
        const formdata = {
          username : this.username,
          password : this.password,
        }
        console.log(formdata)
        this.$axios
        .post('http://127.0.0.1:8000/accounts/login/', formdata, {
            headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            },
          })
        .then(res => {
            console.log(res)
            // 토큰 저장
            const token = res.data.key
            localStorage.setItem('access_token', token)
            // const refretoken = res.data.refresh_token
            // localStorage.setItem('refresh_token', refretoken)
            
            // 회원정보 불러오기
            const config = {
              headers: {
                Authorization: 'Token ' + token,
              },
            }
            this.username = ''
            this.password = ''
            axios.get('http://127.0.0.1:8000/detailuser/', config)
            .then((response) => {
                console.log('사용자정보는',response)
                const userdata = response.data;
                // 변이 호출하여 state 업데이트
                this.$store.dispatch('SET_USER', userdata);
              }
            )

            // 로그인 액션을 호출하여 로그인 상태 변경
            this.$store.dispatch('login');


            // 로그인상태 유지 (토큰 기본으로 실어서 보내도록 설정)
            axios.defaults.headers.common.Authorization = `Token ${token}`
            window.alert('로그인에 성공하셨습니다.')

            //state 데이터 값 변경
            // this.$store.commit('setUsername', data.user.username)
            // this.$store.commit('setUseremail', data.user.email)

            
            // 홈 창으로 바로 넘어가도록
            setTimeout(() =>{
              this.$router.push('/home');
            }, 100);
          })
          .catch(err => {
            console.log(err)
            const error_msg = err.request.response
            console.log('에러메세지는', error_msg)
            const real_error = JSON.parse(error_msg)
            console.log(typeof real_error)
            this.error_msg = real_error
            window.alert('오류 메세지를 확인하세요.')
          })
        },
    //     tryLogout() {
    //   // 로그아웃 액션을 호출하여 로그인 상태 변경
    //   this.$store.dispatch('logout');

    //   // 로그인 페이지로 리다이렉트
    //   this.$router.push('/login');
    // },
      },
      watch : {
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
.my-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  padding: 10px;
}

.my-nav a {
       font-family: 'Dovemayo_wild', sans-serif;
  font-size: 20px;

  font-weight: bold;
  color: #333;
  text-decoration: none;
  margin-right: 10px;
}

.my-nav a:hover {
  color: #42b983;
}

.title {
  font-family: 'Dovemayo_wild', sans-serif;
  font-size: 40px;
  font-weight: bold;
  color: #333;
  margin-top: 20px;
}

.my-button {
  font-family: 'Dovemayo_wild', sans-serif;
  font-size: 15px;

  font-weight: bold;
  color: #333;
  background-color: #f8f9fa;
  padding: 10px;
  text-decoration: none;
  cursor: pointer;
}

.my-button:hover {
  color: #42b983;
  
}

 .back {
     font-family: 'Dovemayo_wild', sans-serif;
  font-size: 20px;
  }
   .back1 {
     font-family: 'Dovemayo_wild', sans-serif;
  font-size: 15px;
  }

.login {
  margin-top: 0px;
}

input {
  margin: 10px 0;
  width: 20%;
  padding: 15px;
}

.error-message {
  display: none;
  color: red;
  width: 50%;
  margin: auto;
  font-size: 12px;
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