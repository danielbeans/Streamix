import { ref } from "vue";

export interface AuthObject {
  token: string;
}

export default function useAuth(authInfo: AuthObject | null = null) {
  const auth = ref<AuthObject | null>(authInfo);
  const isLoggedIn = ref(!!auth?.value?.token);

  const setAuth = (newAuth: AuthObject) => {
    auth.value = newAuth;
    isLoggedIn.value = !!auth?.value?.token;
  };

  return { setAuth, isLoggedIn, auth };
}
