<template>
    <div class="history-page">
        <PageNavBar title="浏览历史" />
        <div class="article-list">
            <PostCard v-for="item in historyList" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                <template #footer>
                    <div class="post-stats">
                        <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                        <span><van-icon name="clock-o" /> {{ item.view_time }}</span>
                    </div>
                </template>
            </PostCard>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const historyList = ref([
    { post_id: 1, title: 'Python多线程实战', summary: '详细介绍Python多线程的使用方法', view_count: 1205, view_time: '2024-01-15' },
    { post_id: 2, title: 'Python异步编程', summary: 'asyncio模块的使用技巧', view_count: 892, view_time: '2024-01-14' }
])
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.history-page { background: #f5f5f5; min-height: 100vh; }
.article-list { padding: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
