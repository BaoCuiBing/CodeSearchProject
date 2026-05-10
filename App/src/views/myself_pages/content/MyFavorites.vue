<template>
    <div class="my-favorites-page">
        <PageNavBar title="我的收藏" />
        <div v-if="initialLoading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <van-tabs v-else v-model:active="activeTab" @change="onTabChange">
            <van-tab title="全部">
                <div v-if="tabLoading" class="tab-loading"><van-loading size="20px" /></div>
                <div v-else class="fav-list">
                    <van-empty v-if="favorites.length === 0" description="暂无收藏" />
                    <PostCardList v-else :loading="loading" :finished="finished" :posts="flatFavorites" @load="loadFavorites" @click="goToDetail">
                        <template #footer="{ post }">
                            <div class="fav-meta">
                                <van-tag size="small" :type="post.type === 'article' ? 'primary' : 'success'">{{ post.type === 'article' ? '文章' : '问题' }}</van-tag>
                                <span>{{ post.created_at }}</span>
                            </div>
                        </template>
                    </PostCardList>
                </div>
            </van-tab>
            <van-tab title="文章">
                <div v-if="tabLoading" class="tab-loading"><van-loading size="20px" /></div>
                <div v-else class="fav-list">
                    <van-empty v-if="articleFavorites.length === 0" description="暂无收藏文章" />
                    <PostCardList v-else :loading="loading" :finished="finished" :posts="flatArticleFavorites" @load="loadFavorites" @click="goToDetail">
                        <template #footer="{ post }">
                            <div class="fav-meta">
                                <span>{{ post.created_at }}</span>
                            </div>
                        </template>
                    </PostCardList>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div v-if="tabLoading" class="tab-loading"><van-loading size="20px" /></div>
                <div v-else class="fav-list">
                    <van-empty v-if="questionFavorites.length === 0" description="暂无收藏问题" />
                    <PostCardList v-else :loading="loading" :finished="finished" :posts="flatQuestionFavorites" @load="loadFavorites" @click="goToDetail">
                        <template #footer="{ post }">
                            <div class="fav-meta">
                                <span>{{ post.created_at }}</span>
                            </div>
                        </template>
                    </PostCardList>
                </div>
            </van-tab>
        </van-tabs>
        <van-back-top right="30px" bottom="80px" />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCardList from '@/components/PostCardList.vue'
import { favoriteApi } from '@/assets/app_request_api.js'
const router = useRouter()
const activeTab = ref(0)
const initialLoading = ref(true)
const tabLoading = ref(false)
const error = ref('')
const favorites = ref([])
const articleFavorites = computed(() => favorites.value.filter(f => f.post.type === 'article'))
const questionFavorites = computed(() => favorites.value.filter(f => f.post.type === 'question'))
const flatFavorites = computed(() => favorites.value.map(f => ({ ...f.post, created_at: f.created_at })))
const flatArticleFavorites = computed(() => articleFavorites.value.map(f => ({ ...f.post, created_at: f.created_at })))
const flatQuestionFavorites = computed(() => questionFavorites.value.map(f => ({ ...f.post, created_at: f.created_at })))
const loading = ref(false)
const finished = ref(false)
const page = ref(1)
const loadFavorites = async (isInitial = false) => {
    if (loading.value || finished.value) return
    if (isInitial) { initialLoading.value = true }
    else { tabLoading.value = true }
    loading.value = true
    error.value = ''
    try {
        const typeMap = { 0: 'all', 1: 'article', 2: 'question' }
        const data = await favoriteApi.getList({ type: typeMap[activeTab.value], page: page.value })
        const list = data?.list || []
        if (list.length === 0) { finished.value = true }
        else { favorites.value = [...favorites.value, ...list]; page.value++ }
    } catch (err) {
        error.value = err.message || '加载失败'
        finished.value = true
    } finally {
        initialLoading.value = false
        tabLoading.value = false
        loading.value = false
    }
}
const onTabChange = () => { favorites.value = []; page.value = 1; finished.value = false; loadFavorites(false) }
const goToDetail = (post) => { router.push({ path: '/article', query: { id: post.post_id } }) }
loadFavorites(true)
</script>

<style scoped>
.my-favorites-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.fav-list { padding: 12px; }
.tab-loading { display: flex; justify-content: center; padding: 40px 0; }
.fav-meta { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #999; margin-top: 12px; }
</style>