<template>
  <div>
    <nav class="my-nav" >
      <div class="home">
        <router-link to="/home">Home</router-link>
      </div>
      <div class="bind">
        <router-link to="/finance/deposit">정기예금</router-link> |
        <router-link to="/finance/installment">정기적금</router-link>
      </div>
    </nav>

    <div class="big-box">
<div>

    <h1 class="back" style=" visibility:hidden">정기적금</h1>
        <div class="search-box">
      <h4  style="margin-top:60px; , sans-serif; font-size:30px;">검색하기</h4>
      <h6 style="margin-top:30px; margin-bottom:30px;, sans-serif; font-size:20px;">검색 조건을 입력하세요</h6>

      <hr>
      <h6 style="margin-top:30px; , sans-serif; font-size:20px; ">은행을 선택하세요</h6>
      <div>
        <select style=" margin-top:10px;font-family: SUITE-Regular; font-size: 16px;" id="bank" v-model="choose_bank"  @change="change">
          <option value="" style="color:gray; font-family: SUITE-Regular; font-size: 16px;">전체은행</option>
          <option v-for="bank in aboutChange" :value="bank" :key="bank">{{ bank }}</option>
          
        </select>
      </div><br>
      <h6 style=" sans-serif; font-size:20px; " >예치기간</h6>
      <div>
        <select style=" margin-top:10px; font-family: SUITE-Regular; font-size: 16px;" id="period" v-model="choose_period" @change="change" >
          <option value="" style="color:gray ;  sans-serif;">전체기간</option>
          <option value="6개월">6개월</option>
          <option value="12개월">12개월</option>
          <option value="24개월">24개월</option>
          <option value="36개월">36개월</option>
        </select>
      </div><br>
      
    </div>
</div>

    <div class="show-box" style="border-radius: 10px; ">
         <h1 class="back">정기적금</h1>
        <table>
        <thead>
          <tr>
            <th class="common-th1">공시 제출 월</th>
            <th class="common-th1">금융회사명</th>
            <th class="common-th2">상품명</th>
            <th class="period-column" v-for="period in periods" :key="period">{{ period }} (Click to sort ascending)</th>
          </tr>
        </thead>
        <tbody>
          <tr class="fixed-height"  style="height:74px;margin-top:0px;margin-bottom:0px;" @click="$router.push(`/finance/installment/detail/${deposit.fin_prdt_cd}`)" v-for="deposit in pagedDeposits" :key="deposit.fin_prdt_cd">
            <td>{{ deposit.dcls_month }}</td>
            <td>{{ deposit.kor_co_nm }}</td>
            <td>{{ deposit.fin_prdt_nm }}</td>
            <td v-for="period in periods" :key="period" :style="getCellColor(deposit, period)">{{ getInterestRate(deposit, period) }}</td>
            
          </tr>
        </tbody>
      </table>

      <div class="btn-cover">
        <button :disabled="currentPage === 1" @click="prevPage" class="page-btn">이전</button>
        <span class="page-count">{{ currentPage }} / {{ totalPages }} 페이지</span>
        <button :disabled="currentPage === totalPages" @click="nextPage" class="page-btn">다음</button>
      </div>
    </div>

</div>
    </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'RecommendView',
  data() {
    return {
      choose_bank: '',
      choose_period: '',
      currentPage: 1, // 현재 페이지 번호
      totalPages: 1, // 전체 페이지 수
      pageSize: 10, // 한 페이지에 보여줄 항목 수
      deposits: [], // 백엔드로부터 받아온 예금 정보
      aboutChange:[],
      periods: ['6개월', '12개월', '24개월', '36개월'], // 예치기간 옵션
      filteredDeposits : [],
    }
    },
    created() {
    this.fetchDeposits();
  },
  mounted() {
    this.fetchDeposits(),
    console.log('은행이름mounted됐나요~~')
    this.$axios
      .get('http://127.0.0.1:8000/api/v2/saving-products/', {
            headers: {
              "Content-Type": "multipart/form-data",
              // 'Access-Control-Allow-Origin': '*',
            },
          })
          .then(res => {
        this.deposits = res.data;
        const bankNames = new Set(); // 중복 제거 => set
        this.deposits.forEach(deposit => {
        bankNames.add(deposit.kor_co_nm); // 은행 이름을 Set에 추가
      });
        this.aboutChange = Array.from(bankNames); // Set을 배열로 변환하여 aboutChange에 할당
        
        console.log(this.aboutChange)
        this.totalPages = Math.ceil(this.deposits.length / this.pageSize);
      })
      .catch(err => {
        console.log(err);
      })
  },
  methods: {
    getCellColor(deposit, period) {
        const rate = this.getInterestRate(deposit, period);
        if (rate !== '-' && period === this.choose_period) {
          return { backgroundColor: '#2c3e50', opacity: '0.5', color: '#ffffff' };
        }
        return {};
      },
    fetchDeposits() {
      axios
        .get('http://127.0.0.1:8000/api/v2/saving-products/')
        .then(response => {
          this.deposits = response.data;
          this.filteredDeposits = [...this.deposits]
          this.totalPages = Math.ceil(this.deposits.length / this.pageSize);
        })
        .catch(err => {
          console.log(err);
        });
    },
    applyFilters() {
      this.currentPage = 1;
      this.fetchDeposits();
    },
    // 최대 이자율 보여줄꺼임(우대이자율때문에 개월수에 해당하는 여러 개의 이자율이 존재하는 것으로 추정됨)
    getInterestRate(deposit, period) {
      // Make sure depositoptions_set is defined
      if (!deposit.savingoptions_set) {
        return '-';
      }

      const options = deposit.savingoptions_set;
      // remove '개월' from the period and parse it into an integer
      const periodInMonths = parseInt(period.replace('개월', ''));
      const matchedOptions = options.filter(option => option.save_trm === periodInMonths);
      
      if (matchedOptions.length > 0) {
        // get the maximum interest rate among the matched options
        const maxRate = Math.max(...matchedOptions.map(option => option.intr_rate));
        return `${maxRate}%`;
      } else {
        return '-';
      }
    },
    prevPage() {
      this.currentPage--;
    },
    nextPage() {
      this.currentPage++;
    },
    change(e){
    console.log(e.target.value)
    let filtered = this.deposits;
    console.log(filtered )
    if (this.choose_bank && this.choose_bank !== '전체은행') {
      filtered = filtered.filter(deposit => deposit.kor_co_nm === this.choose_bank);
    }
    this.filteredDeposits = filtered
      console.log(filtered )

    // 페이지 개수를 재계산하고 페이지 번호를 첫 번째 페이지로 리셋
      this.totalPages = Math.ceil(this.filteredDeposits.length / this.pageSize);
      this.currentPage = 1;  

      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;

    return filtered.slice(start, end);

 
    },

  },
  computed: {
    pagedDeposits() {
    const start = (this.currentPage - 1) * this.pageSize;
    const end = start + this.pageSize;
    return this.filteredDeposits.slice(start, end);
  },
  }


};
</script>

<style scoped>
/* 스타일 정의 */
.page-count {
  margin-left: 5px;
  margin-right: 5px;
  margin-top: 30px;
  position: relative;
  top: -10px;
}

.fixed-height {
  height: 74px !important;
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

.selected {
  background-color: rgba(0, 0, 0, 0.5); /* 불투명한 검은색 */
  color: white; /* 글자 색은 흰색 */
   font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;
}


 .back {
     font-family: 'GangwonEdu_OTFBoldA'; 
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 30px;
  }
.big-box {
   
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 20px;
  min-height: 60vh;  
  max-height: 100vh; 
}

.search-box {
  font-family: 'GangwonEdu_OTFBoldA'; 
  width: 250px; /* 고정 너비 */
  height: 823.75px; 
  border:1px solid black; 
  margin-right: 50px;
  border-radius: 10px;  /* 원하는 각도로 조절 가능합니다 */
  box-sizing: border-box;
}

.show-box {
  width: 1200px; /* 최소 너비 */
  
  font-family: 'GangwonEdu_OTFBoldA'; 
  font-size: 20px;
  border-radius: 10px;  /* 원하는 각도로 조절 가능합니다 */
  
  justify-content: flex-start;
}

.period-column {
  font-family: 'GangwonEdu_OTFBoldA';
  font-weight: bolder;
  width: 150px;  /* 너비를 원하는 값으로 변경할 수 있습니다 */
  padding: 5px 10px;  /* 상하 좌우 padding을 원하는 값으로 변경할 수 있습니다 */
  font-size: 20px;
}
.common-th1 {
  padding: 5px 10px;  /* 상하 좌우 padding을 원하는 값으로 변경할 수 있습니다 */
  width: 120px;
  font-size: 20px;

  }

.common-th2 {
  padding: 5px 10px;  /* 상하 좌우 padding을 원하는 값으로 변경할 수 있습니다 */
  width: 160px;
  font-size: 20px;
  }

table {
  width: 1200px;
  border-collapse: collapse;
  border: 2px solid #404040;
  height: 823.75px; 
  border-radius: 10px;  /* 원하는 각도로 조절 가능합니다 */

}

th, td {
  padding: 10px;
}
table tr:first-of-type {
  border-top: 2px solid #404040;
}

.btn-cover .page-btn {
  width: 5rem;
  height: 2rem;
  letter-spacing: 0.5px;
  font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;
  color: #2c3e50;

  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  margin-top: 30px;
  position: relative;
  top: -10px;
}

@font-face {
    font-family: 'GangwonEdu_OTFBoldA';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2201-2@1.0/GangwonEdu_OTFBoldA.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.btn-cover .page-btn:hover {
  background-color: #2c3e50;
  color: white;
}

.btn-cover .page-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
  border-color: #ccc;
}

.btn-cover .page-btn:disabled:hover {
  background-color: transparent;
}

</style>
