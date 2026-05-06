<template>
    <div class="settings-page">
        <van-nav-bar title="设置" left-arrow @click-left="goBack" fixed placeholder />
        <van-cell-group>
            <van-cell title="清除缓存" is-link @click="clearCache" />
            <van-cell title="关于我们" is-link @click="goToAbout" />
            <van-cell title="退出登录" is-link @click="logout" />
        </van-cell-group>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
const router = useRouter()
const goBack = () => router.back()
const clearCache = () => { showToast('缓存已清除') }
const goToAbout = () => { router.push('/about') }
const logout = () => { showToast('已退出登录'); router.push('/shouye') }
</script>

<style scoped>
.settings-page { background: #f5f5f5; min-height: 100vh; }
</style>
