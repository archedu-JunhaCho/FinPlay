<template>
<div class="big">

    <nav class="my-nav">
      <router-link to="/home">Home</router-link>
      <router-link to="/community/board">Back</router-link> 
    </nav>
  <div class="board-list">

    <h1 class="back">Board Detail</h1>
    <div v-if="article" class="article-container">
      <div class="like-buttons">
        <h1 @click="toggleLike(comment)" v-if="article.like_user.includes(whoid)">💖</h1>
        <h1 @click="toggleLike(comment)" v-if="!article.like_user.includes(whoid)">🖤</h1>
      </div>

      <h3 class="article-title">{{ article.title }}</h3>
      <div class="author-follow-container">
        <p class="author">작성자: {{ article.username }}</p>
        <div class="follow-buttons">
          <button @click="follow(article.user)" class="follow-button" v-if="article.username!=who && article.follow.includes(`${who}`)">언팔로우</button>
          <button @click="follow(article.user)" class="follow-button" v-if="article.username!=who && !article.follow.includes(`${who}`)">팔로우</button>
        </div>
      </div>
      <p class="article-content">내용 : {{ article.content }}</p>
      <p class="timestamp">만든 시간: {{ formatDate(article.created_at) }}</p>
      <p class="timestamp">수정 시간: {{ formatDate(article.updated_at) }}</p>

      <!-- Comments Section -->
      <div class="comment-list">
        <h4>댓글 목록</h4>
        <div v-for="commentt in this.article.comment_set" :key="'dat'+commentt.id" class="comment">
          <div>{{ commentt.username }}: {{ commentt.content }}</div>
          <div v-if="commentt.username == who" class="comment-actions">
            <input type="text" v-model="update_dat" @keyup.enter="toggleEdit(commentt.id)" class="edit-comment">
            <input type="submit" @click="toggleEdit(commentt.id)" class="action-button edit-button" value="수정">
            <button @click="deleteComment(commentt.id, commentt.username)" class="action-button delete-button">삭제</button>
          </div>
        </div>
      </div>

      <!-- Comment Input Section -->
      <div class="comments-list">
        <h4>댓글 작성</h4>
        <textarea id="comments" v-model="comments" class="comment-input"></textarea>
        <input type="submit" @click="fnCreateComment()" class="action-button submit-button">
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>

.big {
  width: 100%;
  height: 100%;
}

.board-list {
  max-width: 800px;
  margin: auto;
  margin-top:100px;
  font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;

  padding: 1em;
  background: #FAFAFA;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}


.my-nav {
    width: 100%;
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

.back {
  text-align: center;
  margin-top: 20px;
  color: #333;
  font-size: 1.8em;
  padding: 20px;
}

.article-container {
  border-radius: 5px;
  padding: 20px;
  margin-top: 20px;
  background: #FFF;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.like-buttons {
  display: flex;
  justify-content: center;
  font-size: 2em;
  cursor: pointer;
}

.article-title {
  font-weight: bold;
  font-size: 1.5em;
  margin-top: 10px;
}

.author-follow-container {
  display: flex;
  /* justify-content: space-between; */
  align-items: center;
  margin-top: 20px;
}

.author {
  margin-left: auto;
  align-items: center;
}

.follow-buttons {
  display: flex;
}

.follow-button {
  background-color: #008CBA;
  border: none;
  color: white;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 1em;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 5px;
  transition-duration: 0.4s;
}

.follow-button:hover {
  background-color: #4CAF50;
  color: white;
}

.article-content, .timestamp {
  margin-top: 20px;
}

.comment-list {
  margin-top: 40px;
}

.comment {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}

.comment-actions {
  display: flex;
  justify-content: space-between;
   align-items: left; /* 가운데 정렬을 위해 추가 */
}

.edit-comment {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 5px;
  width: 70%;
}

.action-button {
  background-color: #008CBA;
  border: none;
  color: white;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 1em;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 5px;
  transition-duration: 0.4s;
}

.action-button:hover {
  background-color: #4CAF50;
  color: white;
}

.comments-list {
  margin-top: 20px;
}

.comment-input {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 5px;
}

.submit-button {
  display: block;
  margin-top: 10px;
  width: 100%;
}

.submit-button:hover {
  background-color: #4CAF50;
  color: white
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'BoardDetailView',
  computed: {
    fetchedArticle() {
      return this.article;
    }
  },
  data() {
    return {
      
      article: {}, // 초기화를 빈 객체로 변경
      comments : [],// 댓글을 저장할 배열
      comment: {isLiked : false},
      editedComment: this.originalComment,
      editingCommentId: null,
      // editdat : null,

      isEditing : false,
      formdata : {},
      user: null,
      // update_dat:null,
      
      };
    },


    methods: {
      formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const day = date.getDate();
      const Hours = date.getHours();
      const Minutes = date.getMinutes();
      
      return `${year}년 ${month}월 ${day}일 ${Hours}시 ${Minutes}분`;
    },
      loadArticle(){
        axios.get(`http://127.0.0.1:8000/api/v1/articles/${this.article.id}/`)
        .then((res)=>{
          console.log('정보 업데이트',res)
          this.article = res.data
        })
        .catch((err)=>{
          console.log(err)
        })
      },
      async fetchArticles() {
      let id = this.$route.params.id
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common.Authorization = `Token ${token}`;
      

      const response = await axios.get('http://127.0.0.1:8000/api/v1/articles/' + id + '/');
      this.article = response.data;
      
      },
      
      follow(user) {
        // const loggedInUser = JSON.parse(localStorage.getItem('userdata'));
        // const loggedInUsername = loggedInUser ? loggedInUser.username : '';

        const token = localStorage.getItem('access_token');
        axios.defaults.headers.common.Authorization = `Token ${token}`;

        axios.post(`http://127.0.0.1:8000/follow/${user}/`)
          .then(() => {
            console.log(`팔로우 요청이 성공적으로 전송되었습니다. 팔로우 대상: ${user}`);
          })
          .catch((error) => {
            console.error('팔로우 요청에 실패했습니다:', error);
          });
        this.$router.go('')
      },

        // isFollowing(user) {
        //   const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
        //   if (!loggedInUser || !loggedInUser.following) {
        //     return false;
        //   }
        //   return loggedInUser.following.includes(user.id);
        // },

        toggleLike(comment) {
          if (comment.isLiked) {
            // 이미 좋아요를 눌렀을 경우
       
            let di = this.$route.params.id
     
            const token = localStorage.getItem('access_token')
            axios.defaults.headers.common.Authorization = `Token ${token}`
            // 좋아요 취소 API 호출 (PUT)m
            this.$axios
              .get(`http://127.0.0.1:8000/api/v1/like/${di}/`)
              .then(() => {
                this.article.like_count--;
                this.comment.isLiked = false;
                this.saveLikedStatus(false); // 좋아요 상태를 스토리지에 저장
              })
              .catch((error) => {
                console.error(error);
              });
          } else {
            let di = this.$route.params.id
            // 좋아요를 누르지 않았을 경우
            // 좋아요 추가 API 호출 (PUT)
            const token = localStorage.getItem('access_token');
            axios.defaults.headers.common.Authorization = `Token ${token}`;
            this.$axios
              .get(`http://127.0.0.1:8000/api/v1/like/${di}/`)
              .then(() => {
                this.article.like_count++;
                this.comment.isLiked = true;
                this.saveLikedStatus(true); // 좋아요 상태를 스토리지에 저장
              })
              .catch((error) => {
                console.error(error);
              });
            this.$router.go('')
          }
        },
        toggleEdit(item) {
          console.log(this.$data)
          console.log(this.update_dat)
          console.log(item)
          axios
            .put(`http://127.0.0.1:8000/api/v1/comments/${item}/`, {"content" : this.update_dat})
            .then((response)=>{
              console.log(response)
            })
            .catch((err)=>{
              console.log(err)
            })
            this.$router.go('')
        },

        getLikedStatus() {
          const status = localStorage.getItem('liked'); // 로컬 스토리지에서 좋아요 상태를 가져옴
          return status === 'true'; // 문자열을 불리언 값으로 변환하여 반환
        },
    deleteComment(commentId, commentOwner) {
      let userdata = JSON.parse(localStorage.getItem('userdata'));
      let currentUserId = userdata.username;
    
      // 사용자가 글 작성자인지 확인
      console.log('Deleting post with id:', commentId);
      console.log('currentUserId', currentUserId);
      
      if (currentUserId == commentOwner) {
      
          // API 호출 등으로 실제 삭제 구현
   
          const token = localStorage.getItem('access_token')
          axios.defaults.headers.common.Authorization = `Token ${token}`
          this.$axios.delete('http://127.0.0.1:8000/api/v1/comments/'+commentId +'/', {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              })
              .then(response => {
                console.log(response);
                console.log('댓글 삭제 성공');
                this.fetchArticles(); // 최신 댓글 목록 다시 가져오기
              })
              .catch(error => {
                console.error(error);
                const error_msg = error.request.response;
                console.log('에러메세지는', error_msg);
                const real_error = JSON.parse(error_msg);
                this.error_msg = real_error;
                alert('오류 메세지를 확인하세요.' , error);
                console.log(currentUserId,'currentUserId')
                console.log(userdata,'userdata')
              });
        
      } else {
        alert('내 글만 삭제가 가능합니다');

      }
    },
    
    fnCreateComment() {
      // let userdata = JSON.parse(localStorage.getItem('userdata'));
      // let currentUserId = userdata.username;
      console.log(this.comments)
      const comment = this.comments
      // const username = this.username
      const formData = {'content' :comment}
    if (!comment) {
      alert('댓글을 입력해주세요');
      return;
    } 
      let id = this.$route.params.id;
      const token = localStorage.getItem('access_token')
      axios.defaults.headers.common.Authorization = `Token ${token}`
      console.log(formData)
      axios
      .post('http://127.0.0.1:8000/api/v1/articles/' + id + '/comments/', formData, {
        headers: {
          "Content-Type": "application/json",
          // 'Access-Control-Allow-Origin': '*',
        },
      })
      .then(res => {  
        console.log(res);  // 응답을 콘솔에 출력하기 위해 추가
        // 응답 데이터를 이벤트로 전달
        this.fetchArticles(); // 최신 댓글 목록 가져오기
        this.comments = '';
        
     

      })
      .catch(err => {  
        console.log('댓글 에러임',err);  // 에러를 콘솔에 출력하기 위해 추가
        alert('잠시 후 다시 시도해주세요.');
      });
     },
    joinDepoist() {
      let id = this.$route.params.id;
      const token = localStorage.getItem('access_token')
      axios.defaults.headers.common.Authorization = `Token ${token}`
      // DB api요청 -> 스토어에 저장 -> 로컬스토리지 저장
      this.$axios
      .get('http://127.0.0.1:8000/api/v1/articles/' +id+ '/', {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then(res => {
            console.log(res)

            const userdata = res.data;
            this.$store.dispatch('SET_USER', userdata);
          }
          )
          .catch(err => {
            console.log(err)
          })
        }
      },
    async created() {
      this.who = JSON.parse(localStorage.getItem('userdata')).username;
      this.whoid = JSON.parse(localStorage.getItem('userdata')).id;
      this.fetchArticles();
      // 페이지가 로드될 때 좋아요 상태를 가져와서 적용
      this.comment.isLiked = this.getLikedStatus();
    }, 
    mounted() {
      let id = this.$route.params.id
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common.Authorization = `Token ${token}`;
      
      axios.get('http://127.0.0.1:8000/api/v1/articles/' + id + '/') // 댓글 데이터를 가져오는 API 요청 예시
      .then(response => {
        this.article = response.data; // 받아온 댓글 데이터를 할당
      })
      .catch(error => {
        console.log(error)
      })
  }



    }

</script>