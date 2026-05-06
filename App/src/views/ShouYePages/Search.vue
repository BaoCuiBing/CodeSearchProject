<template>
    <div class="search-page">
        <van-nav-bar title="搜索" left-arrow @click-left="goBack" fixed placeholder />
        <van-search v-model="keyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        <div class="search-content">
            <div class="section-title">搜索历史</div>
            <div class="history-list">
                <van-tag v-for="h in history" :key="h" plain closable @close="removeHistory(h)" @click="searchKeyword(h)">{{ h }}</van-tag>
            </div>
            <div class="section-title">热门搜索</div>
            <div class="hot-list">
                <van-tag v-for="h in hotSearches" :key="h" type="primary" plain @click="searchKeyword(h)">{{ h }}</van-tag>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const keyword = ref('')
const history = ref(['Python多线程', 'Vue3响应式', 'MySQL索引'])
const hotSearches = ref(['Python', 'Vue3', 'React', 'Docker', 'MySQL', 'Redis'])
const goBack = () => router.back()
const onSearch = () => { if (keyword.value.trim()) { router.push({ path: '/search-result', query: { keyword: keyword.value } }) } }
const searchKeyword = (kw) => { keyword.value = kw; onSearch() }
const removeHistory = (kw) => { history.value = history.value.filter(h => h !== kw) }
</script>

<style scoped>
.search-page { background: #f5f5f5; min-height: 100vh; }
.search-content { padding: 16px; }
.section-title { font-size: 14px; color: #999; margin-bottom: 12px; }
.history-list, .hot-list { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }
</style>
