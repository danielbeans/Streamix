import axios from "axios";
import { AxiosError, AxiosRequestConfig } from "axios";
import { FetchStatus } from "../enum/status.enum";
import { ref, onUnmounted } from "vue";
import { onMounted } from "@vue/runtime-core";

type ResponseError = { error: string };

export default function useAxios<T>(
  config: AxiosRequestConfig,
  runOnMount = false,
  defaultValue = null
) {
  const status = ref<FetchStatus>(FetchStatus.IDLE);
  const data = ref<T | ResponseError | null>(defaultValue);

  async function fetchData<T>() {
    status.value = FetchStatus.RUNNING;
    try {
      const res = await axios(config);
      status.value = FetchStatus.SUCCESS;
      return JSON.parse(JSON.stringify(res.data)) as T;
    } catch (error) {
      status.value = FetchStatus.ERROR;
      const res = error as AxiosError;
      return (
        res.isAxiosError && res.response
          ? res.response.data
          : { error: `useAxios(${config}): Unable to fetch data.` }
      ) as ResponseError;
    }
  }

  async function run() {
    data.value = await fetchData();
  }

  onMounted(() => runOnMount && run());
  onUnmounted(() => {});
  return { run, data, status };
}
