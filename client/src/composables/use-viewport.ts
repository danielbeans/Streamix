import { onUnmounted, reactive, ref, Ref, watch, watchEffect } from "vue";

export default function useViewport() {
  const viewportSize = ref(window.innerWidth);
  const resizeHandler = () => (viewportSize.value = window.innerWidth);
  window.addEventListener("resize", resizeHandler);
  onUnmounted(() => window.removeEventListener("resize", resizeHandler));
  return { viewportSize };
}
