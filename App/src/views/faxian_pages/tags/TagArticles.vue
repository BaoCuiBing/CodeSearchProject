<template>
    <div class="tag-articles-page">
        <PageNavBar :title="tagName" />
        <van-empty v-if="error" :description="error" />
        <template v-else>
            <van-empty v-if="!loading && articles.length === 0" description="暂无文章" />
            <div v-else class="article-list">
                <PostCardList :loading="loading" :finished="finished" :posts="articles" @load="loadArticles" @click="goToDetail">
                <template #footer="{ post }">
                    <div class="post-stats">
                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                        <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ post.like_count }}</span>
                    </div>
                </template>
            </PostCardList>
            </div>
        </template>
        <van-back-top right="30px" bottom="80px" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { tagApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCardList from '@/components/PostCardList.vue'
const router = useRouter()
const route = useRoute()
const tagName = ref(route.query.name || '标签')
const loading = ref(false)
const finished = ref(false)
const error = ref('')
const articles = ref([])
const page = ref(1)
const loadArticles = async () => {
    if (loading.value || finished.value) return
    loading.value = true
    error.value = ''
    try {
        const tagId = route.query.id
        const data = await tagApi.getArticles(tagId, { page: page.value })
        const list = data?.list || []
        articles.value = [...articles.value, ...list]
        page.value++
        if (list.length === 0) { finished.value = true }
    } catch (err) {
        error.value = err.message || '加载失败'
        finished.value = true
    } finally {
        loading.value = false
    }
}
const goToDetail = (post) => { router.push({ path: '/article', query: { id: post.post_id } }) }
onMounted(() => { loadArticles() })
</script>

<style scoped>
.tag-articles-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.article-list { padding: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
