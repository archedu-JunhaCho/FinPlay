<template>
  <div class="main-container">
    <nav class="my-nav">
      <router-link to="/home">Home</router-link> 
      <router-link to="/community/board">돌아가기</router-link>
    </nav>
    <h1 class="back">작성하기</h1><br>


    <div class="box">

    <form @submit.prevent="fnCreateArticle" class="form-container">
      <div class="input-group">
        <label class="back1" for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title"><br>
      </div>

      <div class="input-group">
        <label class="back1" for="content">내용 : </label>
        <textarea id="content" cols="30" rows="10" v-model="content"></textarea><br>
      </div><br>

      <div class="button-wrapper">
        <input type="submit" id="submit" title="Button push black/gray" class="button btnBlackGray btnPush">
      </div>
    </form>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  background-color: #fff;
  color: black;
  font-family: 'Dovemayo_wild', sans-serif; 
  padding: 0px;
  height: 4rem;
  margin: 0 auto;
  align-items: flex-start;
  margin: auto;

 
}

.my-nav {
  color: black;
  font-size: 20px;
  margin-bottom: 40px;
}

.back {
  text-align: center;
  font-size: 40px;
  margin-bottom: 0px;
  margin-top: 150px;
}

.box {
  width: 1000px;
  margin: auto;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 800px;
  margin: auto;
  margin-top: 100px;
}

.input-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 1em;
}

.back1 {
  margin-bottom: .5em;
  color: black;
  text-align: left;
  font-size: 30px;
  margin-top: .5em;
}

#title, #content {
  padding: .5em;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 1em;
}

.button {
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
  font-size: 20px;
  text-decoration: none;
  background: gray;
}

.button:hover {
  box-shadow: 0px 2px 0px 0px rgba(0, 0, 0, 0.3);
  transform: translateY(3px);
}

</style>

<script>
export default {
  name: 'CreateBoardView',
  data() {
    return {
      title: null,
      content: null,
    }
  },
  methods: {
  createArticle() {
    const articleData = {
      title: this.title, // 작성할 글의 제목을 입력하세요
      content: this.content, // 작성할 글의 내용을 입력하세요
    };

    this.$emit('create-article', articleData);
  },
  fnCreateArticle() {
    const title = this.title;
    const content = this.content;
    // const username = this.username

    if (!title) {
      alert('제목을 입력해주세요.');
      return;
    } else if (!content) {
      alert('내용을 입력해주세요.');
      return;
    }

    this.$axios
      .post('http://127.0.0.1:8000/api/v1/articles/', { title, content}, {
        headers: {
          "Content-Type": "application/json",
          // 'Access-Control-Allow-Origin': '*',
        },
      })
      .then(res => {  
        console.log(res);  // 응답을 콘솔에 출력하기 위해 추가
        // 응답 데이터를 이벤트로 전달
        this.$emit('article-created', res.data);
        // 글 작성 후 BoardView.vue로 이동
        this.$router.push({path: '/community/board'});
      })
      .catch(err => {  
        console.log(err);  // 에러를 콘솔에 출력하기 위해 추가
        alert('잠시 후 다시 시도해주세요.');
      });
  }
}

  }

</script>


