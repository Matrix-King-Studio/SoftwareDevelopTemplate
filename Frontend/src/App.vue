<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="header-container">
        <RouterLink to="/" class="header-brand" aria-label="前往首页">
          <span class="brand-logo">M</span>
          <span class="brand-text">Frontend</span>
        </RouterLink>

        <nav class="app-nav" aria-label="主导航">
          <RouterLink to="/" class="nav-link" exact-active-class="is-active">首页</RouterLink>
          <RouterLink to="/signup_login" class="nav-link" active-class="is-active">登录/注册</RouterLink>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 200;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0.8rem var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-lg);
}

.header-brand {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  text-decoration: none;
}

.brand-logo {
  display: inline-flex;
  width: 36px;
  height: 36px;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
  font-weight: var(--font-weight-bold);
  color: #fff;
  background: linear-gradient(140deg, var(--color-primary), #18a9a9);
  box-shadow: var(--shadow-md);
}

.brand-text {
  font-size: 1.06rem;
  font-weight: var(--font-weight-bold);
  letter-spacing: 0.2px;
  color: var(--color-text-primary);
}

.app-nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.nav-link {
  text-decoration: none;
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
  border-radius: 999px;
  padding: 0.44rem 0.88rem;
  transition: all var(--transition-fast);
}

.nav-link:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.nav-link.is-active {
  color: #fff;
  background: linear-gradient(135deg, var(--color-primary), #0c7bb4);
  box-shadow: var(--shadow-sm);
}

.main-content {
  flex: 1;
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    align-items: stretch;
    padding: 0.75rem var(--spacing-md);
    gap: var(--spacing-md);
  }

  .header-brand {
    justify-content: center;
  }

  .app-nav {
    justify-content: center;
  }
}
</style>
