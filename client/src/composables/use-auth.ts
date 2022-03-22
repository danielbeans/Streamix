import { computed, reactive, toRefs, watchEffect } from "vue";
import useAxios from "./use-axios";
export interface AuthObject {
  refresh_token: string;
  access_token: string;
  expires_at: number;
}

const authState = reactive<AuthObject>({
  refresh_token: localStorage.getItem("access_token") ?? ``,
  access_token: localStorage.getItem("refresh_token") ?? ``,
  expires_at: parseInt(localStorage.getItem("expires_at") ?? `0`),
});

export default function useAuth() {
  const initialAuthState = reactive<AuthObject>({
    refresh_token: ``,
    access_token: ``,
    expires_at: 0,
  });

  const { run, data, status } = useAxios<AuthObject>({
    method: `POST`,
    url: `/api/auth/token`,
    headers: {
      "Content-Type": `application/json`,
    },
    data: authState,
  });

  const isNotExpired = computed(() => authState.expires_at < Date.now());

  const isValidAuth = computed(
    () =>
      authState.refresh_token && authState.access_token && isNotExpired.value
  );

  const isLoggedIn = computed(() => !!isValidAuth.value);

  const authenticate = async () => {
    if (isLoggedIn.value) return false;
    try {
      // await run();
      data.value = {
        refresh_token: "refresh",
        access_token: "access",
        expires_at: 5,
      };
      if (data.value !== null) Object.assign(authState, data.value); // ! Remember to check status for success
      return true;
    } catch (e: unknown) {
      console.error(e);
      return new Error((e as Error).message);
    }
  };

  const unauthenticate = () => Object.assign(authState, initialAuthState);

  watchEffect(() =>
    localStorage.setItem("access_token", authState.access_token)
  );

  watchEffect(() =>
    localStorage.setItem("refresh_token", authState.refresh_token)
  );

  watchEffect(() =>
    localStorage.setItem("expires_at", JSON.stringify(authState.expires_at))
  );

  return {
    authenticate,
    unauthenticate,
    isLoggedIn,
    isValidAuth,
    ...toRefs(authState),
  };
}
