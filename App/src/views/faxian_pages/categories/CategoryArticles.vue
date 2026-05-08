<template>
    <div class="category-articles-page">
        <PageNavBar :title="categoryName" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <div v-else-if="error" class="error-wrap">
            <van-icon name="warn-o" size="48" color="#999" />
            <p class="error-text">{{ error }}</p>
            <van-button type="primary" size="small" @click="loadArticles">重试</van-button>
        </div>
        <div v-else class="article-list">
            <van-empty v-if="articles.length === 0" description="暂无文章" />
            <PostCard v-for="post in articles" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
                <template #footer>
                    <div class="post-stats">
                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                        <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ post.like_count }}</span>
                    </div>
                </template>
            </PostCard>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { articleApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const route = useRoute()
const categoryName = ref(route.query.name || '分类')
const loading = ref(true)
const error = ref('')
const articles = ref([])
const loadArticles = async () => {
    loading.value = true
    error.value = ''
    try {
        const categoryId = route.query.id
        const data = await articleApi.getList({ category_id: categoryId, page: 1 })
        articles.value = data?.list || []
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
onMounted(() => { loadArticles() })
</script>

<style scoped>
.category-articles-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.article-list { padding: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>