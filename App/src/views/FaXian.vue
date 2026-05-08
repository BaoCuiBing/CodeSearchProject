<template>
    <div class="faxian-page">
        <van-nav-bar title="发现" fixed placeholder />
        <div class="search-header">
            <van-search v-model="searchKeyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        </div>
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <div v-else-if="error" class="error-wrap">
            <van-icon name="warn-o" size="48" color="#999" />
            <p class="error-text">{{ error }}</p>
            <van-button type="primary" size="small" @click="loadAll">重试</van-button>
        </div>
        <template v-else>
            <div class="category-section">
                <div class="section-title">分类浏览</div>
                <div class="category-grid">
                    <div v-for="cat in categories" :key="cat.category_id" class="category-item" @click="goToCategory(cat.category_id)">
                        <van-icon :name="cat.icon" size="28" color="#1989fa" />
                        <span>{{ cat.name }}</span>
                    </div>
                </div>
            </div>
            <div class="ranking-section">
                <div class="section-title">
                    <span>排行榜</span>
                    <span class="more" @click="goToRankings">更多</span>
                </div>
                <div class="ranking-tabs">
                    <van-tabs v-model:active="activeRankingTab">
                        <van-tab title="文章热榜">
                            <div class="ranking-list">
                                <van-empty v-if="articleRanking.length === 0" description="暂无数据" />
                                <RankingItem v-for="(item, index) in articleRanking" :key="item.post_id" :index="index" :title="item.title" :subtitle="item.author?.username + ' · 热度 ' + item.hot_score" @click="goToDetail(item.post_id)" />
                            </div>
                        </van-tab>
                        <van-tab title="用户活跃">
                            <div class="ranking-list">
                                <van-empty v-if="userRanking.length === 0" description="暂无数据" />
                                <RankingItem v-for="(item, index) in userRanking" :key="item.user_id" :index="index" :title="item.username" :subtitle="'文章 ' + item.post_count + ' · 评论 ' + item.comment_count">
                                    <template #avatar>
                                        <van-image round width="40px" height="40px" :src="item.avatar" />
                                    </template>
                                </RankingItem>
                            </div>
                        </van-tab>
                    </van-tabs>
                </div>
            </div>
            <div class="recommend-section">
                <div class="section-title">推荐关注</div>
                <div class="user-list">
                    <van-empty v-if="recommendUsers.length === 0" description="暂无推荐" />
                    <UserListItem v-for="user in recommendUsers" :key="user.user_id" :avatar="user.avatar" :username="user.username" :bio="user.bio" :is-followed="user.is_followed" @toggle="followUser(user)" />
                </div>
            </div>
        </template>
        <div class="bottom-spacer"></div>
        <van-floating-bubble :gap="{x: 30, y: 80}" icon="plus" @click="goToPostEdit" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { categoryApi, rankingApi, followApi } from '@/assets/app_request_api.js'
import { setCache, getCache } from '@/assets/local_storage.js'
import RankingItem from '@/components/RankingItem.vue'
import UserListItem from '@/components/UserListItem.vue'
const router = useRouter()
const searchKeyword = ref('')
const activeRankingTab = ref(0)
const loading = ref(true)
const error = ref('')
const categories = ref([])
const articleRanking = ref([])
const userRanking = ref([])
const recommendUsers = ref([])
const categoryIcons = ['cluster-o', 'desktop-o', 'phone-o', 'records', 'setting-o', 'photo-fail', 'chart-trending-o', 'bag-o']
const loadCategories = async () => {
    const cached = getCache('categories')
    if (cached) { categories.value = cached; return }
    const data = await categoryApi.getList()
    categories.value = (data || []).map((cat, idx) => ({ ...cat, icon: categoryIcons[idx % categoryIcons.length] }))
    setCache('categories', categories.value, 30 * 60 * 1000)
}
const loadArticleRanking = async () => {
    const cached = getCache('articleRanking')
    if (cached) { articleRanking.value = cached; return }
    const data = await rankingApi.getList('article_hot', 'week', 5)
    articleRanking.value = data?.list || []
    setCache('articleRanking', data?.list, 5 * 60 * 1000)
}
const loadUserRanking = async () => {
    const cached = getCache('userRanking')
    if (cached) { userRanking.value = cached; return }
    const data = await rankingApi.getList('user_active', 'week', 5)
    userRanking.value = data?.list || []
    setCache('userRanking', data?.list, 5 * 60 * 1000)
}
const loadRecommendUsers = async () => {
    const data = await rankingApi.getList('contributor', 'week', 3)
    recommendUsers.value = data?.list || []
}
const loadAll = async () => {
    loading.value = true
    error.value = ''
    try {
        await Promise.all([loadCategories(), loadArticleRanking(), loadUserRanking(), loadRecommendUsers()])
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const followUser = async (user) => {
    const data = await followApi.toggleFollow(user.user_id)
    user.is_followed = data.is_followed !== undefined ? data.is_followed : !user.is_followed
}
const onSearch = () => {
    if (searchKeyword.value.trim()) {
        router.push({ path: '/search', query: { keyword: searchKeyword.value } })
    }
}
const goToCategory = (catId) => { router.push({ path: '/category', query: { id: catId } }) }
const goToRankings = () => { router.push('/rankings') }
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const goToPostEdit = () => { router.push('/post-edit') }
onMounted(() => { loadAll() })
</script>

<style scoped>
.faxian-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.search-header { background: #fff; padding: 8px 12px; }
.category-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-size: 16px; font-weight: 500; }
.section-title .more { color: #1989fa; font-size: 14px; }
.category-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.category-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.category-item span { font-size: 13px; color: #666; }
.ranking-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.ranking-list { padding: 8px 0; }
.recommend-section { background: #fff; padding: 16px; }
.user-list { display: flex; flex-direction: column; gap: 16px; }
.bottom-spacer { height: 80px; }
</style>