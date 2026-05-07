<template>
    <div class="favorites-page">
        <PageNavBar title="我的收藏" />
        <van-tabs v-model:active="activeTab" @change="onTabChange">
            <van-tab title="文章">
                <div class="article-list">
                    <van-empty v-if="articles.length === 0" description="暂无收藏文章" />
                    <PostCard v-for="item in articles" :key="item.favorite_id" :title="item.post?.title || ''" :summary="item.post?.summary || ''" @click="goToDetail(item.post?.post_id)">
                        <template #footer>
                            <div class="post-stats">
                                <span><van-icon name="eye-o" /> {{ item.post?.view_count || 0 }}</span>
                                <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ item.post?.like_count || 0 }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="question-list">
                    <van-empty v-if="questions.length === 0" description="暂无收藏问题" />
                    <PostCard v-for="item in questions" :key="item.favorite_id" :title="item.post?.title || ''" :summary="item.post?.summary || ''" @click="goToDetail(item.post?.post_id)">
                        <template #footer>
                            <div class="question-stats">
                                <span><van-icon name="eye-o" /> {{ item.post?.view_count || 0 }}</span>
                                <span><van-icon name="chat-o" /> {{ item.post?.comment_count || 0 }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { favoriteApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const activeTab = ref(0)
const articles = ref([])
const questions = ref([])
const loadArticles = async () => {
    const data = await favoriteApi.getList({ type: 'article', page: 1 })
    articles.value = data?.list || []
}
const loadQuestions = async () => {
    const data = await favoriteApi.getList({ type: 'question', page: 1 })
    questions.value = data?.list || []
}
const onTabChange = async (index) => {
    if (index === 0 && articles.value.length === 0) { await loadArticles() }
    if (index === 1 && questions.value.length === 0) { await loadQuestions() }
}
const goToDetail = (postId) => { if (postId) { router.push({ path: '/article', query: { id: postId } }) } }
onMounted(() => { loadArticles() })
</script>

<style scoped>
.favorites-page { background: #f5f5f5; min-height: 100vh; }
.article-list, .question-list { padding: 12px; }
.post-stats, .question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
