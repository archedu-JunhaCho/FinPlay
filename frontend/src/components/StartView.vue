
<template>
  <div>
    <!-- <nav class="my-nav">
      <div class="links">
        <router-link to="/login">로그인</router-link> | 
        <router-link to="/register">회원가입</router-link>
      </div>
    </nav> -->
    <!-- 아이디어 / 돌아다니는 아바타들  -->
    <div class="home-view color-change-2x" @click="goToHome()">
      <h1 class="sample-text" style="position: fixed; left: 40%; right: 40%;">FinPlay</h1>
      <img :src=realurl+avatarurl1 alt="??" class="homeimg">
      <img :src=realurl+avatarurl2 alt="??" class="homeimg">
      <img :src=realurl+avatarurl3 alt="??" class="homeimg">
      <img :src=realurl+avatarurl4 alt="??" class="homeimg">
      <img :src=realurl+avatarurl5 alt="??" class="homeimg">
      <img :src=realurl+avatarurl6 alt="??" class="homeimg">
      <img :src=realurl+avatarurl7 alt="??" class="homeimg">
      <img :src=realurl+avatarurl8 alt="??" class="homeimg">
      <img :src=realurl+avatarurl9 alt="??" class="homeimg"> 
      <img :src=realurl+avatarurl10 alt="??" class="homeimg">
    </div>
  </div>
</template>

<style scoped>
.home-view {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7); /* 검은색 배경을 투명하게 설정 */
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.sample-text {
   font-family: 'Dovemayo_wild', sans-serif;
  font-size: 150px;
  font-weight: bold;
  color: white;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.my-nav {
 display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  padding: 10px;

}

.my-nav p {
  font-family: Arial, sans-serif;
  font-weight: bold;
  color: #000000; /* 텍스트 색상을 흰색으로 설정 */
  margin-right: 10px;
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


.my-nav p:hover {
  color: #42b983;
}
.homeimg{
  opacity: 40%;
  z-index: 1;
}
.color-change-2x{-webkit-animation:color-change-2x 2s linear infinite alternate both;animation:color-change-2x 2s linear infinite alternate both}

@-webkit-keyframes color-change-2x{0%{background:#7064b5}100%{background:#7c6b85}}@keyframes color-change-2x{0%{background:#4d6c6e}100%{background:#714e86}}

</style>

<script>
export default {
  data(){
    return {
      realurl : process.env.VUE_APP_BACKEND_API_URL,
      avatarurl1 : "/media/avatar/1.jpg",
      avatarurl2 : "/media/avatar/2.jpg",
      avatarurl3 : "/media/avatar/3.jpg",
      avatarurl4 : "/media/avatar/4.jpg",
      avatarurl5 : "/media/avatar/5.jpg",
      avatarurl6 : "/media/avatar/6.jpg",
      avatarurl7 : "/media/avatar/7.jpg",
      avatarurl8 : "/media/avatar/8.jpg",
      avatarurl9 : "/media/avatar/9.jpg",
      avatarurl10 : "/media/avatar/10.jpg",
      
    }
  },
  methods: {
    goToHome() {
      this.$router.push('/home');
    },
  },
};
</script>
