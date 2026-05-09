<template>
    <div class="tag-articles-page">
        <PageNavBar :title="tagName" />
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
const articles = ref([])
const page = ref(1)
const loadArticles = async () => {
    if (finished.value) return
    loading.value = true
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
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
