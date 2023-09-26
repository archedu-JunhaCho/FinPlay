<template>
  <div class="main-container">
    <nav class="my-nav">
      <router-link to="/home">Home</router-link> |
      <router-link to="/community/board">뒤로가기</router-link>    
    </nav>

    <h3 style="margin-top: 80px;font-size:40px;font-weight:bold">Update Information</h3><br>

     <p style="font-size:20px" v-if="article">userId : {{ article.username }}</p>
      <p style="font-size:20px" v-if="article">만든 시간 : {{ formatDate(article.created_at) }}</p>
      <p style="font-size:20px" v-if="article">수정 시간 : {{ formatDate(article.updated_at)}}</p>
      <p style="font-size:20px" v-if="article">좋아요 몇개? : {{ article.like_count}}</p>

    <form @submit.prevent="updateBoard" class="form-container">
      <div class="input-group">
        <label for="title">제목: </label>
        <input type="text" id="title" v-model="article_title">
      </div><br>

      <div class="input-group">
        <label for="content">내용 : </label>
        <input type="text" id="content" v-model="article_content">
      </div><br>

     
    <div class="container">

      <div class="button-wrapper">
        <input type="submit" value="Update" title="Button push black/gray"  class="button btnBlackGray btnPush">
      </div>
    </div>
    </form>
  </div>
</template>

<style scoped>

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


body {
  margin: 0;
  padding: 0;
}

.main-container {
  background-color: #fff;
  color: #2c3e50;
  font-family: 'Dovemayo_wild', sans-serif; 
  padding: 0px;
  margin: 0 auto;
  align-items: flex-start;
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

h3 {
  text-align: center;
  font-size: 40px;
  margin-bottom: 20px;
  color: #2c3e50;
  font-family: 'Dovemayo_wild', sans-serif; 
}

.form-container {
   display: flex;
  flex-direction: column;
  align-items: center;
  width: 800px;
  margin: auto;
  margin-top: 30px;
  font-size: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 1em;
}

.input-group label {
  margin-bottom: .5em;
  color: #2c3e50;
  text-align: left;
  font-family: 'Dovemayo_wild', sans-serif; 
}

.input-group input {
  padding: .5em;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  color: #2c3e50;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 1em;
}

.button-wrapper input[type="submit"] {
  display: flex;
  justify-content: center;
  width: 100px;
  height: 50px;
  padding: 0;
  margin: 10px 0;
  font-weight: 600;
  text-align: center;
  line-height: 50px;
   background: #2c3e50;
  border-radius: 5px;
  transition: all 0.2s;
  font-family: 'Dovemayo_wild', sans-serif; 
  font-size: 20px;
  text-decoration: none;
}

.button-wrapper input[type="submit"]:hover {
  box-shadow: 0px 2px 0px 0px rgba(0, 0, 0, 0.3);
  transform: translateY(3px);
}

</style>

<script>
export default {
  name: 'changeBoardView',
  data() {
    return {
      article: null,  // 게시물 정보
      article_title: '',
      article_content: '',
    };
  },
  created() {
    let id = this.$route.params.id;
    this.$axios.get('http://127.0.0.1:8000/api/v1/articles/'+id +'/')
      .then(response => {
        this.article = response.data;
        this.article_title = response.data.title;
        this.article_content = response.data.content;
      })
      .catch(error => {
        console.error(error);
      });
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
    updateBoard() {
      const formdata = {
        title: this.article_title,
        content: this.article_content,
      };
      let id = this.$route.params.id;
      this.$axios.put('http://127.0.0.1:8000/api/v1/articles/'+id +'/', formdata, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(response => {
          console.log(response);
          alert('업데이트 성공');
          this.$router.push('/community/board');
        })
        .catch(error => {
          console.error(error);
          const error_msg = error.request.response;
          console.log('에러메세지는', error_msg);
          const real_error = JSON.parse(error_msg);
          this.error_msg = real_error;
          alert('오류 메세지를 확인하세요.' , error);
        });
    }
  },
};
</script>