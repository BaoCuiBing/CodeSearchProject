<template>
    <div class="search-result-page">
        <van-nav-bar title="搜索结果" left-arrow @click-left="goBack" fixed placeholder />
        <van-search v-model="keyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        <van-tabs v-model:active="activeTab">
            <van-tab title="综合">
                <div class="result-list">
                    <div v-for="item in results" :key="item.post_id" class="result-item" @click="goToDetail(item.post_id)">
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.summary }}</p>
                        <div class="result-meta">
                            <span>{{ item.author.username }}</span>
                            <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                            <span><van-icon name="good-job-o" /> {{ item.like_count }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="文章">
                <div class="result-list">
                    <div v-for="item in articleResults" :key="item.post_id" class="result-item" @click="goToDetail(item.post_id)">
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.summary }}</p>
                        <div class="result-meta">
                            <span>{{ item.author.username }}</span>
                            <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                            <span><van-icon name="good-job-o" /> {{ item.like_count }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="result-list">
                    <div v-for="item in questionResults" :key="item.post_id" class="result-item" @click="goToDetail(item.post_id)">
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.summary }}</p>
                        <div class="result-meta">
                            <span>{{ item.author.username }}</span>
                            <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                            <span><van-icon name="good-job-o" /> {{ item.like_count }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
const keyword = ref(route.query.keyword || '')
const activeTab = ref(0)
const results = ref([
    { post_id: 1, title: '如何在 Python 中实现多线程并发？', summary: '本文详细介绍了 Python 中多线程的使用方法...', author: { username: '程序员小明' }, view_count: 1205, like_count: 86 },
    { post_id: 2, title: 'Vue3 中的组合式 API 如何使用？', summary: '组合式 API 是 Vue3 的重要特性...', author: { username: '前端小王' }, view_count: 892, like_count: 64 },
    { post_id: 3, title: 'MySQL 索引失效的常见场景', summary: '总结 MySQL 索引失效的 10 种常见场景...', author: { username: 'DBA老张' }, view_count: 2341, like_count: 156 }
])
const articleResults = ref([
    { post_id: 2, title: 'Vue3 中的组合式 API 如何使用？', summary: '组合式 API 是 Vue3 的重要特性...', author: { username: '前端小王' }, view_count: 892, like_count: 64 }
])
const questionResults = ref([
    { post_id: 1, title: '如何在 Python 中实现多线程并发？', summary: '本文详细介绍了 Python 中多线程的使用方法...', author: { username: '程序员小明' }, view_count: 1205, like_count: 86 }
])
const goBack = () => router.back()
const onSearch = () => {}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.search-result-page { background: #f5f5f5; min-height: 100vh; }
.result-list { padding: 12px; }
.result-item { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.result-item h4 { margin: 0 0 8px; font-size: 16px; color: #333; }
.result-item p { margin: 0 0 12px; font-size: 14px; color: #666; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.result-meta { display: flex; gap: 16px; font-size: 13px; color: #999; }
</style>
