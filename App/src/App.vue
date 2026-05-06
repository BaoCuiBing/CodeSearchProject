<template>
    <div class="app-container">
        <router-view />
        <van-tabbar v-if="showTabbar" route active-color="#1989fa" inactive-color="#7d7e80">
            <van-tabbar-item replace to="/shouye" icon="wap-home-o">首页</van-tabbar-item>
            <van-tabbar-item replace to="/faxian" icon="fire-o">发现</van-tabbar-item>
            <van-tabbar-item replace to="/message" icon="chat-o" badge="5">消息</van-tabbar-item>
            <van-tabbar-item replace to="/myself" icon="user-o">我的</van-tabbar-item>
        </van-tabbar>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const tabbarRoutes = ['/shouye', '/faxian', '/message', '/myself']
const showTabbar = computed(() => tabbarRoutes.includes(route.path))
</script>

<style scoped>
.app-container {height: 100vh; display: flex; flex-direction: column;}
</style>
