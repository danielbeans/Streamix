import { reactive, Ref, ref, UnwrapRef, watch } from "vue";
import validator from "validator";
import axios, { AxiosRequestConfig } from "axios";

export type ValidatorFunction = (
  value: string,
  options?:
    | validator.IsLengthOptions
    | validator.IsEmailOptions
    | validator.IsAlphaOptions
) => boolean;

export interface FormState<T> {
  [key: string]: string;
}

export interface FormErrors {
  [key: string]: string | boolean;
}

export interface ValidationRules {
  [key: string]: ValidatorFunction;
}

export default function useForm<T>(
  formState: FormState<T>,
  validationRules: ValidationRules | null = null
) {
  const valid = ref(false);
  const errors = reactive({} as FormErrors);
  const form = ref(formState);

  const resetForm = () =>
    Object.keys(form.value).forEach((i) => (form.value[i] = ``));

  const validateFormData = () => {
    if (validationRules === null) return;
    for (const [formKey, rule] of Object.entries(validationRules)) {
      if (typeof rule !== `function`) continue;
      if (form.value[formKey] === ``) {
        delete errors[formKey];
        continue;
      }
      try {
        const validated = rule(form.value[formKey]); // call function passaed in as second argument
        if (!validated) {
          errors[formKey] = true;
        } else delete errors[formKey]; // if validated successfully, reverse boolean to indicate no errors have occured
      } catch (e) {
        console.error(
          `Error in validation rule for ${formKey}. 
          Please check that you're using the correct configuration of this function before use (LoginForm.vue).`
        );
      }
    }
    valid.value = Object.keys(errors).length <= 0; // check if the value is fully validated
  };

  const submitForm = async <T>(config: AxiosRequestConfig<T>) => {
    try {
      if (!valid.value) throw Error(`Validation error detected`);
      const res = await axios(config);
      return res;
    } catch (err) {
      console.error(`Unable to make request to ${config.url}`, err);
    }
  };

  watch(
    form,
    () => {
      validateFormData();
    },
    { deep: true }
  );

  return {
    resetForm,
    submitForm,
    validateFormData,
    form,
    errors,
    valid,
  };
}
