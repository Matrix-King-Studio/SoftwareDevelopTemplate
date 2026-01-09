<template>
  <div class="login-form">
    <h3>登录账户</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名</label>
        <input
          id="username"
          v-model="formData.username"
          type="text"
          placeholder="请输入用户名或邮箱"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input
          id="password"
          v-model="formData.password"
          type="password"
          placeholder="请输入密码"
          required
        />
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="!loading">登录</span>
          <span v-else>
            <span class="spinner"></span>
            登录中...
          </span>
        </button>
      </div>

      <div v-if="errorMessage" class="error-message">
        <span class="error-icon">!</span>
        {{ errorMessage }}
      </div>

      <div class="form-footer">
        <a href="#" class="forgot-password">忘记密码？</a>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useRouter } from 'vue-router';

const emit = defineEmits<{
  'login-success': []
}>();

const accountStore = useAccountStore();
const router = useRouter();

const formData = reactive({
  username: '',
  password: ''
});

const loading = computed(() => accountStore.isLoading);
const errorMessage = ref('');

const handleSubmit = async () => {
  if (!formData.username || !formData.password) {
    errorMessage.value = '请填写完整的登录信息';
    return;
  }

  errorMessage.value = '';

  const result = await accountStore.login(formData.username, formData.password);

  if (result.success) {
    console.log('登录成功');
    emit('login-success');
    router.push('/');
  } else {
    console.error('登录失败:', result.error);
    errorMessage.value = result.error || '登录失败，请检查用户名和密码';
  }
};
</script>

<style scoped>
.login-form {
  width: 100%;
}

.login-form h3 {
  margin: 0 0 var(--spacing-lg) 0;
  text-align: center;
  color: var(--color-text-primary);
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-xs);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
  font-size: 0.95rem;
}

.form-group input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: 1rem;
  box-sizing: border-box;
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  transition: all var(--transition-fast);
}

.form-group input::placeholder {
  color: var(--color-text-secondary);
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.form-actions {
  margin: var(--spacing-lg) 0;
}

.submit-btn {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius-md);
  font-size: 1rem;
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
}

.submit-btn:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background-color: var(--color-border-dark);
  cursor: not-allowed;
  opacity: 0.7;
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  background-color: #fff1f0;
  color: var(--color-error);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  margin-top: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 0.95rem;
  border: 1px solid #ffccc7;
}

.error-icon {
  display: inline-flex;
  width: 20px;
  height: 20px;
  align-items: center;
  justify-content: center;
  background-color: var(--color-error);
  color: white;
  border-radius: 50%;
  font-weight: var(--font-weight-bold);
  font-size: 0.8rem;
}

.form-footer {
  text-align: right;
  margin-top: var(--spacing-md);
}

.forgot-password {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color var(--transition-fast);
}

.forgot-password:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}
</style>