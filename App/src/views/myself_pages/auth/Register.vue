<template>
    <div class="register-page">
        <PageNavBar title="注册" />
        <div class="register-header">
            <div class="logo">
                <img src="/imgs/bo_luo_tb.png" alt="logo" class="logo-img" />
            </div>
            <h2>欢迎注册</h2>
            <p class="subtitle">加入CodeSearch，发现优质代码</p>
        </div>
        <div class="register-form">
            <van-field v-model="usernumber" label="账号" placeholder="请输入账号" />
            <van-field v-model="username" label="昵称" placeholder="请输入昵称" />
            <van-field v-model="password" type="password" label="密码" placeholder="请输入密码" />
            <van-field v-model="confirmPassword" type="password" label="确认密码" placeholder="请再次输入密码" />
            <van-field v-model="email" label="邮箱" placeholder="请输入邮箱（选填）" />
            <div class="form-actions">
                <van-button type="primary" block round :loading="loading" @click="handleRegister">注册</van-button>
                <div class="form-links">
                    <span class="link" @click="goToLogin">已有账号？去登录</span>
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
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const email = ref('')
const loading = ref(false)
const handleRegister = async () => {
    if (!usernumber.value.trim()) { showToast('请输入账号'); return }
    if (!username.value.trim()) { showToast('请输入昵称'); return }
    if (!password.value.trim()) { showToast('请输入密码'); return }
    if (password.value !== confirmPassword.value) { showToast('两次密码不一致'); return }
    loading.value = true
    try {
        const data = await userApi.register(usernumber.value, username.value, password.value, email.value)
        setUser({ user_id: data.user_id, username: data.username })
        showToast('注册成功')
        router.replace('/shouye')
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}
const goToLogin = () => { router.replace('/login') }
</script>

<style scoped>
.register-page { min-height: 100vh; background: #f5f5f5; padding: 40px 24px; }
.register-header { text-align: center; margin-bottom: 40px; }
.logo { margin-bottom: 16px; }
.logo-img { width: 64px; height: 64px; }
.register-header h2 { margin: 0 0 8px; font-size: 24px; color: #333; }
.subtitle { margin: 0; font-size: 14px; color: #999; }
.register-form { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
.form-actions { margin-top: 24px; }
.form-links { text-align: center; margin-top: 16px; }
.link { font-size: 14px; color: #1989fa; cursor: pointer; }
</style>
