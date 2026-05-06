<template>
    <div class="category-detail-page">
        <van-nav-bar :title="category.name" left-arrow @click-left="goBack" fixed placeholder />
        <div class="category-info">
            <van-icon :name="category.icon" size="48" color="#1989fa" />
            <h2>{{ category.name }}</h2>
            <p>{{ category.description }}</p>
            <span class="post-count">{{ category.post_count }} 篇文章</span>
        </div>
        <div class="post-list">
            <div v-for="post in posts" :key="post.post_id" class="post-card" @click="goToDetail(post.post_id)">
                <h4>{{ post.title }}</h4>
                <p>{{ post.summary }}</p>
                <div class="post-meta">
                    <span>{{ post.author.username }}</span>
                    <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                    <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
const category = ref({
    category_id: route.query.id || 1,
    name: '后端开发',
    icon: 'cluster-o',
    description: '服务端开发技术，包括 Python、Java、Go 等语言及框架',
    post_count: 156
})
const posts = ref([
    { post_id: 1, title: '如何在 Python 中实现多线程并发？', summary: '本文详细介绍了 Python 中多线程的使用方法...', author: { username: '程序员小明' }, view_count: 1205, like_count: 86 },
    { post_id: 3, title: 'MySQL 索引失效的常见场景', summary: '总结 MySQL 索引失效的 10 种常见场景...', author: { username: 'DBA老张' }, view_count: 2341, like_count: 156 },
    { post_id: 5, title: 'Docker 容器化部署实战', summary: '从零开始学习 Docker...', author: { username: '运维小李' }, view_count: 987, like_count: 72 }
])
const goBack = () => router.back()
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.category-detail-page { background: #f5f5f5; min-height: 100vh; }
.category-info { background: #fff; padding: 24px; text-align: center; margin-bottom: 8px; }
.category-info h2 { margin: 12px 0 8px; font-size: 20px; color: #333; }
.category-info p { margin: 0 0 8px; font-size: 14px; color: #666; }
.post-count { font-size: 13px; color: #999; }
.post-list { padding: 12px; }
.post-card { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.post-card h4 { margin: 0 0 8px; font-size: 16px; color: #333; }
.post-card p { margin: 0 0 12px; font-size: 14px; color: #666; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.post-meta { display: flex; gap: 16px; font-size: 13px; color: #999; }
</style>
