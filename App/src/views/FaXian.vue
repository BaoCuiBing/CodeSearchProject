<template>
    <div class="faxian-page">
        <van-nav-bar title="发现" fixed placeholder />
        <div class="search-header">
            <van-search v-model="searchKeyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        </div>
        <div class="category-section">
            <div class="section-title">
                <span>分类浏览</span>
                <span v-if="!showAllCategories && categories.length > 16" class="more" @click="showAllCategories = true">显示更多</span>
                <span v-else-if="showAllCategories && categories.length > 16" class="more" @click="showAllCategories = false">收起</span>
            </div>
            <div v-if="categoriesLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
            <van-empty v-else-if="categoriesError" :description="categoriesError" />
            <div v-else class="category-grid">
                <div v-for="cat in displayCategories" :key="cat.category_id" class="category-item" @click="goToCategory(cat.category_id)">
                    <img v-if="cat.icon" :src="cat.icon" class="category-icon" />
                    <van-icon v-else name="folder-o" size="28" color="#1989fa" />
                    <span>{{ cat.name }}</span>
                </div>
            </div>
        </div>
        <div class="ranking-section">
            <div class="section-title">
                <span>排行榜</span>
                <span class="more" @click="goToRankings">更多</span>
            </div>
            <div v-if="rankingLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
            <van-empty v-else-if="rankingError" :description="rankingError" />
            <div v-else class="ranking-tabs">
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
                            <RankingItem v-for="(item, index) in userRanking" :key="item.user_id" :index="index" :title="item.username" :subtitle="'文章 ' + item.article_count + ' · 评论 ' + item.comment_count" @click="goToProfile(item.user_id)">
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
            <div v-if="recommendLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
            <van-empty v-else-if="recommendError" :description="recommendError" />
            <div v-else class="user-list">
                <van-empty v-if="recommendUsers.length === 0" description="暂无推荐" />
                <UserListItem v-for="user in recommendUsers" :key="user.user_id" :avatar="user.avatar" :username="user.username" :bio="user.bio" :is-followed="user.is_followed" @toggle="followUser(user)" />
            </div>
        </div>
        <div class="bottom-spacer"></div>
        <van-floating-bubble :gap="{x: 30, y: 80}" icon="plus" @click="goToPostEdit" />
        <van-back-top right="30px" bottom="130px" />
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { categoryApi, rankingApi, followApi } from '@/assets/app_request_api.js'
import { setCache, getCache } from '@/assets/local_storage.js'
import RankingItem from '@/components/RankingItem.vue'
import UserListItem from '@/components/UserListItem.vue'
const router = useRouter()
const searchKeyword = ref('')
const activeRankingTab = ref(0)
const categories = ref([])
const showAllCategories = ref(false)
const displayCategories = computed(() => showAllCategories.value ? categories.value : categories.value.slice(0, 16))
const categoriesLoading = ref(true)
const categoriesError = ref('')
const rankingLoading = ref(true)
const rankingError = ref('')
const recommendLoading = ref(true)
const recommendError = ref('')
const articleRanking = ref([])
const userRanking = ref([])
const recommendUsers = ref([])
const loadCategories = async () => {
    categoriesLoading.value = true
    categoriesError.value = ''
    try {
        const cached = getCache('categories')
        if (cached) { categories.value = cached; return }
        const data = await categoryApi.getList()
        categories.value = data || []
        setCache('categories', categories.value, 30 * 60 * 1000)
    } catch (err) {
        categoriesError.value = err.message || '加载失败'
    } finally {
        categoriesLoading.value = false
    }
}
const loadArticleRanking = async () => {
    rankingLoading.value = true
    rankingError.value = ''
    try {
        const cached = getCache('articleRanking')
        if (cached) { articleRanking.value = cached; return }
        const data = await rankingApi.getList('article_hot', 'week', 5)
        articleRanking.value = data?.list || []
        setCache('articleRanking', data?.list, 5 * 60 * 1000)
    } catch (err) {
        rankingError.value = err.message || '加载失败'
    } finally {
        rankingLoading.value = false
    }
}
const loadUserRanking = async () => {
    try {
        const cached = getCache('userRanking')
        if (cached) { userRanking.value = cached; return }
        const data = await rankingApi.getList('user_active', 'week', 5)
        userRanking.value = data?.list || []
        setCache('userRanking', data?.list, 5 * 60 * 1000)
    } catch (err) {
        rankingError.value = err.message || '加载失败'
    }
}
const loadRecommendUsers = async () => {
    recommendLoading.value = true
    recommendError.value = ''
    try {
        const data = await rankingApi.getList('contributor', 'week', 3)
        recommendUsers.value = data?.list || []
    } catch (err) {
        recommendError.value = err.message || '加载失败'
    } finally {
        recommendLoading.value = false
    }
}
const loadAll = async () => {
    await Promise.all([loadCategories(), loadArticleRanking(), loadUserRanking(), loadRecommendUsers()])
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
const goToProfile = (userId) => { router.push({ path: '/profile', query: { id: userId } }) }
const goToPostEdit = () => { router.push('/post-edit') }
onMounted(() => { loadAll() })
</script>

<style scoped>
.faxian-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.section-loading { display: flex; justify-content: center; align-items: center; padding: 40px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.search-header { background: #fff; padding: 8px 12px; }
.category-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-size: 16px; font-weight: 500; }
.section-title .more { color: #1989fa; font-size: 14px; cursor: pointer; }
.category-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.category-item { display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer; }
.category-icon { width: 28px; height: 28px; object-fit: contain; }
.category-item span { font-size: 13px; color: #666; max-width: 75px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ranking-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.ranking-list { padding: 8px 0; }
.recommend-section { background: #fff; padding: 16px; }
.user-list { display: flex; flex-direction: column; gap: 16px; }
.bottom-spacer { height: 80px; }
</style>