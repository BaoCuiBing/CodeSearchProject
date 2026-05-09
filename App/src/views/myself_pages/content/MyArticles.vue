<template>
    <div class="my-articles-page">
        <PageNavBar title="我的文章" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
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
        <van-floating-bubble :gap="{x: 30, y: 80}" icon="plus" @click="goToPostEdit" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { articleApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const loading = ref(true)
const error = ref('')
const articles = ref([])
const loadArticles = async () => {
    loading.value = true
    error.value = ''
    try {
        const data = await articleApi.getList({ user_id: getUserId(), type: 'article', page: 1 })
        articles.value = data?.list || []
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const goToPostEdit = () => { router.push('/post-edit') }
onMounted(() => { loadArticles() })
</script>

<style scoped>
.my-articles-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.article-list { padding: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>