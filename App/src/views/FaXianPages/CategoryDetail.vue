<template>
    <div class="category-detail-page">
        <PageNavBar :title="category.name" />
        <div class="category-info">
            <van-icon :name="category.icon" size="48" color="#1989fa" />
            <h2>{{ category.name }}</h2>
            <p>{{ category.description }}</p>
            <span class="post-count">{{ category.post_count }} 篇文章</span>
        </div>
        <div class="post-list">
            <PostCard v-for="post in posts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
                <template #footer>
                    <div class="post-meta">
                        <span>{{ post.author.username }}</span>
                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                        <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                    </div>
                </template>
            </PostCard>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
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
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.category-detail-page { background: #f5f5f5; min-height: 100vh; }
.category-info { background: #fff; padding: 24px; text-align: center; margin-bottom: 8px; }
.category-info h2 { margin: 12px 0 8px; font-size: 20px; color: #333; }
.category-info p { margin: 0 0 8px; font-size: 14px; color: #666; }
.post-count { font-size: 13px; color: #999; }
.post-list { padding: 12px; }
.post-meta { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
