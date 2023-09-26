<template>
  <div class="profile">
    <nav class="my-nav">
      <router-link to="/home">Home</router-link>
    </nav>
    <h1 style=" font-family: 'Dovemayo_wild';  font-weight: bold; margin-top: 3%;" >My Information</h1><br>

    <div>
      <div>
        <!-- {{ userdata }}  -->
        <img :src=realurl+avatarurl+random v-if="avatar">
      </div><br>
      <div class="back">
        <p v-for="(items, key, index) in userdata" :key="index" style="margin: 0; max-height: 46px;">
          <span style="font-size: 17px; " v-if="['username','email','name','age','gender','date_joined ', 'product_lst', 'product_lst_saving','follow'].includes(key)">{{ key }} : <input type="text" :value=items disabled class="ipBox"></span>
        </p>
        <p style="margin: 0;"><span class="ipBox" style="font-size: 17px; ">마지막 로그인 : {{ userdata.last_login.slice(0,10) }}</span></p>
      </div>
      <div class="container">
          <div class="button-wrapper" >
            <button @click="$router.push('/profileupdate')" title="Button push black/gray"  class="button btnBlackGray btnPush">UPDATE</button>
            <div class="clear"></div>
          </div>
        </div>

    </div><br>





  </div>
</template>

<script>
// import axios from 'axios';

export default {
  data() {
    return {
      id: '',
      email: '',
      userdata : '',
      avatar : true,
      avatarurl : JSON.parse(localStorage.getItem('userdata')).avatar[0].img_file.slice(6),
      realurl : process.env.VUE_APP_BACKEND_API_URL,
      random : `?v=${Math.random()}`,
      namechange : {
        'product_lst_saving' : '가입 적금',
        'product_lst ' : '가입 예금',
        'username ' : '아이디',
        'email  ' : '이메일',
        'name  ' : '아이디',
        'age  ' : '나이',
        'gender ' : '성별',
        'follow ' : '팔로워',
      }
    };
  },
  created() {
    console.log('자두과자', window.localStorage.getItem('userdata'))
    const tmp = window.localStorage.getItem('userdata')
    this.userdata = JSON.parse(tmp);
  },
};
</script>

<style>
/* 스타일 정의 */
/* .profile {
  margin-top: 0px;
} */


nav {
  padding: 10px;
  text-align: right;
  
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;

}

nav a.router-link-exact-active {
  color: #42b983;
}

 .back {
     font-family: 'Dovemayo_wild', sans-serif; 
  }


.container {
  padding-top: 1em;
  margin-top: 1em;
  margin-bottom: 1em;
  border-top: solid 1px #CCC;
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
.ipBox{
  background-color: #ffffff;
  border: none;
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
