<template>
  <section class="login-form text-center mt-10 mx-auto w-full">
    <h3 class="text-3xl mb-5">Welcome Back</h3>
    <p class="text-black-400 mb-3">
      New to Streamix?
      <router-link
        class="text-blue-500 font-bold hover:underline cursor-pointer underline-offset-4"
        to="/signup"
        >Sign up.</router-link
      >
    </p>
    <div class="flex flex-col lg:w-1/4 md:w-1/2 mx-8 md:mx-auto">
      <el-input
        type="text"
        size="large"
        v-model="form.username"
        placeholder="Username"
        class="my-2"
      />
      <div
        v-if="errors.email"
        class="bg-red-100 border flex items-center border-red-400 text-red-700 px-4 py-2 rounded relative"
        role="alert"
      >
        <span class="block sm:inline text-sm"
          >Please check your email and try again.</span
        >
        <span class="absolute top-0 bottom-0 right-0 px-4 py-3"> </span>
      </div>
      <el-input
        v-model="form.password"
        type="password"
        size="large"
        placeholder="Password"
        class="my-2"
        show-password
      />
      <div
        v-if="errors.password"
        class="bg-red-100 border flex items-center border-red-400 text-red-700 px-4 py-2 rounded relative"
        role="alert"
      >
        <span class="block sm:inline text-sm"
          >Please make sure your password is greater than 8 characters.</span
        >
        <span class="absolute top-0 bottom-0 right-0 px-4 py-3"> </span>
      </div>
      <div class="mt-4 flex flex-wrap w-full lg:flex-nowrap">
        <el-button
          size="large"
          @click="submitForm"
          :loading="status === FetchStatus.RUNNING"
          class="mb-5 w-full lg:flex-1 lg:mr-3"
          type="primary"
          >Login</el-button
        >
        <el-button
          @click="resetForm"
          size="large"
          class="w-full lg:flex-1 lg:ml-3"
          type="danger"
          >Clear
        </el-button>
      </div>
    </div>
    <dialog :open="dialogVisible" class="text-left">
      <el-dialog :show-close="false" v-model="dialogVisible" width="30%">
        <template #title
          ><div class="text-xl pb-5 border-b-2 border-gray-200">
            {{ dialogInfo.title }}
          </div></template
        >
        <span>{{ dialogInfo.message }}</span>
        <template #footer>
          <el-button type="primary" class="px-8" @click="dialogInfo.action">{{
            dialogInfo.button
          }}</el-button>
        </template>
      </el-dialog>
    </dialog>
  </section>
</template>

<style lang="scss">
.el-dialog__body {
  padding-top: 0 !important;
}
</style>
<script lang="ts" setup>
import useForm, { ValidationRules } from "../composables/use-form";
import validator from "validator";
import { FetchStatus } from "../enum/status.enum";
import useDialog from "../composables/use-dialog";
import { useRouter } from "vue-router";

interface LoginForm {
  email: string;
  password: string;
}

const router = useRouter();

const validatorRules: ValidationRules = {
  username: (value: string, options = {}) =>
    validator.isAlphanumeric(
      value,
      `en-US`,
      options as validator.IsAlphanumericOptions
    ),
  password: (value: string, options = { min: 8 }) =>
    validator.isLength(value, options as validator.IsLengthOptions),
};

const { resetForm, submitForm, form, errors, data, status } =
  useForm<LoginForm>({ username: ``, password: `` }, validatorRules, {
    url: `/api/auth/login`,
    method: `POST`,
  });

const { dialogInfo, dialogVisible } = useDialog(
  status,
  {
    title: `Success`,
    message: `You have successfully logged in. Please press Ok to continue to the dashboard.`,
    button: `Ok`,
    action: () => router.push(`/dashboard`),
  },
  {
    title: `Error`,
    message: `There was an error logging you in. Please check your credentials and try again.`,
    button: `Try again`,
    action: () => {
      resetForm();
      dialogVisible.value = false;
    },
  }
);
</script>
