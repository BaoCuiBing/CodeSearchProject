<template>
    <div class="search-result-page">
        <PageNavBar title="搜索结果" />
        <van-search v-model="keyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        <van-tabs v-model:active="activeTab" @change="onTabChange">
            <van-tab title="综合">
                <div class="result-list">
                    <van-empty v-if="results.length === 0" description="暂无搜索结果" />
                    <PostCard v-for="item in results" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="result-meta">
                                <span>{{ item.author?.username || '' }}</span>
                                <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                                <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ item.like_count }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="文章">
                <div class="result-list">
                    <van-empty v-if="articleResults.length === 0" description="暂无文章" />
                    <PostCard v-for="item in articleResults" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="result-meta">
                                <span>{{ item.author?.username || '' }}</span>
                                <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                                <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ item.like_count }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="result-list">
                    <van-empty v-if="questionResults.length === 0" description="暂无问题" />
                    <PostCard v-for="item in questionResults" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="result-meta">
                                <span>{{ item.author?.username || '' }}</span>
                                <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                                <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ item.like_count }}</span>
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
import { useRouter, useRoute } from 'vue-router'
import { searchApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const route = useRoute()
const keyword = ref(route.query.keyword || '')
const activeTab = ref(0)
const results = ref([])
const articleResults = ref([])
const questionResults = ref([])
const loadResults = async () => {
    const data = await searchApi.search(keyword.value, { type: 'all' })
    results.value = data?.list || []
}
const loadArticleResults = async () => {
    const data = await searchApi.search(keyword.value, { type: 'article' })
    articleResults.value = data?.list || []
}
const loadQuestionResults = async () => {
    const data = await searchApi.search(keyword.value, { type: 'question' })
    questionResults.value = data?.list || []
}
const onTabChange = async (index) => {
    if (index === 0 && results.value.length === 0) { await loadResults() }
    if (index === 1 && articleResults.value.length === 0) { await loadArticleResults() }
    if (index === 2 && questionResults.value.length === 0) { await loadQuestionResults() }
}
const onSearch = () => {
    if (keyword.value.trim()) {
        router.push({ path: '/search-result', query: { keyword: keyword.value } })
        loadResults()
    }
}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
onMounted(() => { loadResults() })
</script>

<style scoped>
.search-result-page { background: #f5f5f5; min-height: 100vh; }
.result-list { padding: 12px; }
.result-meta { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
