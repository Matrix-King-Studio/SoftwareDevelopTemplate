<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="container hero-content">
        <p class="hero-eyebrow">Frontend</p>
        <h1 class="hero-title">把产品想法更快交付到用户手里</h1>
        <p class="hero-subtitle">
          统一工程模板、账号体系和页面规范，减少重复搭建时间。
        </p>
        <div class="hero-actions">
          <router-link to="/signup_login" class="btn btn-primary">立即开始</router-link>
          <a href="#features" class="btn btn-secondary">查看能力</a>
        </div>
      </div>
    </section>

    <section class="user-section">
      <div class="container">
        <UserProfile />
      </div>
    </section>

    <section id="features" class="features-section">
      <div class="container">
        <div class="section-header">
          <h2>你可以直接复用的模块</h2>
          <p>从认证、状态管理到页面结构，开箱即可继续业务开发。</p>
        </div>

        <div class="features-grid">
          <article class="feature-card">
            <span class="feature-tag">01</span>
            <h3>基础认证流程</h3>
            <p>内置登录注册逻辑，API 对接方式清晰，方便扩展权限能力。</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">02</span>
            <h3>模块化页面结构</h3>
            <p>首页、账号页与通用组件已拆分，后续新增页面更容易维护。</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">03</span>
            <h3>统一视觉变量</h3>
            <p>颜色、阴影、边距通过全局变量管理，样式一致性更高。</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">04</span>
            <h3>响应式适配</h3>
            <p>移动端与桌面端布局分别优化，避免关键按钮挤压和错位。</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">05</span>
            <h3>可扩展状态管理</h3>
            <p>Pinia store 结构明确，适合继续接入更多业务域的数据流。</p>
          </article>
          <article class="feature-card">
            <span class="feature-tag">06</span>
            <h3>快速部署友好</h3>
            <p>Vite 构建链路轻量，适合本地调试与持续集成环境。</p>
          </article>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="container cta-content">
        <h2>准备好开始你的下一个前端项目了吗？</h2>
        <p>注册一个账户，直接在现有模板上继续开发。</p>
        <router-link to="/signup_login" class="btn btn-primary btn-large">注册免费账户</router-link>
      </div>
    </section>

    <footer class="home-footer">
      <div class="container">
        <p>&copy; 2026 Frontend. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import UserProfile from '@/components/account/UserProfile.vue';
</script>

<style scoped>
.home-page {
  min-height: 100%;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.hero-section {
  padding: 4.6rem 0 3.4rem;
  border-bottom: 1px solid var(--color-border);
  background:
    linear-gradient(130deg, #f9fbff 0%, #eef4ff 55%, #eaf6f2 100%);
}

.hero-content {
  text-align: center;
}

.hero-eyebrow {
  display: inline-block;
  margin: 0 0 var(--spacing-md);
  padding: 0.3rem 0.75rem;
  border-radius: 999px;
  border: 1px solid rgba(15, 104, 216, 0.2);
  color: #0b5fc8;
  background: rgba(15, 104, 216, 0.06);
  font-size: 0.9rem;
}

.hero-title {
  margin: 0;
  font-size: clamp(2rem, 4.6vw, 3.6rem);
  line-height: 1.12;
  color: #0d2748;
}

.hero-subtitle {
  max-width: 680px;
  margin: var(--spacing-md) auto 0;
  font-size: 1.08rem;
  color: var(--color-text-secondary);
}

.hero-actions {
  margin-top: var(--spacing-xl);
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 132px;
  border-radius: 12px;
  padding: 0.66rem 1.2rem;
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.btn-primary {
  color: #fff;
  border: 1px solid transparent;
  background: linear-gradient(135deg, var(--color-primary), #0b83b8);
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  color: #0b5fc8;
  border: 1px solid rgba(15, 104, 216, 0.35);
  background-color: rgba(255, 255, 255, 0.8);
}

.btn-secondary:hover {
  border-color: var(--color-primary);
  background-color: rgba(15, 104, 216, 0.08);
}

.btn-large {
  padding: 0.82rem 1.35rem;
}

.user-section {
  padding: 2.5rem 0 1.25rem;
}

.features-section {
  padding: 2.2rem 0 4rem;
}

.section-header {
  text-align: center;
  margin-bottom: 1.6rem;
}

.section-header h2 {
  margin: 0;
  font-size: clamp(1.6rem, 3.1vw, 2.3rem);
  color: #102c4f;
}

.section-header p {
  margin: 0.65rem 0 0;
  color: var(--color-text-secondary);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--spacing-md);
}

.feature-card {
  position: relative;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  background-color: rgba(255, 255, 255, 0.9);
  padding: 1.2rem;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: rgba(15, 104, 216, 0.35);
  box-shadow: var(--shadow-md);
}

.feature-tag {
  display: inline-block;
  margin-bottom: 0.7rem;
  font-size: 0.78rem;
  font-weight: var(--font-weight-bold);
  letter-spacing: 0.04em;
  color: #0c67cc;
  background-color: rgba(15, 104, 216, 0.11);
  border-radius: 999px;
  padding: 0.18rem 0.56rem;
}

.feature-card h3 {
  margin: 0;
  font-size: 1.05rem;
  color: var(--color-text-primary);
}

.feature-card p {
  margin: 0.6rem 0 0;
  color: var(--color-text-secondary);
  font-size: 0.96rem;
}

.cta-section {
  color: #fff;
  background: linear-gradient(125deg, #0f68d8 0%, #0e8bb7 100%);
}

.cta-content {
  text-align: center;
  padding: 3.2rem var(--spacing-lg);
}

.cta-content h2 {
  margin: 0;
  font-size: clamp(1.55rem, 3.2vw, 2.3rem);
}

.cta-content p {
  margin: 0.8rem 0 1.4rem;
  color: rgba(255, 255, 255, 0.9);
}

.cta-content .btn-primary {
  background: #fff;
  color: #0f68d8;
}

.home-footer {
  border-top: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.7);
}

.home-footer p {
  margin: 0;
  text-align: center;
  color: var(--color-text-secondary);
  padding: var(--spacing-lg) 0;
  font-size: 0.92rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 var(--spacing-md);
  }

  .hero-section {
    padding: 3.4rem 0 2.4rem;
  }

  .hero-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }

  .cta-content {
    padding: 2.6rem var(--spacing-md);
  }
}
</style>
