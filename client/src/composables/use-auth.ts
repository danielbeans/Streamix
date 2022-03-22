import { computed, reactive, ref, watchEffect } from "vue";
import { FetchStatus } from "../enum/status.enum";
import useAxios from "./use-axios";
export interface AuthObject {
  refresh_token: string;
  access_token: string;
  expires_at: number;
}

export default function useAuth(authInfo: AuthObject | null = null) {
  const auth = ref<AuthObject>({
    refresh_token: localStorage.getItem("access_token") ?? ``,
    access_token: localStorage.getItem("refresh_token") ?? ``,
    expires_at: parseInt(localStorage.getItem("expires_at") ?? `0`),
  });

  const { run, data, status } = useAxios<AuthObject>({
    method: `POST`,
    url: `/api/auth/token`,
    headers: {
      "Content-Type": `application/json`,
    },
    data: auth,
  });

  const tokenIsExpired = computed(() => auth.value.expires_at >= Date.now());

  const isValidAuth = computed(
    () => auth.value.refresh_token && auth.value.access_token && !tokenIsExpired
  );

  const isLoggedIn = computed(() => isValidAuth); // ! may not update, check for proper reactivity

  const authenticate = async () => {
    if (isLoggedIn) return false;
    try {
      // await run();
      if (true) auth.value = data.value as AuthObject; // ! this may pose a problem, test for proper reactivity
      return true;
    } catch (e: unknown) {
      console.error(e);
      return new Error((e as Error).message);
    }
  };

  watchEffect(() =>
    localStorage.setItem("access_token", auth.value.access_token)
  );

  watchEffect(() =>
    localStorage.setItem("refresh_token", auth.value.refresh_token)
  );

  watchEffect(() =>
    localStorage.setItem("expires_at", JSON.stringify(auth.value.expires_at))
  );

  return { authenticate, isLoggedIn, isValidAuth };
}
