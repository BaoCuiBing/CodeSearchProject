<template>
    <div class="search-page">
        <PageNavBar title="搜索" />
        <van-search v-model="keyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        <div class="search-content">
            <div class="section-title">搜索历史</div>
            <div v-if="historyLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
            <van-empty v-else-if="historyError" :description="historyError" />
            <div v-else class="history-list">
                <van-tag v-for="h in history" :key="h.history_id" plain closable @close="removeHistory(h.history_id)" @click="searchKeyword(h.keyword)">{{ h.keyword }}</van-tag>
            </div>
            <div class="section-title">热门搜索</div>
            <div v-if="hotLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
            <van-empty v-else-if="hotError" :description="hotError" />
            <div v-else class="hot-list">
                <van-tag v-for="h in hotSearches" :key="h.keyword" type="primary" plain @click="searchKeyword(h.keyword)">{{ h.keyword }}</van-tag>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { searchApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
const router = useRouter()
const keyword = ref('')
const historyLoading = ref(true)
const historyError = ref('')
const hotLoading = ref(true)
const hotError = ref('')
const history = ref([])
const hotSearches = ref([])
const loadHistory = async () => {
    historyLoading.value = true
    historyError.value = ''
    try {
        const data = await searchApi.getHistory(1, 20)
        history.value = data?.list || []
    } catch (err) {
        historyError.value = err.message || '加载失败'
    } finally {
        historyLoading.value = false
    }
}
const loadHotSearches = async () => {
    hotLoading.value = true
    hotError.value = ''
    try {
        const data = await searchApi.getHot()
        hotSearches.value = data || []
    } catch (err) {
        hotError.value = err.message || '加载失败'
    } finally {
        hotLoading.value = false
    }
}
const loadAll = async () => {
    await Promise.all([loadHistory(), loadHotSearches()])
}
const onSearch = () => { if (keyword.value.trim()) { router.push({ path: '/search-result', query: { keyword: keyword.value } }) } }
const searchKeyword = (kw) => { keyword.value = kw; onSearch() }
const removeHistory = async (historyId) => {
    await searchApi.deleteHistoryItem(historyId)
    history.value = history.value.filter(h => h.history_id !== historyId)
}
onMounted(() => { loadAll() })
</script>

<style scoped>
.search-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.section-loading { display: flex; justify-content: center; align-items: center; padding: 40px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.search-content { padding: 16px; }
.section-title { font-size: 14px; color: #999; margin-bottom: 12px; }
.history-list, .hot-list { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.history-list .van-tag, .hot-list .van-tag { padding: 6px 14px; }
</style>