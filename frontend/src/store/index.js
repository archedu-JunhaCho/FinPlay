import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
// import JSON from 'JSON'
// import router from '@/router'



Vue.use(Vuex)



export default new Vuex.Store({
  state: {
    // 로그인 상태 저장
    isLoggedIn:false,
    UserData: {},

  },
  getters: {
  },
  mutations: {
    login(state) {
      state.isLoggedIn = true;
      localStorage.setItem('isLoggedIn', true)
    },
    logout(state) {
      state.isLoggedIn = false;
      state.UserData = {};
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('userdata');
    
      // 클라이언트에서 서버에 로그아웃 요청을 보냄
      axios.post('http://127.0.0.1:8000/updateuser/')
        .then(() => {
          // 서버로부터 응답을 받은 후 로컬 스토리지 및 Axios 헤더에서 토큰 삭제
          localStorage.removeItem('access_token');
          delete axios.defaults.headers.common['Authorization'];
        })
        .catch(error => {
          // 에러 처리
          console.log(error);
        });
      },
     
      SET_USER(state, userdata) {
        state.UserData = userdata.userdata;
        console.log('state는', state);
        console.log('state의 내부는', state.UserData);
        localStorage.setItem('userdata', JSON.stringify(state.UserData));
      },
      // 회원탈퇴
      clearUserData(state) {
        state.UserData = {};
      },
  
  },
  actions: {
    login({commit }) {
      commit('login');
    },
    logout({ commit }) {
      
        commit('logout');
    },
    SET_USER ({commit}, userdata) {
      commit('SET_USER', userdata)
    },
    withdrawal({ commit }) {
      commit('clearUserData')
    }
  },
  modules: {
    // auth
  }
})


