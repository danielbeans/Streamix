import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
<<<<<<< HEAD
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
=======
import Home from "../views/Home.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
>>>>>>> a5ee137... Scaffold Vue 3.0 and Django Streamix project.
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
