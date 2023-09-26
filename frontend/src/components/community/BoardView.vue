<template>
  <div class="board-list">
    <nav class="my-nav">
      <router-link to="/home">Home</router-link>
    </nav>


    <p style="display:none">{{paginatedData}}</p>
    <p style="display:none">{{detailData[1]}}</p>


    <h1 class="back">BoardView</h1>

    <div class="big-container">

      <div class="container">
        <div class="button-wrapper" >
          <button @click="goToCreateBoard()" title="Button push black/gray"  class="button btnBlackGray btnPush">글쓰기</button>
          <div class="clear"></div>
        </div>
      </div>



    <br>

    <div class="table-container">
      <table class="board-table">
        <thead>
          <tr>
            <th>No</th>
            <th>작성자</th>
            <th>제목</th>
            <th>등록일시</th>
            <th>좋아요</th>
            <th>댓글수</th>
          </tr>
        </thead>
        <tbody>
          

            <tr  v-for="(row, idx) in paginatedData" :key="idx">
  
              <td @click="viewPost(row.id)">{{ idx+1 }}</td>
              <td @click="viewPost(row.id)">{{ row.username }}</td>
              <td @click="viewPost(row.id)">{{ row.title }}</td>
              <td @click="viewPost(row.id)">{{ formatDate(row.created_at) }}</td>
              <td @click="viewPost(row.id)">{{ row.like_count }}</td>
              <td @click="viewPost(row.id)">{{ row.comment_count }}</td>
              <td>
                <button class="edit-button" @click="editPost(row.id)">수정</button>
                <button class="delete-button" style="margin-left:10px" @click="deletePost(row.id, row.username)">삭제</button>

              
              </td>
            </tr>
    
    <tr v-if="paginatedData.length === 0">
      <td colspan="5">No posts found</td>
    </tr>
  </tbody>
      </table>
    </div>
      <div class="btn-cover">
        <button :disabled="pageNum === 0" @click="prevPage" class="page-btn">
          이전
        </button>
        <span class="page-count">{{ pageNum + 1 }} / {{ pageCount + 1 }}  </span>
        <button :disabled="pageNum >= pageCount - 1" @click="nextPage" class="page-btn">
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BoardView',
  data() {
    return {
      paginatedData: [], // 글 목록 데이터
      pageNum: 0,

      detailData : [], // formdata 초기화
      
      listArray: [],


      // 전체 데이터 배열
      allData: [],

      // 페이지당 표시할 항목 개수
      itemsPerPage: 8,

 

      isSearching: false,
      filteredList: [],
    };
  },
  
  computed: {
    // pageCount() {
    //     const listLength = this.listArray.length;
    //     const pageSize = this.pageSize;
    //     let pageCount = 1+ Math.ceil(listLength / pageSize);

    //     return pageCount;
    //   },

    displayedData() {
      const startIndex = this.pageNum * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.allData.slice(startIndex, endIndex);
    },
    // 전체 페이지 개수
    pageCount() {
      return Math.ceil(this.allData.length / this.itemsPerPage);
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const day = date.getDate();
      return `${year}년 ${month}월 ${day}일`;
    },
     viewPost(id){
      this.$router.push(`/community/board/${id}`);
     },
     editPost(id){
      this.$router.push(`/community/board/change/${id}`);
     },
    searchByUsername() {
      axios.get('http://127.0.0.1:8000/api/v1/articles/')
        .then(response => {
          const data = response.data;
          this.filteredList = data.filter(article => article.username === this.searchKeyword);
          if (this.filteredList.length === 0) {
            // 검색 결과가 없을 경우
            alert('검색 결과가 없습니다.');
          } else {
            // 검색 결과가 있을 경우
            this.isSearching = true;
          }
        })
        .catch(error => {
          console.error('검색 요청에 실패했습니다:', error);
          alert('검색 요청에 실패했습니다.');
        });
    },
    goToCreateBoard() {
    this.$router.push({ name: 'createBoardView' });
    },
    handleDeleteClick(event, postId, username) {
    event.stopPropagation();
    // 삭제 로직을 여기에 구현합니다.
    console.log("Deleting post with id:", postId);
    console.log("Username:", username);
  },
    deletePost(postId, postOwner) {
      let userdata = JSON.parse(localStorage.getItem('userdata'));
      let currentUserId = userdata.username;
     
      // 사용자가 글 작성자인지 확인
      
      if (currentUserId == postOwner) {
        if (window.confirm('정말 삭제하기를 원하세요?')) {
          // API 호출 등으로 실제 삭제 구현
          console.log('Deleting post with id:', postId);
          console.log(currentUserId,'currentUserId')
          console.log(userdata,'userdata')
          let id = this.paginatedData[0].id;
          console.log(id,"ddddddddddddd")
          const token = localStorage.getItem('access_token')
          axios.defaults.headers.common.Authorization = `Token ${token}`
            this.$axios.delete('http://127.0.0.1:8000/api/v1/articles/'+id +'/', {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              })
              .then(response => {
                console.log(response);
                alert('삭제 성공');
                this.$router.go('/community/board');
              })
              .catch(error => {
                console.error(error);
                const error_msg = error.request.response;
                console.log('에러메세지는', error_msg);
                const real_error = JSON.parse(error_msg);
                this.error_msg = real_error;
                alert('오류 메세지를 확인하세요.' , error);
                console.log(currentUserId,'currentUserId')
                console.log(postOwner,'postOwner')
                console.log(userdata,'userdata')
              });
        }
      } else {
        alert('내 글만 삭제가 가능합니다');
        
        console.log(currentUserId,'currentUserId')
        console.log(userdata,'userdata')

        console.log('currentUserId:', currentUserId);
        console.log('postOwner:', postOwner);
      }
    },
    getPaginatedData() {
      // 글 목록 데이터를 가져오는 로직
       const token = localStorage.getItem('access_token')
      axios.defaults.headers.common.Authorization = `Token ${token}`
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/articles/',
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then((response) => {
          console.log("<<<<<<<<<<<<")
          console.log('어떤 데이터가 들어오고 있는지 확인해야겟씀',response.data)
          
          this.paginatedData = response.data;
        })
        .catch((error) => {
          console.log('>>>>>>>>>>>>>>')
          console.log(error);
        });
    },
    nextPage() {
      if (this.pageNum < this.pageCount - 1) {
        this.pageNum++;
      }
    },
    prevPage() {
      if (this.pageNum > 0) {
        this.pageNum--;
      }
    },
    fnView(idx) {
      // 선택한 글 보기 로직 구현
      console.log('Viewing article at index:', idx);
    },
  },
  mounted() {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common.Authorization = `Token ${token}`;

      axios.get('http://127.0.0.1:8000/api/v1/articles/')
        .then(response => {
          this.paginatedData = response.data;
          console.log(this.paginatedData);

          for (let i = 0; i < this.paginatedData.length; i++) {
            let id = this.paginatedData[i].id;

            axios.get(`http://127.0.0.1:8000/api/v1/articles/${id}/`)
              .then(response => {
                const detailData = response.data;
                console.log('detailData',detailData);
                this.detailData.push(detailData); // 상세 데이터를 배열에 추가
                // 가져온 상세 데이터 처리하기
               
               // paginatedData에 created_at 값을 추가합니다
              this.paginatedData[i].created_at = detailData.created_at;
              this.paginatedData[i].like_count = detailData.like_count;
              this.paginatedData[i].comment_count = detailData.comment_count;
              })
              .catch(error => {
                console.error(error);
              });

          }
        })
        .catch(error => {
          console.error(error);
        });
    },



}

</script>

<style scoped>


.big-container {
  width: 1400px;
  margin: auto;
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
.container {
  padding-top: 1em;
  margin-top: 1em;
  margin-bottom: 1em;
  border-top : none;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;


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


   .back1 {
     font-family: 'Dovemayo_wild', sans-serif;
    font-size: 20px;
  }

.search-input {
  margin-right: 10px;
}

.search-button {
  margin-right: 10px;
}

.board-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0px;
  font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;

}
.back {
   font-family: 'Dovemayo_wild', sans-serif; 
    font-size: 40px;
    margin:auto;
    margin-top:60px;

}

table {
  width: 100%;
  border-collapse: collapse;
}
table th {
  font-size: 1.2rem;
}
table tr {
  height: 2rem;
  text-align: center;
  border-bottom: 1px solid #505050;
}
table tr:first-of-type {
  border-top: 2px solid #404040;
}
table tr td {
  padding: 1rem 0;
  font-size: 1.1rem;
}
.btn-cover {
  margin-top: 1.5rem;
  text-align: center;
}
.btn-cover .page-btn {
  width: 5rem;
  height: 2rem;
  letter-spacing: 0.5px;
}
.btn-cover .page-count {
  padding: 0 1rem;
}
</style>


