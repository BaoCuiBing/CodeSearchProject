<template>
    <div class="search-page">
        <PageNavBar title="搜索" />
        <van-search v-model="keyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        <div class="search-content">
            <div class="section-title">搜索历史</div>
            <div class="history-list">
                <van-tag v-for="h in history" :key="h.history_id" plain closable @close="removeHistory(h.history_id)" @click="searchKeyword(h.keyword)">{{ h.keyword }}</van-tag>
            </div>
            <div class="section-title">热门搜索</div>
            <div class="hot-list">
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
const history = ref([])
const hotSearches = ref([])
const loadHistory = async () => {
    const data = await searchApi.getHistory(1, 20)
    history.value = data?.list || []
}
const loadHotSearches = async () => {
    const data = await searchApi.getHot()
    hotSearches.value = data || []
}
const onSearch = () => { if (keyword.value.trim()) { router.push({ path: '/search-result', query: { keyword: keyword.value } }) } }
const searchKeyword = (kw) => { keyword.value = kw; onSearch() }
const removeHistory = async (historyId) => {
    await searchApi.deleteHistoryItem(historyId)
    history.value = history.value.filter(h => h.history_id !== historyId)
}
onMounted(async () => {
    await Promise.all([loadHistory(), loadHotSearches()])
})
</script>

<style scoped>
.search-page { background: #f5f5f5; min-height: 100vh; }
.search-content { padding: 16px; }
.section-title { font-size: 14px; color: #999; margin-bottom: 12px; }
.history-list, .hot-list { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }
</style>
