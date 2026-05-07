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
            <van-empty v-if="posts.length === 0" description="暂无文章" />
            <PostCard v-for="post in posts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
                <template #footer>
                    <div class="post-meta">
                        <span>{{ post.author?.username || '' }}</span>
                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                        <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                    </div>
                </template>
            </PostCard>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { categoryApi, articleApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const route = useRoute()
const categoryIcons = ['cluster-o', 'desktop-o', 'phone-o', 'records', 'setting-o', 'photo-fail', 'chart-trending-o', 'bag-o']
const category = ref({ name: '', icon: '', description: '', post_count: 0 })
const posts = ref([])
const loadCategory = async () => {
    const categoryId = parseInt(route.query.id)
    const data = await categoryApi.getList()
    const found = (data || []).find(c => c.category_id === categoryId)
    if (found) {
        category.value = { ...found, icon: categoryIcons[categoryId % categoryIcons.length] }
    }
}
const loadPosts = async () => {
    const categoryId = route.query.id
    const data = await articleApi.getList({ category_id: categoryId, page: 1 })
    posts.value = data?.list || []
}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
onMounted(async () => {
    await Promise.all([loadCategory(), loadPosts()])
})
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
