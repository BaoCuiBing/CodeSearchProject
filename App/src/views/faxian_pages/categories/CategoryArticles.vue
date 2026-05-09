<template>
    <div class="category-articles-page">
        <PageNavBar :title="categoryName" />
        <div v-if="loading && articles.length === 0" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <div v-else class="article-list">
            <van-empty v-if="!loading && articles.length === 0" description="暂无文章" />
            <PostCardList v-else :loading="loading" :finished="finished" :posts="articles" @load="loadArticles" @click="goToDetail">
                <template #footer="{ post }">
                    <div class="post-stats">
                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                        <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ post.like_count }}</span>
                    </div>
                </template>
            </PostCardList>
        </div>
        <van-back-top right="30px" bottom="80px" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { articleApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCardList from '@/components/PostCardList.vue'
const router = useRouter()
const route = useRoute()
const categoryName = ref(route.query.name || '分类')
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
        const categoryId = route.query.id
        const data = await articleApi.getList({ category_id: categoryId, page: page.value })
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
const goToDetail = (post) => { router.push({ path: '/article', query: { id: post.post_id } }) }
onMounted(() => { loadArticles() })
</script>

<style scoped>
.category-articles-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.article-list { padding: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>