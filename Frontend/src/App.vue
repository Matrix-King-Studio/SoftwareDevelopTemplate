<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="header-container">
        <div class="header-brand">
          <span class="brand-logo">Matrix</span>
          <span class="brand-text">Frontend</span>
        </div>
        <nav class="app-nav">
          <RouterLink to="/" class="nav-link">首页</RouterLink>
          <RouterLink to="/signup_login" class="nav-link">登录/注册</RouterLink>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-header {
  background-color: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-md) 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
}

.brand-logo {
  display: inline-flex;
  width: 32px;
  height: 32px;
  align-items: center;
  justify-content: center;
  background-color: var(--color-primary);
  color: white;
  border-radius: var(--border-radius-md);
  font-size: 1.2rem;
}

.brand-text {
  color: var(--color-text-primary);
}

.app-nav {
  display: flex;
  gap: var(--spacing-lg);
  align-items: center;
}

.nav-link {
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: color var(--transition-fast), background-color var(--transition-fast);
}

.nav-link:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.nav-link.router-link-active {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.main-content {
  flex: 1;
  background-color: var(--color-bg-primary);
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .app-nav {
    width: 100%;
    justify-content: center;
  }

  .brand-text {
    display: none;
  }
}
</style>