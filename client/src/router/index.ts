import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import Dashboard from "../views/Dashboard.vue";
import Migrate from "../views/Migrate.vue";
import useAuth from "../composables/use-auth";
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "Signup",

    component: Signup,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/migrate/:id",
    name: "Migrate",
    component: Migrate,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// router.replace(`/login`);

router.beforeEach((to, from, next) => {
  const { isLoggedIn } = useAuth();
  if (isLoggedIn.value && (to.name === `Login` || to.name === `Signup`))
    next(`/dashboard`);
  else if (
    !isLoggedIn.value &&
    (to.name === `Dashboard` || to.name === `Migrate`)
  )
    next(`/login`);
  else next();
});

export default router;
