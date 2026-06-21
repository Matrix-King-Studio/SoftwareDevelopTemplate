import js from '@eslint/js'
import globals from 'globals'
import tseslint from 'typescript-eslint'
import pluginVue from 'eslint-plugin-vue'
import prettier from 'eslint-plugin-prettier'
import prettierConfig from 'eslint-config-prettier'
import vueParser from 'vue-eslint-parser'

/**
 * ESLint Flat Config（ESLint 9+）
 *
 * 技术栈：Vue 3 + TypeScript + Prettier
 * 设计目标：在保证主流规范的同时，与 Prettier 协作（格式交给 Prettier，
 * ESLint 只负责代码质量规则），避免两者冲突。
 */
export default tseslint.config(
  // ── 全局忽略 ──
  {
    ignores: ['dist', 'node_modules', 'build', '*.config.js', '*.config.ts'],
  },

  // ── JavaScript 推荐规则 ──
  js.configs.recommended,

  // ── TypeScript 推荐规则（含风格化规则） ──
  ...tseslint.configs.recommended,
  ...tseslint.configs.stylistic,

  // ── Vue 3 推荐规则（flat 版） ──
  ...pluginVue.configs['flat/recommended'],

  // ── Vue 单文件组件：使用 vue-eslint-parser，内部 <script> 交给 TS parser ──
  {
    files: ['**/*.vue'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tseslint.parser,
        sourceType: 'module',
      },
    },
  },

  // ── 通用规则配置 ──
  {
    files: ['**/*.{js,ts,vue}'],
    plugins: {
      prettier,
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.es2022,
      },
    },
    rules: {
      // Prettier 集成：先关闭与 Prettier 冲突的规则，再把格式问题报为 error
      ...prettierConfig.rules,
      'prettier/prettier': 'error',

      // TypeScript 规则
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
        },
      ],
      '@typescript-eslint/explicit-module-boundary-types': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',

      // Vue 规则
      'vue/multi-word-component-names': 'off',
      'vue/define-macros-order': [
        'error',
        {
          order: ['defineProps', 'defineEmits'],
        },
      ],
      'vue/block-order': [
        'error',
        {
          order: ['template', 'script', 'style'],
        },
      ],
      'vue/component-api-style': ['error', ['script-setup']],

      // 通用规则
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
    },
  }
)
