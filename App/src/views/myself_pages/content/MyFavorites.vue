<template>
    <div class="my-favorites-page">
        <PageNavBar title="我的收藏" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <div v-else-if="error" class="error-wrap">
            <van-icon name="warn-o" size="48" color="#999" />
            <p class="error-text">{{ error }}</p>
            <van-button type="primary" size="small" @click="loadFavorites">重试</van-button>
        </div>
        <van-tabs v-else v-model:active="activeTab" @change="onTabChange">
            <van-tab title="全部">
                <div class="fav-list">
                    <van-empty v-if="favorites.length === 0" description="暂无收藏" />
                    <PostCard v-for="item in favorites" :key="item.post_id" :title="item.post.title" :summary="item.post.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="fav-meta">
                                <van-tag size="small" :type="item.post.type === 'article' ? 'primary' : 'success'">{{ item.post.type === 'article' ? '文章' : '问题' }}</van-tag>
                                <span>{{ item.created_at }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="文章">
                <div class="fav-list">
                    <van-empty v-if="articleFavorites.length === 0" description="暂无收藏文章" />
                    <PostCard v-for="item in articleFavorites" :key="item.post_id" :title="item.post.title" :summary="item.post.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="fav-meta">
                                <span>{{ item.created_at }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="fav-list">
                    <van-empty v-if="questionFavorites.length === 0" description="暂无收藏问题" />
                    <PostCard v-for="item in questionFavorites" :key="item.post_id" :title="item.post.title" :summary="item.post.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="fav-meta">
                                <span>{{ item.created_at }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
import { favoriteApi } from '@/assets/app_request_api.js'
const router = useRouter()
const activeTab = ref(0)
const loading = ref(true)
const error = ref('')
const favorites = ref([])
const articleFavorites = computed(() => favorites.value.filter(f => f.post.type === 'article'))
const questionFavorites = computed(() => favorites.value.filter(f => f.post.type === 'question'))
const loadFavorites = async () => {
    loading.value = true
    error.value = ''
    try {
        const typeMap = { 0: 'all', 1: 'article', 2: 'question' }
        const data = await favoriteApi.getList({ type: typeMap[activeTab.value] })
        favorites.value = data.list || []
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const onTabChange = () => { loadFavorites() }
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
loadFavorites()
</script>

<style scoped>
.my-favorites-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.fav-list { padding: 12px; }
.fav-meta { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #999; margin-top: 12px; }
</style>