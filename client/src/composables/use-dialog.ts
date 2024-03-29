import { reactive, ref, Ref, watch, watchEffect } from "vue";
import { FetchStatus } from "../enum/status.enum";

interface DialogInfo {
  readonly title: string;
  message: string;
  readonly button: string;
  readonly action: () => void;
}

export default function useDialog<T>(
  status: Ref<FetchStatus>,
  data: Ref<T>,
  successInfo: DialogInfo,
  errorInfo: DialogInfo
) {
  const dialogVisible = ref(false);
  const dialogInfo = reactive<DialogInfo>({
    title: ``,
    message: ``,
    button: ``,
    action: () => void 0,
  });

  watchEffect(() => {
    if (status.value === FetchStatus.SUCCESS)
      Object.assign(dialogInfo, successInfo);
    else if (status.value === FetchStatus.ERROR) {
      // errorInfo.message = data.value.message;
      Object.assign(dialogInfo, errorInfo);
    }
  });

  watch(status, (newStatus) => {
    dialogVisible.value =
      newStatus === FetchStatus.SUCCESS || newStatus === FetchStatus.ERROR;
  });

  return { dialogVisible, dialogInfo };
}
