<template>
    <div class="rankings-page">
        <PageNavBar title="排行榜" />
        <van-tabs v-model:active="activeTab">
            <van-tab title="文章热榜">
                <div class="ranking-list">
                    <RankingItem v-for="(item, index) in articleRanking" :key="item.post_id" :index="index" :title="item.title" :subtitle="item.author.username + ' · 热度 ' + item.hot_score" @click="goToDetail(item.post_id)" />
                </div>
            </van-tab>
            <van-tab title="用户活跃">
                <div class="ranking-list">
                    <RankingItem v-for="(item, index) in userRanking" :key="item.user_id" :index="index" :title="item.username" :subtitle="'文章 ' + item.article_count + ' · 获赞 ' + item.like_count" @click="goToDetail(item.user_id)">
                        <template #avatar>
                            <van-image round width="40px" height="40px" :src="item.avatar" />
                        </template>
                    </RankingItem>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import RankingItem from '@/components/RankingItem.vue'
const router = useRouter()
const activeTab = ref(0)
const articleRanking = ref([
    { post_id: 1, title: '如何在 Python 中实现多线程并发？', author: { username: '程序员小明' }, hot_score: 8500 },
    { post_id: 2, title: 'Vue3 中的组合式 API 如何使用？', author: { username: '前端小王' }, hot_score: 7200 }
])
const userRanking = ref([
    { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', article_count: 56, like_count: 2341 },
    { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', article_count: 43, like_count: 1892 }
])
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.rankings-page { background: #f5f5f5; min-height: 100vh; }
.ranking-list { padding: 8px 0; }
</style>
