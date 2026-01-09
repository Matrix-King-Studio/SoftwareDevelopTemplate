import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import accountApi from '@/api/account';

const STORAGE_KEY_TOKEN = 'auth_token';
const STORAGE_KEY_USER = 'auth_user';

export const useAccountStore = defineStore('account', () => {
  const userInfo = ref<any>(null);
  const token = ref<string | null>(null);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  const isLoggedIn = computed(() => !!userInfo.value);

  // 初始化：从localStorage恢复登录状态
  const initializeAuth = () => {
    try {
      const savedToken = localStorage.getItem(STORAGE_KEY_TOKEN);
      const savedUser = localStorage.getItem(STORAGE_KEY_USER);

      if (savedToken && savedUser) {
        token.value = savedToken;
        userInfo.value = JSON.parse(savedUser);
      }
    } catch (err) {
      console.error('Failed to restore auth state:', err);
      localStorage.removeItem(STORAGE_KEY_TOKEN);
      localStorage.removeItem(STORAGE_KEY_USER);
    }
  };

  // 保存登录状态到localStorage
  const saveAuthState = (newToken: string, newUserInfo: any) => {
    token.value = newToken;
    userInfo.value = newUserInfo;
    localStorage.setItem(STORAGE_KEY_TOKEN, newToken);
    localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(newUserInfo));
  };

  // 清除localStorage中的登录状态
  const clearAuthState = () => {
    token.value = null;
    userInfo.value = null;
    localStorage.removeItem(STORAGE_KEY_TOKEN);
    localStorage.removeItem(STORAGE_KEY_USER);
  };

  const login = async (username: string, password: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await accountApi.login({ username, password });
      const newToken = response.data.key; // 假设后端返回token在data.key字段
      const newUserInfo = response.data.user || { username }; // 假设有用户信息

      // 保存到localStorage
      saveAuthState(newToken, newUserInfo);

      return { success: true, data: response.data };
    } catch (err: any) {
      error.value = err.message || '登录失败';
      return { success: false, error: err.message };
    } finally {
      isLoading.value = false;
    }
  };

  const register = async (username: string, email: string, password1: string, password2: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await accountApi.register({ username, password1, password2, email });
      return { success: true, data: response.data };
    } catch (err: any) {
      error.value = err.message || '注册失败';
      return { success: false, error: err.message };
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    clearAuthState();
  };

  const fetchUserInfo = async () => {
    try {
      const response = await accountApi.getUserDetail();
      userInfo.value = response.data;
      // 也保存到localStorage
      if (token.value) {
        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(response.data));
      }
      return { success: true, data: response.data };
    } catch (err: any) {
      error.value = err.message || '获取用户信息失败';
      return { success: false, error: err.message };
    }
  };

  return {
    userInfo,
    token,
    isLoading,
    error,
    isLoggedIn,
    login,
    register,
    logout,
    fetchUserInfo,
    initializeAuth
  };
});