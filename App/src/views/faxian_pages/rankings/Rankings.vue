<template>
    <div class="rankings-page">
        <PageNavBar title="排行榜" />
        <van-tabs v-model:active="activeTab" @change="onTabChange">
            <van-tab title="文章热榜">
                <div v-if="articleLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                <van-empty v-else-if="articleError" :description="articleError" />
                <div v-else class="ranking-list">
                    <van-empty v-if="articleRanking.length === 0" description="暂无数据" />
                    <RankingItem v-for="(item, index) in articleRanking" :key="item.post_id" :index="index" :title="item.title" :subtitle="item.author?.username + ' · 热度 ' + item.hot_score" @click="goToDetail(item.post_id)" />
                </div>
            </van-tab>
            <van-tab title="用户活跃">
                <div v-if="userLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                <van-empty v-else-if="userError" :description="userError" />
                <div v-else class="ranking-list">
                    <van-empty v-if="userRanking.length === 0" description="暂无数据" />
                    <RankingItem v-for="(item, index) in userRanking" :key="item.user_id" :index="index" :title="item.username" :subtitle="'文章 ' + (item.article_count || 0) + ' · 获赞 ' + (item.like_count || 0)" @click="goToProfile(item.user_id)">
                        <template #avatar>
                            <van-image round width="40px" height="40px" :src="item.avatar || ''" />
                        </template>
                    </RankingItem>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { rankingApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
import RankingItem from '@/components/RankingItem.vue'
const router = useRouter()
const activeTab = ref(0)
const articleLoading = ref(true)
const articleError = ref('')
const userLoading = ref(false)
const userError = ref('')
const articleRanking = ref([])
const userRanking = ref([])
const loadArticleRanking = async () => {
    articleLoading.value = true
    articleError.value = ''
    try {
        const data = await rankingApi.getList('article_hot', 'week', 20)
        articleRanking.value = data?.list || []
    } catch (err) {
        articleError.value = err.message || '加载失败'
    } finally {
        articleLoading.value = false
    }
}
const loadUserRanking = async () => {
    userLoading.value = true
    userError.value = ''
    try {
        const data = await rankingApi.getList('user_active', 'week', 20)
        userRanking.value = data?.list || []
    } catch (err) {
        userError.value = err.message || '加载失败'
    } finally {
        userLoading.value = false
    }
}
const onTabChange = async (index) => {
    if (index === 0 && articleRanking.value.length === 0) { await loadArticleRanking() }
    if (index === 1 && userRanking.value.length === 0) { await loadUserRanking() }
}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const goToProfile = (userId) => { router.push({ path: '/profile', query: { id: userId } }) }
onMounted(() => { loadArticleRanking() })
</script>

<style scoped>
.rankings-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.section-loading { display: flex; justify-content: center; align-items: center; padding: 40px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.ranking-list { padding: 12px; }
</style>