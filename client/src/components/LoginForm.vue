<template>
  <section class="login-form mt-10 mx-auto lg:w-full w-1/2">
    <h3 class="text-3xl mb-5">Welcome Back</h3>
    <p class="text-black-400 mb-3">
      New to Streamix?
      <router-link class="text-blue-500 font-bold" to="/signup"
        >Sign up.</router-link
      >
    </p>
    <div class="flex flex-col lg:w-1/4 mx-10 lg:mx-auto">
      <el-input
        type="text"
        size="large"
        v-model="form.email"
        placeholder="Email:"
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
        placeholder="Password:"
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
      <div class="mt-4 flex flex-wrap lg:flex-nowrap">
        <el-button
          size="large"
          @click="submitForm"
          class="w-full mb-5 lg:w-1/2"
          type="success"
          >Login</el-button
        >
        <el-button
          @click="resetForm"
          size="large"
          class="w-full lg:w-1/2 mx-0 lg:mx-3"
          type="danger"
          >Clear
        </el-button>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
interface LoginForm {
  email: string;
  password: string;
}

import useForm, { ValidationRules } from "../composables/use-form";
import validator from "validator";

const validatorRules: ValidationRules = {
  email: (value, options = {}) =>
    validator.isEmail(value, options as validator.IsEmailOptions),
  password: (value: string, options = { min: 8 }) =>
    validator.isLength(value, options as validator.IsLengthOptions),
};

const { resetForm, submitForm, form, errors, data, status } =
  useForm<LoginForm>({ email: ``, password: `` }, validatorRules, {
    url: `/api/login`,
    method: `post`,
  });
</script>
