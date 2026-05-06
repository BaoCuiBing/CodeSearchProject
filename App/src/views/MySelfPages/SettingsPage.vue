<template>
    <div class="settings-page">
        <van-nav-bar title="设置" left-arrow @click-left="goBack" fixed placeholder />
        <van-cell-group>
            <van-cell title="账号与安全" is-link @click="goToSecurity" />
            <van-cell title="隐私设置" is-link @click="goToPrivacy" />
            <van-cell title="消息通知" is-link @click="goToNotificationSettings" />
            <van-cell title="清除缓存" is-link @click="clearCache" />
        </van-cell-group>
        <div class="logout-section">
            <van-button block type="danger" plain @click="logout">退出登录</van-button>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const goBack = () => router.back()
const goToSecurity = () => { router.push('/security') }
const goToPrivacy = () => { router.push('/privacy') }
const goToNotificationSettings = () => { router.push('/notification-settings') }
const clearCache = () => {}
const logout = () => { router.push('/login') }
</script>

<style scoped>
.settings-page { background: #f5f5f5; min-height: 100vh; }
.logout-section { padding: 24px 16px; }
</style>
