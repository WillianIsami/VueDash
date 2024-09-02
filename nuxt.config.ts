// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },

  typescript: {
    typeCheck: true,
    strict: false,
  },

  modules: ['@nuxt/eslint'],
});
