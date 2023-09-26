<template>
    <div >
    <div v-if="!isAvatar" style="position: fixed; left: 43%; bottom: 40%; width: 250px; height: 250px; border: 1px solid black;" class="shake-bottom randomBox" @click="clickRandombox"><div style="margin-top: 16%; font-family: NeoDunggeunmoPro-Regular; font-size: 120px;">?</div></div>
    <nav class="my-nav">
      <div class="links" v-if="!isLoggedIn" >
        <router-link style="margin-right:25px;margin-left:25px" to="/login">로그인</router-link> | 
        <router-link  style="margin-right:25px;margin-left:25px" to="/register">회원가입</router-link>
      </div>
      <div v-else  id="lst" class="link-list"  >
          <router-link style="margin-right: 50px;" to="/profile">Profile</router-link> |
          <router-link style="margin-right: 50px;" to="/finance/map">Map</router-link> |
          <router-link style="margin-right: 50px;" to="/finance/rate">Rate</router-link> |
          <router-link style="margin-right: 50px;" to="/profileupdate/avatar">Avatar</router-link> |
          <router-link style="margin-right: 50px;" to="/finance/deposit">Products</router-link> |
          <router-link style="margin-right: 50px;" to="/community/board">Board</router-link> |
          <span class="logout-link" @click="logout()">로그아웃</span>
        </div>
    </nav><br>

    <!-- <h1 class="title">HomeView</h1> -->

      <div class="chat_wrap" v-if="avatarClick">
      <div class="header">아바타에게 질문해보세요</div>
      <div class="chat" id="chatbox" style="height: 82%; border: none;">
          <ul>
              <!-- 동적 생성 -->
          </ul>
      </div>
      <div class="input-div">
          <textarea placeholder="질문을 입력하고 엔터를 눌러주세요." v-model="chattxt" @keyup.enter="sendMsg" maxlength="50" ></textarea>
      </div>


      <!-- format -->
      <div class="chat format">
          <ul>
              <li>
                  <div class="sender">
                      <span></span>
                  </div>
                  <div class="message">
                      <span></span>
                  </div>
              </li>
          </ul>
      </div>
    </div>

    <div id="avatar_box" v-if="isAvatar" class="box animated wobble pulse" @click="clickAvatar">
      <div></div>
      <p class="speech-bubble box animated bounceIn bounceOut">안녕하세요 <br>질문이 있으면 <br>저를 눌러주세요</p>
      <img class="avatar_img" :src=realurl+avatarUrl+random alt="" >
    </div>
    <button @click="goRec" v-if="avatarClick" id="rec_product" class="box animated pulse">
      추천 상품 받으러가기
    </button>
  
  </div>
</template>

<script>
import axios from 'axios'
// import openai from 'openai'

// import send from 'send'
export default {
  name: 'HomeView',
  data() {
    return {
      isLoggedIn: false,
      isAvatar : false,
      avatarUrl : null,
      realurl : process.env.VUE_APP_BACKEND_API_URL,
      random : `?v=${Math.random()}`,
      chattxt : null, 
      avatarClick : false,
      chatMessages: [],
    }
  },
  mounted() {
    /* eslint-disable */
    if (localStorage.getItem('access_token')) {
        this.isLoggedIn = true
        console.log(JSON.parse(localStorage.getItem('userdata')).avatar)
        if (JSON.parse(localStorage.getItem('userdata')).avatar == []) {
          console.log('아바타값 없음')
          this.avatarUrl = null
          this.isAvatar = false
        } else {
          console.log('아바타값 있음')
          this.avatarUrl = JSON.parse(localStorage.getItem('userdata')).avatar[0].img_file.slice(6)
          this.isAvatar = true
        }
      } else {
        this.isLoggedIn = false
      };


    
    // this.avatarUrl = localStorage.getItem('')
  },
  methods: {
    clickRandombox(){
      console.log('랜덤 박스 클릭')
      if (this.isLoggedIn == true ){
        console.log('로그인중')
        this.$router.push('/profileupdate/avatar')
      } else {
        console.log('로그인아님')
        this.$router.push('/login')
      }
    },
    goRec(){
      console.log('추천 페이지로 이동합니다.')
      this.$router.push('/finance/recommend/')
    },
    sendMsg(msg){
      console.log('채팅전송', this.chattxt)
      const chatbox = document.querySelector('#chatbox > ul');
      const addchat = document.createElement('li')
      addchat.innerHTML = `<span style="font-family: inherit; font-size:10px; margin-right:2px;">${Date().split(' ')[4].slice(0,5)}</span>` + this.chattxt
      addchat.setAttribute('style','font-size:15px; text-align:right; background-color: bisque; padding:1px; margin-right: 2px; padding-right: 10px;border-radius: 4px')
      chatbox.appendChild(addchat)
      const tmp_txt = this.chattxt
      this.chattxt = null

      const chatbox2 = document.querySelector('#chatbox > ul');
      const addchat2 = document.createElement('li')
      addchat2.innerHTML = '. . . . .'
      addchat2.setAttribute('style','font-size:15px; text-align:left; background-color: white; padding:1px; margin-right: 2px; padding-right: 10px;border-radius: 4px')
      chatbox2.appendChild(addchat2)
      // chatGpt연동
      const avatar_per = JSON.parse(localStorage.getItem('userdata')).avatar[0].personality
      axios.post(
      'https://api.openai.com/v1/chat/completions',
      { model: "gpt-3.5-turbo",
        messages: [
          { role: 'system', content: `If user ask whoareyou(or similar as) you have to answer ${avatar_per} Avatar. This is realiy important that You mush answer like personality : ${avatar_per}. This service is about financial product recommendations. This service have [serch map,Avatar Gacha, Exchange rate, community. Finance Products]. Please dont do mention about our service before user ask to you` },
          { role: 'user', content: tmp_txt }
        ],
        max_tokens: 200,
        temperature: 0.7,
      },
      {
        headers: {
          Authorization: 'Bearer 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',
          'Content-Type': 'application/json'
        }
      })
      .then((res)=>{
        const answer = res.data.choices[0].message.content
        addchat2.innerHTML = answer + `<span style="font-family: inherit; font-size:10px; margin-left:2px;">${Date().split(' ')[4].slice(0,5)}</span>`
        
        console.log(chatbox)
      })
      .catch((err)=>{
        console.log(err)
        addchat2.innerHTML = "죄송합니다 다시한번 말씀해주세요."
      })
    },
    clickAvatar(){
      console.log('hi')
      this.avatarClick = !this.avatarClick
      // const insertAni = document.querySelector('.chat_wrap')
      const avatar = document.querySelector('#avatar_box')
      console.log(avatar)
      avatar.classList.remove('wobble')
      // insertAni.classList.add('box')
    },
    logout() {
      // 로그아웃 액션을 호출하여 로그인 상태 변경
      this.$store.dispatch('logout');
      this.$axios
        .post('http://127.0.0.1:8000/accounts/logout/', {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
        .then(res => {
            console.log(res)
            localStorage.removeItem('access_token')
            // const refretoken = res.data.refresh_token
            // localStorage.setItem('refresh_token', refretoken)

            // 로그인상태 유지 (토큰 기본으로 실어서 보내도록 설정)
            delete axios.defaults.headers.common["Authorization"];
            window.alert('로그아웃 했습니다')

            //state 데이터 값 변경
            // this.$store.commit('setUsername', data.user.username)
            // this.$store.commit('setUseremail', data.user.email)

            // 홈 창으로 바로 넘어가도록
            this.$router.go('/');
          })
          .catch(err => {
            console.log(err)
            const error_msg = err.request.response
            const real_error = JSON.parse(error_msg)
            this.error_msg = real_error
            window.alert('오류 메세지를 확인하세요.')
          })
        },
  },
}

</script>

<style scoped>
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

.title {
  font-family: 'Dovemayo_wild', sans-serif;
  font-size: 40px;
  font-weight: bold;
  color: #333;
  margin-top: 20px;
}

.links {
  display: flex;
  justify-content: space-between;
  align-items: right;
  margin:auto;
}

.link-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin:auto;
}


.link-list .links {
  display: flex;
}



.link-list .links router-link {
  margin-right: 10px;
  text-decoration: none;
}

.links {
  justify-content: center;
  align-items: center;
}
.logout-link {
  cursor: pointer;
  color: red;
  font-family: 'Dovemayo_wild', sans-serif;
  font-size: 20px;

}

.lst {
  text-align: center;
}

span {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-weight: bold;
  color: #2c3e50;
}



#avatar_box {
  width: 250px;
  height: 250px;
  border: 1px solid #2c3e50;
  background-color: #2c3e50;
  border-radius: 40px;
  /* position: fixed; */
  margin: auto;
  margin-top: 15%;
}
.avatar_img{
  width: 250px;
  height: 250px;
  /* border: 1px solid #2c3e50; */
  position: relative;
  bottom: 45%;

}
.animated {
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

.animated.hinge {
  -webkit-animation-duration: 2s;
  animation-duration: 2s;
}

@-webkit-keyframes wobble {
  0% {
    -webkit-transform: translateX(0%);
    transform: translateX(0%);
  }

  15% {
    -webkit-transform: translateX(-25%) rotate(-5deg);
    transform: translateX(-25%) rotate(-5deg);
  }

  30% {
    -webkit-transform: translateX(20%) rotate(3deg);
    transform: translateX(20%) rotate(3deg);
  }

  45% {
    -webkit-transform: translateX(-15%) rotate(-3deg);
    transform: translateX(-15%) rotate(-3deg);
  }

  60% {
    -webkit-transform: translateX(10%) rotate(2deg);
    transform: translateX(10%) rotate(2deg);
  }

  75% {
    -webkit-transform: translateX(-5%) rotate(-1deg);
    transform: translateX(-5%) rotate(-1deg);
  }

  100% {
    -webkit-transform: translateX(0%);
    transform: translateX(0%);
  }
}

@keyframes wobble {
  0% {
    -webkit-transform: translateX(0%);
    -ms-transform: translateX(0%);
    transform: translateX(0%);
  }

  15% {
    -webkit-transform: translateX(-25%) rotate(-5deg);
    -ms-transform: translateX(-25%) rotate(-5deg);
    transform: translateX(-25%) rotate(-5deg);
  }

  30% {
    -webkit-transform: translateX(20%) rotate(3deg);
    -ms-transform: translateX(20%) rotate(3deg);
    transform: translateX(20%) rotate(3deg);
  }

  45% {
    -webkit-transform: translateX(-15%) rotate(-3deg);
    -ms-transform: translateX(-15%) rotate(-3deg);
    transform: translateX(-15%) rotate(-3deg);
  }

  60% {
    -webkit-transform: translateX(10%) rotate(2deg);
    -ms-transform: translateX(10%) rotate(2deg);
    transform: translateX(10%) rotate(2deg);
  }

  75% {
    -webkit-transform: translateX(-5%) rotate(-1deg);
    -ms-transform: translateX(-5%) rotate(-1deg);
    transform: translateX(-5%) rotate(-1deg);
  }

  100% {
    -webkit-transform: translateX(0%);
    -ms-transform: translateX(0%);
    transform: translateX(0%);
  }
}

.wobble {
  animation: wobble 0.8s ease-in ;
  -webkit-animation-name: wobble;
  animation-name: wobble;
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    -webkit-transform: scale(0.3);
    -ms-transform: scale(0.3);
    transform: scale(0.3);
  }

  50% {
    opacity: 1;
    -webkit-transform: scale(1.05);
    -ms-transform: scale(1.05);
    transform: scale(1.05);
  }

  70% {
    -webkit-transform: scale(0.9);
    -ms-transform: scale(0.9);
    transform: scale(0.9);
  }

  100% {
    -webkit-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
  }
}

.bounceIn {
  -webkit-animation-name: bounceIn;
  animation-name: bounceIn;
  animation-delay: 2s;
}

@keyframes bounceOut {
  0% {
    -webkit-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
  }
  25% {
    -webkit-transform: scale(0.95);
    -ms-transform: scale(0.95);
    transform: scale(0.95);
  }
  50% {
    opacity: 1;
    -webkit-transform: scale(1.1);
    -ms-transform: scale(1.1);
    transform: scale(1.1);
  }
  100% {
    opacity: 0;
    -webkit-transform: scale(0.3);
    -ms-transform: scale(0.3);
    transform: scale(0.3);
  }
}

.bounceOut {
  -webkit-animation-name: bounceOut;
  animation-name: bounceOut;
  animation-delay: 5s;
}

@font-face {
    font-family: 'Dovemayo_wild';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2302@1.0/Dovemayo_wild.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}

.speech-bubble {
  width: 200px;
  min-height: 100px;
	position: relative;
	background: #d7e7d3;
	border-radius: .4em;
  left: 5px;
  bottom: 120px;
  padding: 10px;
  overflow-wrap: break-word;
  align-items: center;
  display: flex;
  justify-content: center;
  font-family: "Dovemayo_wild";
  color: black;
  font-size: 13px;
}


.speech-bubble:after {
	content: '';
	position: absolute;
	bottom: 0;
	left: 50%;
	width: 0;
	height: 0;
	border: 27px solid transparent;
	border-top-color: #d7e7d3;
	border-bottom: 0;
	border-left: 0;
	margin-left: -13.5px;
	margin-bottom: -27px;
}

*{ margin: 0; padding: 0; }
.chat{
  height: 250px;
  padding : 10px;
  word-wrap: break-word;
  overflow: auto;

}
.chat::-webkit-scrollbar {
  width: 10px; /* 스크롤 막대 너비 */
}
.chat::-webkit-scrollbar-thumb {
  background-color: gray; /* 스크롤 막대 색상 */
}


.chat_wrap .header { font-size: 14px; padding: 15px 0; background: #2c3e50;; color: white; text-align: center; border-start-end-radius: 15px; border-top-left-radius: 15px;}
 
.chat_wrap .chat { padding-bottom: 80%; }
.chat_wrap .chat ul { width: 100%; list-style: none; }
.chat_wrap .chat ul li { width: 100%; }
.chat_wrap .chat ul li.left { text-align: left; }
.chat_wrap .chat ul li.right { text-align: right; }
 
.chat_wrap .chat ul li > div { font-size: 13px;  }
.chat_wrap .chat ul li > div.sender { margin: 10px 20px 0 20px; font-weight: bold; }
.chat_wrap .chat ul li > div.message { display: inline-block; word-break:break-all; margin: 5px 20px; max-width: 75%; border: 1px solid #888; padding: 10px; border-radius: 5px; background-color: #FCFCFC; color: #555; text-align: left; }
 
.chat_wrap .input-div { width: 300px; background-color: #FFF; text-align: center;  border-top: 1px solid#464545; left:0; font-family: Dovemayo_wild;}
.chat_wrap .input-div > textarea { width: 100%; height: 80px; border: 1px solid black; padding: 10px; position: absolute; left: -1px; bottom: 1px;
border-radius: 10px;}
 
.format { display: none; }
#rec_product{
  position: relative;
  left: 400px;
  bottom: 150px;
  padding: 10px;
  background-color: #2c3e50;
  border-radius: 10px;
  font-family: Dovemayo_wild;
  color: white;
  border: none;
}

@-webkit-keyframes pulse {
  0% {
    -webkit-transform: scale(1);
    transform: scale(1);
  }

  50% {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
  }

  100% {
    -webkit-transform: scale(1);
    transform: scale(1);
  }
}

@keyframes pulse {
  0% {
    -webkit-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
  }

  50% {
    -webkit-transform: scale(1.1);
    -ms-transform: scale(1.1);
    transform: scale(1.1);
  }

  100% {
    -webkit-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
  }
}

.pulse:hover {
  -webkit-animation-name: pulse;
  animation-name: pulse;
  animation-iteration-count: infinite;
}

.shake-bottom {
  animation: roll-in-bottom 2s linear forwards, shake-bottom 1.5s ease-in-out 2s infinite;
}

@keyframes shake-bottom {
  0%, 100% {
    transform: rotate(0deg);
    transform-origin: 50% 100%;
  }
  10% {
    transform: rotate(2deg);
  }
  20%, 40%, 60% {
    transform: rotate(-4deg);
  }
  30%, 50%, 70% {
    transform: rotate(4deg);
  }
  80% {
    transform: rotate(-2deg);
  }
  90% {
    transform: rotate(2deg);
  }
}

@keyframes roll-in-bottom {
  0% {
    transform: translateY(800px) rotate(540deg);
    opacity: 0;
  }
  100% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }

}

.randomBox{
  border-radius: 20px;
  background-color: #2c3e50;
  color: white;
}

@font-face {
    font-family: 'NeoDunggeunmoPro-Regular';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2302@1.0/NeoDunggeunmoPro-Regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}

.chat_wrap { position: absolute; left: 150px; bottom: 200px; width: 400px; height: 700px; border: 1px solid #464545; border-radius: 15px; font-family: Dovemayo_wild;}
</style>
