<template>
    <div class="login-page">
        <PageNavBar title="登录" />
        <div class="login-header">
            <div class="logo">
                <img src="/imgs/bo_luo_tb.png" alt="logo" class="logo-img" />
            </div>
            <h2>CodeSearch</h2>
            <p class="subtitle">让代码搜索更简单</p>
        </div>
        <div class="login-form">
            <van-field v-model="usernumber" label="账号" placeholder="请输入账号" />
            <van-field v-model="password" type="password" label="密码" placeholder="请输入密码" />
            <div class="form-actions">
                <van-button type="primary" block round :loading="loading" @click="handleLogin">登录</van-button>
                <div class="form-links">
                    <span class="link" @click="goToRegister">注册账号</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { userApi } from '@/assets/app_request_api.js'
import { setUser } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
const router = useRouter()
const usernumber = ref('')
const password = ref('')
const loading = ref(false)
const handleLogin = async () => {
    if (!usernumber.value.trim()) { showToast('请输入账号'); return }
    if (!password.value.trim()) { showToast('请输入密码'); return }
    loading.value = true
    try {
        const data = await userApi.login(usernumber.value, password.value)
        setUser({ user_id: data.user_id, username: data.username })
        showToast('登录成功')
        router.replace('/shouye')
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}
const goToRegister = () => { router.push('/register') }
</script>

<style scoped>
.login-page { min-height: 100vh; background: #f5f5f5; padding: 40px 24px; }
.login-header { text-align: center; margin-bottom: 40px; }
.logo { margin-bottom: 16px; }
.logo-img { width: 64px; height: 64px; }
.login-header h2 { margin: 0 0 8px; font-size: 24px; color: #333; }
.subtitle { margin: 0; font-size: 14px; color: #999; }
.login-form { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
.form-actions { margin-top: 24px; }
.form-links { display: flex; justify-content: space-between; margin-top: 16px; }
.link { font-size: 14px; color: #1989fa; cursor: pointer; }
</style>
