<template>
    <div class="category-articles-page">
        <PageNavBar :title="categoryName" />
        <div class="article-list">
            <PostCard v-for="post in articles" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
                <template #footer>
                    <div class="post-stats">
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
const categoryName = ref(route.query.name || '分类')
const articles = ref([
    { post_id: 1, title: 'Python多线程实战', summary: '详细介绍Python多线程的使用方法', view_count: 1205, like_count: 86 },
    { post_id: 2, title: 'Python异步编程', summary: 'asyncio模块的使用技巧', view_count: 892, like_count: 64 }
])
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.category-articles-page { background: #f5f5f5; min-height: 100vh; }
.article-list { padding: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
