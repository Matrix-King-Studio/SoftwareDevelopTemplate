<template>
  <div class="register-form">
    <h3>创建账户</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="reg-username">用户名</label>
        <input
          id="reg-username"
          v-model="formData.username"
          type="text"
          placeholder="请输入用户名"
          required
        />
      </div>

      <div class="form-group">
        <label for="reg-email">邮箱</label>
        <input
          id="reg-email"
          v-model="formData.email"
          type="email"
          placeholder="请输入邮箱地址"
          required
        />
      </div>

      <div class="form-group">
        <label for="reg-password">密码</label>
        <input
          id="reg-password"
          v-model="formData.password1"
          type="password"
          placeholder="请输入密码（至少6位）"
          required
        />
      </div>

      <div class="form-group">
        <label for="reg-confirm-password">确认密码</label>
        <input
          id="reg-confirm-password"
          v-model="formData.password2"
          type="password"
          placeholder="请再次输入密码"
          required
        />
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="!loading">注册</span>
          <span v-else>
            <span class="spinner"></span>
            注册中...
          </span>
        </button>
      </div>

      <div v-if="errorMessage" class="error-message">
        <span class="error-icon">!</span>
        {{ errorMessage }}
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useRouter } from 'vue-router';

const emit = defineEmits<{
  'register-success': []
}>();

const accountStore = useAccountStore();
const router = useRouter();

const formData = reactive({
  username: '',
  password1: '',
  password2: '',
  email: ''
});

const loading = computed(() => accountStore.isLoading);
const errorMessage = ref('');

const handleSubmit = async () => {
  if (!formData.username || !formData.email || !formData.password1 || !formData.password2) {
    errorMessage.value = '请填写完整的注册信息';
    return;
  }

  if (formData.password1 !== formData.password2) {
    errorMessage.value = '两次输入的密码不一致';
    return;
  }

  if (formData.password1.length < 6) {
    errorMessage.value = '密码长度至少为6位';
    return;
  }

  errorMessage.value = '';

  const result = await accountStore.register(
    formData.username,
    formData.email,
    formData.password1,
    formData.password2
  );

  if (result.success) {
    console.log('注册成功');
    emit('register-success');
  } else {
    console.error('注册失败:', result.error);
    errorMessage.value = result.error || '注册失败';
  }
};
</script>

<style scoped>
.register-form {
  width: 100%;
}

.register-form h3 {
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
  background-color: var(--color-success);
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
  background-color: #45a819;
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
</style>