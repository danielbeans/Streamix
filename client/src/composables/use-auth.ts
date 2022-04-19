import { computed, reactive, toRefs, watch, watchEffect } from "vue";
import useAxios from "./use-axios";
import { onMounted } from "@vue/runtime-core";
export interface AuthObject {
  access_token: string;
}

export interface JWTObject {
  readonly id: string;
  readonly name: string;
  readonly username: string;
  readonly email: string;
  readonly exp: number;
  readonly hasSpotifyAuth: boolean;
  readonly hasYoutubeAuth: boolean;
}

const authState = reactive<AuthObject>({
  access_token: localStorage.getItem("access_token") ?? ``,
});

const jwt = reactive<JWTObject>({
  id: ``,
  name: ``,
  username: ``,
  email: ``,
  hasSpotifyAuth: false,
  hasYoutubeAuth: false,
  exp: 0,
});

export default function useAuth(refresh = false) {
  const initialAuthState = reactive<AuthObject>({
    access_token: ``,
  });

  const intialJWT = reactive<JWTObject>({
    id: ``,
    name: ``,
    username: ``,
    email: ``,
    hasSpotifyAuth: false,
    hasYoutubeAuth: false,
    exp: 0,
  });

  const { run, data, status } = useAxios<AuthObject>({
    method: `POST`,
    url: `/api/auth/token`,
    headers: {
      "Content-Type": `application/json`,
    },
    data: authState,
  });

  const isNotExpired = computed(() => jwt.exp < Date.now());

  const isValidAuth = computed(
    () => authState.access_token && jwt.id && isNotExpired
  );

  const isLoggedIn = computed(() => !!isValidAuth.value);

  const authenticate = async () => {
    if (!refresh && isLoggedIn.value && isValidAuth.value) return false;
    try {
      await run();
      if (data.value !== null) Object.assign(authState, data.value); // ! Remember to check status for success
      return true;
    } catch (e: unknown) {
      console.error(e);
      return new Error((e as Error).message);
    }
  };

  const unauthenticate = () => {
    Object.assign(authState, initialAuthState);
    Object.assign(jwt, intialJWT);
  };

  const setAccessToken = (accessToken: string) =>
    (authState.access_token = accessToken);

  const decodeJWT = (token: string): JWTObject | null => {
    try {
      return JSON.parse(atob(token.split(`.`)[1]));
    } catch (e) {
      return null;
    }
  };

  watch(authState, () => {
    localStorage.setItem("access_token", authState.access_token);
    Object.assign(jwt, decodeJWT(authState.access_token));
  });

  onMounted(() => {
    authState.access_token &&
      Object.assign(jwt, decodeJWT(authState.access_token));
  });

  return {
    authenticate,
    unauthenticate,
    isLoggedIn,
    isValidAuth,
    requestNewToken: run,
    setAccessToken,
    ...toRefs(authState),
    ...toRefs(jwt),
  };
}
