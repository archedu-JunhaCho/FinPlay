import Vue from 'vue';
import Router from 'vue-router';

import StartView from '../components/StartView.vue';
import HomeView from '../components/HomeView.vue';
import LoginView from '../components/user/LoginView.vue';
import ProfileView from '../components/user/ProfileView.vue';
import ProfileUpdateView from '../components/user/ProfileUpdateView.vue';
import createMeView from '../components/user/createMeView.vue';
import DeleteUserView from '../components/user/DeleteUserView.vue';
import RegisterView from '../components/user/RegisterView.vue';
import MapView from '../components/financeService/MapView.vue';
import RateView from '../components/financeService/RateView.vue';
import DepositView from '../components/financeService/DepositView.vue';
import InstallmentView from '../components/financeService/InstallmentView.vue';
import DepositDetailView from '../components/financeService/DepositDetailView.vue';
import InstallmentDetailView from '../components/financeService/InstallmentDetailView.vue';
import RecommendView from '../components/financeService/RecommendView.vue';
import BoardView from '../components/community/BoardView.vue';
import BoardDetailView from '../components/community/BoardDetailView.vue';
import changeBoardView from '../components/community/changeBoardView.vue';
import createBoardView from '../components/community/createBoardView.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Start',
      component: StartView
    },
    {
      path: '/home',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    // 권한이 없을 때 아래 경로로 접속되는 거 막기 => requiresAuth
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView,
      // meta: {requiresAuth:true},
    },
    {
      path: '/profileupdate',
      name: 'ProfileUpdate',
      component: ProfileUpdateView,
      // meta: {requiresAuth:true},
    },
    {
      path: '/profileupdate/avatar',
      name: 'createMeView',
      component: createMeView,
      // meta: {requiresAuth:true},
    },
    {
      path: '/profiledelete',
      name: 'ProfileDelete',
      component: DeleteUserView,
      // meta: {requiresAuth:true},
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/finance/map',
      name: 'Map',
      component: MapView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/finance/rate',
      name: 'Rate',
      component: RateView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/finance/deposit',
      name: 'Deposit',
      component: DepositView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/finance/installment',
      name: 'Installment',
      component: InstallmentView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/finance/deposit/detail/:id',
      name: 'DepositDetail',
      component: DepositDetailView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/finance/installment/detail/:id',
      name: 'InstallmentDetail',
      component: InstallmentDetailView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/finance/recommend',
      name: 'Recommend',
      component: RecommendView,
      // meta: {requiresAuth:true}
    },

    {
      path: '/community/board',
      name: 'Board',
      component: BoardView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/community/board/:id',
      name: 'BoardDetailView',
      component: BoardDetailView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/community/board/change/:id',
      name: 'changeBoardView',
      component: changeBoardView,
      // meta: {requiresAuth:true}
    },
    {
      path: '/community/board/create',
      name: 'createBoardView',
      component: createBoardView,
      // meta: {requiresAuth:true}
    },
  ]
});


// 라우트가 이동될 때 to 라우트 레코드 matched 속성에서 recoard.meta.requiresAuth가 True이면 로그인 권한 체크
// 체크 후 로그인이 되어있지 않으면 (/)으로 가고 로그인이 되어있느면 정상적으로 라우팅

router.beforeEach((to, from, next) => {
  // 1번 해결 로컬스토리지 체크
  const loggedIn = localStorage.getItem('username');
  console.log(to);
  
  // 2번 해결 requiresAuth 체크
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/');
  } else {
    next();
  }
});

export default router;
