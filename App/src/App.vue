<template>
    <div class="app-container">
        <router-view />
        <van-tabbar v-if="showTabbar" route active-color="#1989fa" inactive-color="#7d7e80">
            <van-tabbar-item replace to="/shouye" icon="wap-home-o">首页</van-tabbar-item>
            <van-tabbar-item replace to="/faxian" icon="fire-o">发现</van-tabbar-item>
            <van-tabbar-item replace to="/message" icon="chat-o" :badge="unreadCount > 0 ? unreadCount : ''">消息</van-tabbar-item>
            <van-tabbar-item replace to="/myself" icon="user-o">我的</van-tabbar-item>
        </van-tabbar>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { messageApi } from '@/assets/app_request_api.js'
import { getUserId, isLogin } from '@/assets/local_storage.js'
const route = useRoute()
const unreadCount = ref(0)
const tabbarRoutes = ['/shouye', '/faxian', '/message', '/myself']
const showTabbar = computed(() => tabbarRoutes.includes(route.path))
const loadUnreadCount = async () => {
    if (!isLogin()) return
    const data = await messageApi.getUnreadCount(getUserId())
    unreadCount.value = data?.unread_count || 0
}
onMounted(() => { loadUnreadCount() })
</script>

<style scoped>
.app-container {min-height: 100vh; display: flex; flex-direction: column;}
</style>
