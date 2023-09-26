<template>
  <div>
    <!-- 화면에 표시할 내용 추가 -->
    <nav>
        <router-link to="/home">Home</router-link>
    </nav><br>
    <h1>Withdrawal Membership</h1>
    <p>정말 탈퇴를 원하십니까? 원해요?????</p>
    <div id="delete_before">
      <div class="text-center">
        <label for="" class="text-black mb-3">비밀번호를 입력 해 주세요!</label>
        <div class="input">
          <input type="password" style="text-align:center" ref="pwd" class="form-control me-2" v-model="password" placeholder="비밀번호를 입력하세요">
        </div><br>
        
      </div>
    </div>
    <div v-if="passwordMatch">
      <button @click="withdrawal" :disabled="isWithdrawalProcessing">Withdraw</button>
    </div>
    <div v-else>
      <button @click="withdrawalfailed" :disabled="isWithdrawalProcessing">Withdraw</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      password: '',
      isWithdrawalProcessing: false, // 탈퇴 처리 중 여부를 나타내는 상태 변수
    };
  },
  methods: {
    withdrawal() {
      if (this.isWithdrawalProcessing) {
        return; // 탈퇴 처리 중인 경우 중복 클릭 방지
      }
      const userPassword = ''; // 사용자의 비밀번호 변수에 할당
      if (this.password === userPassword) {
        this.isWithdrawalProcessing = true; // 탈퇴 처리 중 상태로 설정
        axios
          .delete('http://127.0.0.1:8000/accounts/delete/', {
            headers: {
              Authorization: `Token ${localStorage.getItem('access_token')}`,
            },
          })
          .then(response => {
            alert(response.data.detail);
            // 탈퇴 성공 처리 후 필요한 작업 수행
          })
          .catch(error => {
            console.error(error);
            alert('탈퇴 처리 중 오류가 발생했습니다.');
            // 탈퇴 실패 처리 후 필요한 작업 수행
          })
          .finally(() => {
            this.isWithdrawalProcessing = false; // 탈퇴 처리 완료 상태로 설정
          });
      } else {
        this.withdrawalfailed();
      }
    },
    withdrawalfailed() {
      alert('비밀번호가 일치하지 않습니다.');
      // 비밀번호 불일치 처리 후 필요한 작업 수행
    },
  },
};
</script>

