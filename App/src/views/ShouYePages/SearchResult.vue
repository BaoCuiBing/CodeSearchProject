<template>
    <div class="search-result-page">
        <PageNavBar title="搜索结果" />
        <van-search v-model="keyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        <van-tabs v-model:active="activeTab">
            <van-tab title="综合">
                <div class="result-list">
                    <PostCard v-for="item in results" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="result-meta">
                                <span>{{ item.author.username }}</span>
                                <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                                <span><van-icon name="good-job-o" /> {{ item.like_count }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="文章">
                <div class="result-list">
                    <PostCard v-for="item in articleResults" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="result-meta">
                                <span>{{ item.author.username }}</span>
                                <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                                <span><van-icon name="good-job-o" /> {{ item.like_count }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="result-list">
                    <PostCard v-for="item in questionResults" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="result-meta">
                                <span>{{ item.author.username }}</span>
                                <span><van-icon name="eye-o" /> {{ item.view_count }}</span>
                                <span><van-icon name="good-job-o" /> {{ item.like_count }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
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
const onSearch = () => {}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.search-result-page { background: #f5f5f5; min-height: 100vh; }
.result-list { padding: 12px; }
.result-meta { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
