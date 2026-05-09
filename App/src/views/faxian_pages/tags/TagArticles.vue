<template>
    <div class="tag-articles-page">
        <PageNavBar :title="tagName" />
        <div v-if="error" class="error-wrap">
            <van-icon name="warn-o" size="48" color="#999" />
            <p class="error-text">{{ error }}</p>
            <van-button type="primary" size="small" @click="loadArticles">重试</van-button>
        </div>
        <PostCardList v-else :loading="loading" :finished="finished" :immediate-check="false" :posts="articles" @load="loadArticles" @click="goToDetail">
            <template #footer="{ post }">
                <div class="post-stats">
                    <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                    <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ post.like_count }}</span>
                </div>
            </template>
        </PostCardList>
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
const pageSize = 10
const loadArticles = async () => {
    if (loading.value) return
    loading.value = true
    error.value = ''
    try {
        const tagId = route.query.id
        const data = await tagApi.getArticles(tagId, { page: page.value })
        const list = data?.list || []
        if (list.length === 0) {
            finished.value = true
        } else {
            articles.value = [...articles.value, ...list]
            page.value++
        }
    } catch (err) {
        error.value = err.message || '加载失败'
        finished.value = true
    } finally {
        loading.value = false
    }
}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
onMounted(() => { loadArticles() })
</script>

<style scoped>
.tag-articles-page { background: #f5f5f5; min-height: 100vh; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>