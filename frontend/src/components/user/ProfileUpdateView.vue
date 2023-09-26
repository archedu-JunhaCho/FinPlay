<template>
  <div class="profile">
    <nav class="my-nav">
    <a href="#" @click="goback">뒤로가기</a> |
    <router-link to="/home">Home</router-link> 
    </nav>
    <p style="display:none"> 컴퓨티드로 계산한 forsave : {{ forsave }} <br></p>
    <p style="display:none"> 데이터로 저장한 formdata : {{ formdata }} </p>
    <!-- 업데이트 폼 -->
    <div class="BigBox" style="margin-top: 3%;">
      <h1 class="back">Profile Update</h1>
      <br>
      <p v-for="(items, key, index) in formdata" :key="index">
        <span class="back1" v-if="['username','email','name','age',].includes(key)"><p >{{key}} : </p> <input type="text" v-model="formdata[key]"></span>
      </p>
      <p><span class="back1" > <p >gender : </p>
        <select @change="ChangeSex">
          <option value=null></option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select></span></p>
      <!-- select options -->
      <div >
        <button class = 'optionBtn' v-for="(item, index) in all_options" :key=index @click="btnClick">{{item}}</button>
      </div>
      <br><p style="font-size: 17px; font-family: Dovemayo_wild;">※ 업데이트를 진행할시 추천상품을 받아보실 수 있습니다 ※</p>
      <div class="container">
        <div class="button-wrapper" >
          <button href="" @click="updateProfile" title="Button push black/gray"  class="button btnBlackGray btnPush">Update</button>
          <div class="clear"></div>
        </div>
      </div>
    </div>

    
<div class="BigBox"><br>
<h3 class="back">Change Password</h3><br>

    <div>
      <label class="back1" style="margin-right:5px" for="newPassword">New Password : </label>
      <input class="back2" type="password" id="newPassword" v-model="user_newPassword">
    </div><br>
    <div>
      <label class="back1" style="margin-right:5px" for="confirmPassword">Confirm Password : </label>
      <input class="back2" type="password" id="confirmPassword" v-model="user_confirmPassword">
    </div><br>
    <div class="container">
        <div class="button-wrapper" >
          <button href="" @click="changePassword()" title="Button push black/gray"  class="button btnBlackGray btnPush">Change</button>
          <div class="clear"></div>
        </div>
      </div>
  </div>

<hr>
  <div style="margin-top:20px;">
  <div class="container">
        <div class="button-wrapper" >
          <p class="back">회원 탈퇴</p><br><br>
          <button href="" @click="deleteuser()" title="Button push black/gray"  class="button btnBlackGray btnPush" style="margin-left: 40px;">Delete</button>
          <div class="clear"></div>
        </div>
      </div>
      <div style="margin-bottom:100px;"></div>
</div>
</div>

    
</template>

<script>
// import { mapState } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      user_name: '',
      user_age: '',
      user_gender: '',
      user_newPassword: '',
      user_confirmPassword: '',

      // 에러메세지
      error_msg : '',

      // 유저 정보 업데이트 폼
      formdata : {
        username : '',
        email : '',
        name : '',
        age : '',
        gender : '',
        password : '',
        is_active : '',
      },

      // 옵션
      all_options : []
    };
  },
  methods: {
    ChangeSex(e){
      // console.log(e.target.value)
      this.formdata.gender = e.target.value
    },
    // 뒤로가기
    goback(){
      this.$router.back();
    },
    // 프로필 업데이트
    updateProfile() {
      console.log(this.formdata)
      let formdata = this.formdata
      // 서버에 사용자 정보 업데이트 요청 보내기
      this.$axios.put('http://127.0.0.1:8000/updateuser/', formdata, {
          // 헤더정보는 CORS에 필요하다고하여 작성
          headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            },
        })
      .then(res => {
        console.log(res)
        alert('업데이트 성공')
        
        // 토큰 저장
        // const token = res.data.key
        // localStorage.setItem('access_token', token)
        const config = {
              params : {
                username : this.formdata.username
              }
            }
        // 유저 정보 업데이트
        axios.get('http://127.0.0.1:8000/detailuser/', config)
        .then((response) => {
            console.log('사용자정보를 업데이트 합니다.',response)
            const userdata = response.data;

            // 변이 호출하여 state 업데이트
            this.$store.dispatch('SET_USER', userdata);
        })
        .catch((error) => {
          console.log(error);
        })

        // 아바타의 추천 문구만들기 API
        axios.get('http://127.0.0.1:8000/api/v2/recommend-products/',{
          headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            }})
          .then((res)=>{
            console.log(res,'추천 api 전송')
          })
          .catch((err)=>{
            console.log(err)
          })

      })
      .catch(err => {
        console.log(err)
        const error_msg = err.request.response
        console.log('에러메세지는', error_msg)
        const real_error = JSON.parse(error_msg)
        this.error_msg = real_error
        alert('오류 메세지를 확인하세요.')
      })

      // 유저 키워드 생성
      axios.get('http://127.0.0.1:8000/api/v2/user-keyword/',{
          headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            }})
          .then((res)=>{
            console.log(res,'유저 키워드 생성 완료')
          })
          .catch((err)=>{
            console.log(err,'유저 키워드 생성 실패')
          })
    },
      

    // 비밀번호 변경
    changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        // 비밀번호와 확인 비밀번호가 일치하지 않을 경우 처리
        alert('비밀번호가 일치하지 않습니다')
        return
      }
      else {
        const formdata = {
        new_password1: this.user_newPassword,
        new_password2: this.user_confirmPassword,
      }
      console.log(formdata)
        // 서버에 사용자 정보 업데이트 요청 보내기 -> 해야함
      this.$axios.post('http://127.0.0.1:8000/accounts/password/change/', formdata, {
          // 헤더정보는 CORS에 필요하다고하여 작성
          headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            },
        })
        .then(res => {  
              console.log(res)
              window.alert('비밀번호 변경에 성공하셨습니다.')
              this.user_newPassword = ''
              this.user_confirmPassword = ''
             // 토큰 저장
            const token = res.data.key
            localStorage.setItem('access_token', token)
            // 홈으로 바로 넘어가도록
            this.$router.push('/');
            })
          // 비밀번호 변경 실패시
          .catch(err => {
            console.log(err)
            const error_msg = err.request.response
            console.log('에러메세지는', error_msg)
            const real_error = JSON.parse(error_msg)
            this.error_msg = real_error
            alert('오류 메세지를 확인하세요.')
          })

      }
  
    },
    // 회원탈퇴
    deleteuser() {
        const r = window.confirm('Are you sure you want to delete?')
        if (r == true) {
          axios.get('http://127.0.0.1:8000/deleteuser/avatar/')
            .then(() => {
              console.log('아바타 삭제')
            })
            .catch((err) => {
              console.log(err)
            })  
          axios.delete('http://127.0.0.1:8000/deleteuser/')
          .then((res) => {
            console.log(res, '탈퇴확인')
            // DB에서 지우기
            localStorage.removeItem('access_token',)
            localStorage.removeItem('userdata')
            localStorage.removeItem('isLoggedIn')
            // DB에서 아바타 지우기

            delete axios.defaults.headers.common['Authorization'];
            window.alert('회원 탈퇴가 완료되었습니다.')
            this.$router.push('/');
          })
          .catch(err => {
            // 에러 처리
            console.log(err);
          });
        } else {
          window.alert('취소하셨습니다.')
        }
        
    }
  },
  computed: {
    userdata(){
      console.log('자두과자', window.localStorage.getItem('userdata'))
      const tmp = window.localStorage.getItem('userdata')
      return JSON.parse(tmp);
    },
    // forsave를 불러오며 폼데이터도 동일하게 변경
    // forsave는 원본, formdata는 변경될 내용
    forsave() {
      /* eslint-disable */
      const need = this.formdata
      const data = JSON.parse(localStorage.getItem('userdata'))
      const saving = {'name' : need}
      for (let keyy in need){
        saving[keyy] = data[keyy]
      }
      for (let keyy in need){
        need[keyy] = data[keyy]
      }
      console.log(this.formdata)
      return saving
    }
  },
}

</script>

<style>
  /* 스타일 정의 */

.profile {
  margin-top: 0px;
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




.container {
  padding-top: 1em;
  margin-top: 1em;
  margin-bottom: 1em;
 border-top: none;
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


.back {
     font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 40px;
  font-weight: bold;
  }


   .back1 {
    font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;
  display: flex;
  justify-content: center;
  }

  .back2 {
    font-family: 'Dovemayo_wild', sans-serif; 
    font-size: 20px;

  }

  .BigBox{
    border: 1px solid rgba(0, 0, 0, 0.3);
    width: 40%;
    margin: auto;
    padding: 50px;
    margin-bottom: 40px;
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
