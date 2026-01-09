<template>
  <div class="auth-container">
    <div class="auth-wrapper">
      <!-- Decorative Background -->
      <div class="auth-background"></div>

      <!-- Auth Card -->
      <div class="auth-card">
        <!-- Header -->
        <div class="auth-header">
          <h2>{{ activeTab === 'login' ? '欢迎回来' : '加入我们' }}</h2>
          <p class="auth-subtitle">
            {{ activeTab === 'login' ? '登录您的账户' : '创建新账户开始体验' }}
          </p>
        </div>

        <!-- Tabs -->
        <div class="auth-tabs">
          <button
            :class="['tab-button', { active: activeTab === 'login' }]"
            @click="switchTab('login')"
          >
            <span class="tab-icon">→</span>
            登录
          </button>
          <button
            :class="['tab-button', { active: activeTab === 'register' }]"
            @click="switchTab('register')"
          >
            <span class="tab-icon">+</span>
            注册
          </button>
        </div>

        <!-- Forms -->
        <div class="auth-form">
          <transition name="fade" mode="out-in">
            <div v-if="activeTab === 'login'" key="login">
              <LoginForm @login-success="handleLoginSuccess" />
            </div>
            <div v-else key="register">
              <RegisterForm @register-success="handleRegisterSuccess" />
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import LoginForm from '@/components/account/LoginForm.vue';
import RegisterForm from '@/components/account/RegisterForm.vue';

const activeTab = ref('login');

const switchTab = (tab: 'login' | 'register') => {
  activeTab.value = tab;
};

const handleLoginSuccess = () => {
  console.log('登录成功');
};

const handleRegisterSuccess = () => {
  console.log('注册成功');
  activeTab.value = 'login';
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-bg-primary) 0%, var(--color-bg-secondary) 100%);
  padding: var(--spacing-lg);
  position: relative;
  overflow: hidden;
}

.auth-wrapper {
  position: relative;
  width: 100%;
  max-width: 440px;
}

.auth-background {
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 102, 204, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.auth-card {
  background-color: var(--color-bg-secondary);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 100%;
  overflow: hidden;
  position: relative;
  z-index: 1;
  border: 1px solid var(--color-border);
}

.auth-header {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  padding: var(--spacing-xl) var(--spacing-lg);
  text-align: center;
}

.auth-header h2 {
  font-size: 1.8rem;
  margin: 0 0 var(--spacing-xs) 0;
  font-weight: var(--font-weight-bold);
}

.auth-subtitle {
  font-size: 1rem;
  margin: 0;
  opacity: 0.9;
  color: rgba(255, 255, 255, 0.9);
}

/* Auth Tabs */
.auth-tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  background-color: var(--color-bg-primary);
}

.tab-button {
  flex: 1;
  padding: var(--spacing-md);
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
}

.tab-button:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.tab-button.active {
  color: var(--color-primary);
  background-color: var(--color-bg-secondary);
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: var(--color-primary);
}

.tab-icon {
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
}

/* Auth Form */
.auth-form {
  padding: var(--spacing-xl) var(--spacing-lg);
  min-height: 380px;
}

/* Transition Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 480px) {
  .auth-container {
    padding: var(--spacing-md);
  }

  .auth-wrapper {
    max-width: 100%;
  }

  .auth-header {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .auth-header h2 {
    font-size: 1.5rem;
  }

  .auth-form {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .auth-background {
    width: 300px;
    height: 300px;
  }
}
</style>