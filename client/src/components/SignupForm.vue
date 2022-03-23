<template>
  <section class="login-form text-center mt-10 mx-auto w-full">
    <h3 class="text-3xl mb-5">Welcome</h3>
    <p class="text-black-400 mb-3">
      Already have an existing account?
      <router-link
        class="text-blue-500 font-bold hover:underline underline-offset-4"
        to="/login"
        >Log in.</router-link
      >
    </p>

    <div class="flex flex-col md:w-1/2 xl:w-1/3 mx-8 md:mx-auto">
      <el-input
        type="text"
        size="large"
        v-model="form.name"
        placeholder="First Name"
        class="mr-4 my-2"
      />

      <el-input
        type="text"
        size="large"
        v-model="form.username"
        placeholder="Username"
        class="my-2"
      />

      <div
        v-if="errors.username"
        class="bg-red-100 border flex items-center border-red-400 text-red-700 px-4 py-2 rounded relative"
        role="alert"
      >
        <span class="block sm:inline text-sm"
          >Your username can only contain alphanumeric characters.</span
        >
        <span class="absolute top-0 bottom-0 right-0 px-4 py-3"> </span>
      </div>

      <div
        v-if="errors.firstName || errors.lastName"
        class="bg-red-100 border flex items-center border-red-400 text-red-700 px-4 py-2 rounded relative"
        role="alert"
      >
        <span class="block sm:inline text-sm"
          >Your name can only contain alphabetical characters (no numbers,
          symbols, or spaces).</span
        >
        <span class="absolute top-0 bottom-0 right-0 px-4 py-3"> </span>
      </div>

      <el-input
        type="text"
        size="large"
        v-model="form.email"
        placeholder="Email"
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

      <el-input
        v-model="form.confirmPassword"
        type="password"
        size="large"
        placeholder="Confirm Password"
        class="my-2"
        show-password
      />

      <div
        v-if="!passwordsMatch"
        class="bg-red-100 border flex items-center border-red-400 text-red-700 px-4 py-2 rounded relative"
        role="alert"
      >
        <span class="block sm:inline text-sm"
          >Your passwords do not match, please make sure your passwords match
          before submitting.</span
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
          >Signup</el-button
        >

        <el-button
          @click="resetForm"
          size="large"
          class="w-full lg:flex-1 lg:ml-3"
          type="danger"
          >Clear</el-button
        >
      </div>
    </div>
    <dialog :open="dialogVisible" class="text-left">
      <el-dialog :show-close="false" v-model="dialogVisible">
        <template #title
          ><div class="text-xl pb-5 border-b-2 border-gray-200">
            {{ dialogInfo.title }}
          </div></template
        >
        <span class="pt-0">{{ dialogInfo.message }}</span>
        <template #footer>
          <el-button type="primary" class="px-8" @click="dialogInfo.action">{{
            dialogInfo.button
          }}</el-button>
        </template>
      </el-dialog>
    </dialog>
  </section>
</template>
<script lang="ts" setup>
import useForm, { ValidationRules } from "../composables/use-form";
import validator from "validator";
import { ref, watch } from "vue";
import { FetchStatus } from "../enum/status.enum";
import useDialog from "../composables/use-dialog";
import { useRouter } from "vue-router";

interface SignupForm {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const router = useRouter();

const validatorRules: ValidationRules = {
  username: (value: string, options = {}) =>
    validator.isAlphanumeric(
      value,
      `en-US`,
      options as validator.IsAlphanumericOptions
    ),
  name: (value: string, options = { ignore: ` ` }) =>
    validator.isAlpha(
      value,
      `en-US`,
      options as validator.IsAlphanumericOptions
    ),
  email: (value: string, options = {}) =>
    validator.isEmail(value, options as validator.IsEmailOptions),
  password: (value: string, options = { min: 8 }) =>
    validator.isLength(value, options as validator.IsLengthOptions),
  confirmPassword: (value: string, options = { min: 8 }) =>
    validator.isLength(value, options as validator.IsLengthOptions),
};

const { resetForm, submitForm, form, errors, data, status } =
  useForm<SignupForm>(
    {
      name: ``,
      username: ``,
      email: ``,
      password: ``,
      confirmPassword: ``,
    },
    validatorRules,
    { url: `/api/auth/signup`, method: `POST` }
  );

const passwordsMatch = ref(true);

const { dialogInfo, dialogVisible } = useDialog(
  status,
  {
    title: `Success`,
    message: `Your account has been created successfully. Please press Ok to continue to the dashboard.`,
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

watch(
  form,
  () =>
    (passwordsMatch.value = form.value.confirmPassword === form.value.password),
  { deep: true }
);
</script>

<style lang="scss">
.el-button + .el-button {
  margin-left: 0 !important;
}
</style>
