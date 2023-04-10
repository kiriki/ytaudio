/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  'extends': [
    // 'plugin:vue/vue3-recommended',
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-typescript/recommended'
  ],
  env: {
    'vue/setup-compiler-macros': true
  },
  rules: {
    'vue/no-v-html': 'off', 'vue/no-v-text-v-html-on-component': 'off',
  },
  parserOptions: {
    ecmaVersion: 'latest'
  }
}
