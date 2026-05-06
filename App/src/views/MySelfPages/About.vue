<template>
    <div class="about-page">
        <van-nav-bar title="关于我们" left-arrow @click-left="goBack" fixed placeholder />
        <div class="about-content">
            <van-image width="80px" height="80px" src="https://img.yzcdn.cn/vant/cat.jpeg" />
            <h3>CodeSearchProject</h3>
            <p>版本 1.0.0</p>
            <p>基于Sanic后端 + Vue3移动端的代码搜索与内容分享平台</p>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const goBack = () => router.back()
</script>

<style scoped>
.about-page { background: #f5f5f5; min-height: 100vh; }
.about-content { display: flex; flex-direction: column; align-items: center; padding: 40px 16px; }
.about-content h3 { margin: 16px 0 8px; font-size: 20px; color: #333; }
.about-content p { margin: 4px 0; font-size: 14px; color: #999; }
</style>
