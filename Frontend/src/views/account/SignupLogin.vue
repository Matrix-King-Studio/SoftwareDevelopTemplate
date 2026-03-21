<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-hero">
        <p class="hero-kicker">Account Center</p>
        <h2>{{ activeTab === 'login' ? '欢迎回来' : '创建新账号' }}</h2>
        <p>
          {{
            activeTab === 'login'
              ? '登录后即可继续管理你的项目和个人信息。'
              : '几秒钟完成注册，马上开始体验完整功能。'
          }}
        </p>
      </div>

      <div class="auth-tabs" role="tablist" aria-label="登录注册切换">
        <button
          type="button"
          class="tab-button"
          :class="{ active: activeTab === 'login' }"
          @click="switchTab('login')"
        >
          登录
        </button>
        <button
          type="button"
          class="tab-button"
          :class="{ active: activeTab === 'register' }"
          @click="switchTab('register')"
        >
          注册
        </button>
      </div>

      <div class="auth-form">
        <transition name="fade-slide" mode="out-in">
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
</template>

<script setup lang="ts">
import { ref } from 'vue';
import LoginForm from '@/components/account/LoginForm.vue';
import RegisterForm from '@/components/account/RegisterForm.vue';

const activeTab = ref<'login' | 'register'>('login');

const switchTab = (tab: 'login' | 'register') => {
  activeTab.value = tab;
};

const handleLoginSuccess = () => {
  // 登录成功后的跳转逻辑已在 LoginForm 内处理
};

const handleRegisterSuccess = () => {
  activeTab.value = 'login';
};
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 84px);
  display: grid;
  place-items: center;
  padding: clamp(1.2rem, 2.7vw, 2.4rem) var(--spacing-lg);
}

.auth-card {
  width: min(980px, 100%);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  display: grid;
  grid-template-columns: minmax(280px, 1fr) minmax(300px, 1fr);
  position: relative;
}

.auth-card::before,
.auth-card::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.auth-card::before {
  width: 280px;
  height: 280px;
  left: -130px;
  top: -140px;
  background: radial-gradient(circle, rgba(15, 104, 216, 0.2), transparent 70%);
}

.auth-card::after {
  width: 220px;
  height: 220px;
  right: -110px;
  bottom: -110px;
  background: radial-gradient(circle, rgba(23, 156, 61, 0.16), transparent 72%);
}

.auth-hero {
  background: linear-gradient(145deg, #0f68d8, #0b89ab);
  color: #fff;
  padding: clamp(1.5rem, 3vw, 2.2rem);
  position: relative;
  z-index: 1;
}

.hero-kicker {
  margin: 0;
  font-size: 0.86rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.88;
}

.auth-hero h2 {
  margin: 0.5rem 0 0;
  font-size: clamp(1.7rem, 3.3vw, 2.3rem);
  line-height: 1.2;
}

.auth-hero p {
  margin: 0.9rem 0 0;
  max-width: 28ch;
  color: rgba(255, 255, 255, 0.9);
}

.auth-tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  background-color: #f6f8fc;
}

.tab-button {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.8rem;
  cursor: pointer;
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.tab-button:hover {
  color: var(--color-primary);
  background-color: rgba(15, 104, 216, 0.06);
}

.tab-button.active {
  color: var(--color-primary);
  background-color: #fff;
  box-shadow: inset 0 -2px 0 var(--color-primary);
}

.auth-form {
  grid-column: 2;
  grid-row: 1 / span 2;
  padding: clamp(1.1rem, 2.4vw, 1.7rem);
  position: relative;
  z-index: 1;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all var(--transition-normal);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(5px);
}

@media (max-width: 900px) {
  .auth-page {
    min-height: auto;
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .auth-card {
    grid-template-columns: 1fr;
  }

  .auth-tabs {
    grid-column: 1;
    grid-row: 2;
  }

  .auth-form {
    grid-column: 1;
    grid-row: 3;
  }
}
</style>
