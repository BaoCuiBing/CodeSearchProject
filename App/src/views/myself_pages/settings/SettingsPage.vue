<template>
    <div class="settings-page">
        <PageNavBar title="设置" />
        <van-cell-group>
            <van-cell title="账号与安全" is-link @click="goToSecurity" />
            <van-cell title="隐私设置" is-link @click="goToPrivacy" />
            <van-cell title="消息通知" is-link @click="goToNotificationSettings" />
            <van-cell title="清除缓存" is-link @click="clearCache" />
        </van-cell-group>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
const router = useRouter()
const goToSecurity = () => { router.push('/security') }
const goToPrivacy = () => { router.push('/privacy') }
const goToNotificationSettings = () => { router.push('/notification-settings') }
const clearCache = () => {}
</script>

<style scoped>
.settings-page { background: #f5f5f5; min-height: 100vh; }
</style>
