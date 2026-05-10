<template>
    <div class="app-container">
        <router-view v-slot="{ Component }">
            <keep-alive :include="['ShouYe', 'FaXian', 'Message', 'MySelf']">
                <component :is="Component" />
            </keep-alive>
        </router-view>
        <van-tabbar v-if="showTabbar" v-model="activeTab" active-color="#1989fa" inactive-color="#7d7e80" @change="onTabChange">
            <van-tabbar-item icon="wap-home-o">首页</van-tabbar-item>
            <van-tabbar-item icon="fire-o">发现</van-tabbar-item>
            <van-tabbar-item icon="chat-o" :badge="unreadCount > 0 ? unreadCount : ''">消息</van-tabbar-item>
            <van-tabbar-item icon="user-o">我的</van-tabbar-item>
        </van-tabbar>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showDialog } from 'vant'
import { messageApi } from '@/assets/app_request_api.js'
import { isLogin } from '@/assets/local_storage.js'
const route = useRoute()
const router = useRouter()
const unreadCount = ref(0)
const activeTab = ref(0)
const tabRoutes = ['/shouye', '/faxian', '/message', '/myself']
const showTabbar = computed(() => tabRoutes.includes(route.path))
watch(() => route.path, (path) => {
    const idx = tabRoutes.indexOf(path)
    if (idx !== -1) { activeTab.value = idx; loadUnreadCount() }
}, { immediate: true })
const loadUnreadCount = async () => {
    if (!isLogin()) return
    try {
        const data = await messageApi.getUnreadCount()
        unreadCount.value = data?.total || 0
    } catch (e) { /* 忽略 */ }
}
const onTabChange = (index) => {
    if (index === 0) { router.replace('/shouye'); return }
    if (!isLogin()) {
        activeTab.value = 0
        showDialog({ title: '提示', message: '请先登录', showCancelButton: false, confirmButtonText: '去登录' }).then(() => { router.push('/login') })
        return
    }
    router.replace(tabRoutes[index])
}
</script>

<style scoped>
.app-container {min-height: 100vh; display: flex; flex-direction: column;}
</style>
