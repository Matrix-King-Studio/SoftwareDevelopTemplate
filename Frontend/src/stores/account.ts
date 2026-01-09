import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import accountApi from '@/api/account';

export const useAccountStore = defineStore('account', () => {
  const userInfo = ref<any>(null);
  const token = ref<string | null>(null);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  const isLoggedIn = computed(() => !!userInfo.value);

  const login = async (username: string, password: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await accountApi.login({ username, password });
      token.value = response.data.key; // 假设后端返回token在data.key字段
      userInfo.value = response.data.user || { username }; // 假设有用户信息
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
    userInfo.value = null;
    token.value = null;
  };

  const fetchUserInfo = async () => {
    try {
      const response = await accountApi.getUserDetail();
      userInfo.value = response.data;
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
    fetchUserInfo
  };
});