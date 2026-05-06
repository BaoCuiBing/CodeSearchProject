<template>
    <div class="history-page">
        <van-nav-bar title="浏览历史" left-arrow @click-left="goBack" fixed placeholder />
        <div class="article-list">
            <div v-for="item in historyList" :key="item.post_id" class="post-card" @click="goToDetail(item.post_id)">
                <h4>{{ item.title }}</h4>
                <p>{{ item.summary }}</p>
                <div class="post-stats">
                    <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                    <span><van-icon name="clock-o" /> {{ item.view_time }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const historyList = ref([
    { post_id: 1, title: 'Python多线程实战', summary: '详细介绍Python多线程的使用方法', view_count: 1205, view_time: '2024-01-15' },
    { post_id: 2, title: 'Python异步编程', summary: 'asyncio模块的使用技巧', view_count: 892, view_time: '2024-01-14' }
])
const goBack = () => router.back()
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.history-page { background: #f5f5f5; min-height: 100vh; }
.article-list { padding: 12px; }
.post-card { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.post-card h4 { margin: 0 0 8px; font-size: 16px; }
.post-card p { margin: 0 0 12px; font-size: 14px; color: #666; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; }
</style>
