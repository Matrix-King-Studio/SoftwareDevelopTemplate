<template>
  <div class="user-profile">
    <div v-if="accountStore.isLoggedIn" class="profile-card logged-in">
      <div class="profile-avatar">
        <span class="avatar-initials">{{ userInitials }}</span>
      </div>
      <h3 class="profile-name">{{ accountStore.userInfo?.username || '用户' }}</h3>
      <p class="profile-label">已登录用户</p>
      <button @click="handleLogout" class="btn btn-error">退出登录</button>
    </div>
    <div v-else class="profile-card not-logged-in">
      <div class="not-logged-icon">👤</div>
      <p class="not-logged-text">您尚未登录</p>
      <p class="not-logged-hint">登录后可享受更多功能</p>
      <RouterLink to="/signup_login" class="btn btn-primary">立即登录</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useRouter } from 'vue-router';
import { RouterLink } from 'vue-router';

const accountStore = useAccountStore();
const router = useRouter();

const userInitials = computed(() => {
  const username = accountStore.userInfo?.username || '用户';
  return username.slice(0, 2).toUpperCase();
});

const handleLogout = () => {
  accountStore.logout();
  router.push('/signup_login');
};
</script>

<style scoped>
.user-profile {
  width: 100%;
}

.profile-card {
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  text-align: center;
  transition: all var(--transition-normal);
}

.profile-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

/* Logged In State */
.logged-in {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 102, 204, 0.02) 100%);
}

.profile-avatar {
  display: inline-flex;
  width: 80px;
  height: 80px;
  align-items: center;
  justify-content: center;
  background-color: var(--color-primary);
  color: white;
  border-radius: 50%;
  margin-bottom: var(--spacing-lg);
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  box-shadow: var(--shadow-md);
}

.avatar-initials {
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-name {
  font-size: 1.5rem;
  margin: 0 0 var(--spacing-xs) 0;
  color: var(--color-text-primary);
  font-weight: var(--font-weight-bold);
}

.profile-label {
  color: var(--color-text-secondary);
  font-size: 0.95rem;
  margin: 0 0 var(--spacing-lg) 0;
}

/* Not Logged In State */
.not-logged-in {
  background: linear-gradient(135deg, rgba(250, 173, 20, 0.05) 0%, rgba(250, 173, 20, 0.02) 100%);
}

.not-logged-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-lg);
  display: block;
  opacity: 0.8;
}

.not-logged-text {
  font-size: 1.2rem;
  margin: 0 0 var(--spacing-xs) 0;
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
}

.not-logged-hint {
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-lg) 0;
  font-size: 0.95rem;
}

/* Buttons */
.btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--border-radius-md);
  border: none;
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 1rem;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.btn-error {
  background-color: var(--color-error);
  color: white;
  box-shadow: var(--shadow-sm);
}

.btn-error:hover {
  background-color: #e64845;
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .profile-card {
    padding: var(--spacing-lg);
  }

  .profile-avatar {
    width: 64px;
    height: 64px;
    font-size: 1.5rem;
  }

  .profile-name {
    font-size: 1.3rem;
  }
}
</style>