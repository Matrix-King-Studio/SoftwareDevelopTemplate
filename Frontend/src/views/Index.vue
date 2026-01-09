<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container hero-content">
        <h1 class="hero-title">欢迎来到 Matrix</h1>
        <p class="hero-subtitle">构建未来的现代化应用平台</p>
        <p class="hero-description">
          简洁、高效、专业的解决方案，助力您实现业务目标
        </p>
        <div class="hero-actions">
          <router-link to="/signup_login" class="btn btn-primary">立即开始</router-link>
          <a href="#features" class="btn btn-secondary">了解更多</a>
        </div>
      </div>
    </section>

    <!-- User Profile Section -->
    <section class="user-section">
      <div class="container">
        <UserProfile />
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section" id="features">
      <div class="container">
        <div class="section-header">
          <h2>核心功能</h2>
          <p class="section-subtitle">我们为您提供完整的解决方案</p>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3>快速部署</h3>
            <p>一键部署，快速启动您的项目，让创意快速落地</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>安全可靠</h3>
            <p>企业级安全认证，确保您的数据安全和隐私保护</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>数据分析</h3>
            <p>实时数据分析和展示，帮助您做出更好的决策</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>高性能</h3>
            <p>优化的架构设计，提供稳定和高效的服务体验</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3>全球覆盖</h3>
            <p>多地部署支持，确保用户获得最佳的访问速度</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">💡</div>
            <h3>技术支持</h3>
            <p>24/7 专业技术支持团队，随时准备帮助您解决问题</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container cta-content">
        <h2>准备好开始了吗？</h2>
        <p>加入数千名用户，体验我们的平台</p>
        <router-link to="/signup_login" class="btn btn-primary btn-large">注册免费账户</router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="home-footer">
      <div class="container">
        <p>&copy; 2026 Matrix Frontend. 保留所有权利。</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import UserProfile from '@/components/account/UserProfile.vue';

const router = useRouter();
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  width: 100%;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, var(--color-bg-secondary) 0%, var(--color-bg-primary) 100%);
  padding: var(--spacing-2xl) 0;
  border-bottom: 1px solid var(--color-border);
}

.hero-content {
  text-align: center;
  padding: var(--spacing-xl) var(--spacing-lg);
}

.hero-title {
  font-size: 3.5rem;
  font-weight: var(--font-weight-bold);
  line-height: 1.1;
  margin: 0 0 var(--spacing-md) 0;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
  margin: 0 0 var(--spacing-md) 0;
}

.hero-description {
  font-size: 1.1rem;
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-xl) 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--border-radius-md);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
  display: inline-block;
  cursor: pointer;
  border: none;
  font-family: inherit;
  font-size: 1rem;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-secondary:hover {
  background-color: var(--color-primary-light);
  border-color: var(--color-primary-hover);
}

.btn-large {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: 1.1rem;
}

/* User Section */
.user-section {
  padding: var(--spacing-xl) 0;
  background-color: var(--color-bg-primary);
}

/* Features Section */
.features-section {
  padding: var(--spacing-2xl) 0;
  background-color: var(--color-bg-primary);
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.section-header h2 {
  font-size: 2.5rem;
  margin: 0 0 var(--spacing-md) 0;
  color: var(--color-text-primary);
}

.section-subtitle {
  font-size: 1.1rem;
  color: var(--color-text-secondary);
  margin: 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.feature-card {
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  text-align: center;
  transition: all var(--transition-normal);
  cursor: pointer;
}

.feature-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  display: block;
}

.feature-card h3 {
  font-size: 1.3rem;
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-text-primary);
}

.feature-card p {
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  padding: var(--spacing-2xl) 0;
  color: white;
  text-align: center;
}

.cta-content {
  padding: var(--spacing-xl) var(--spacing-lg);
}

.cta-section h2 {
  font-size: 2.5rem;
  margin: 0 0 var(--spacing-md) 0;
  color: white;
}

.cta-section p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 var(--spacing-xl) 0;
}

.cta-section .btn-primary {
  background-color: white;
  color: var(--color-primary);
}

.cta-section .btn-primary:hover {
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-xl);
}

/* Footer */
.home-footer {
  background-color: var(--color-bg-secondary);
  border-top: 1px solid var(--color-border);
  padding: var(--spacing-lg) 0;
  margin-top: auto;
}

.home-footer p {
  text-align: center;
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 0.95rem;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .hero-section {
    padding: var(--spacing-xl) 0;
  }

  .hero-content {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .hero-actions {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .btn {
    width: 100%;
    text-align: center;
  }

  .section-header h2 {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }

  .cta-section h2 {
    font-size: 2rem;
  }

  .container {
    padding: 0 var(--spacing-md);
  }
}
</style>