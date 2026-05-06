<template>
    <div class="rankings-page">
        <van-nav-bar title="排行榜" left-arrow @click-left="goBack" fixed placeholder />
        <van-tabs v-model:active="activeTab">
            <van-tab title="文章热榜">
                <div class="ranking-list">
                    <div v-for="(item, index) in articleRanking" :key="item.post_id" class="ranking-item" @click="goToDetail(item.post_id)">
                        <span class="rank-num" :class="{ top: index < 3 }">{{ index + 1 }}</span>
                        <div class="rank-content">
                            <h4>{{ item.title }}</h4>
                            <p>{{ item.author.username }} · 热度 {{ item.hot_score }}</p>
                        </div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="用户活跃">
                <div class="ranking-list">
                    <div v-for="(item, index) in userRanking" :key="item.user_id" class="ranking-item user-rank">
                        <span class="rank-num" :class="{ top: index < 3 }">{{ index + 1 }}</span>
                        <van-image round width="40px" height="40px" :src="item.avatar" />
                        <div class="rank-content">
                            <h4>{{ item.username }}</h4>
                            <p>文章 {{ item.article_count }} · 获赞 {{ item.like_count }}</p>
                        </div>
                    </div>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
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
const goBack = () => router.back()
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.rankings-page { background: #f5f5f5; min-height: 100vh; }
.ranking-list { padding: 8px 0; }
.ranking-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-bottom: 1px solid #f5f5f5; }
.ranking-item.user-rank { align-items: center; }
.rank-num { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; color: #999; }
.rank-num.top { color: #ff6b6b; }
.rank-content { flex: 1; }
.rank-content h4 { margin: 0 0 4px; font-size: 15px; color: #333; }
.rank-content p { margin: 0; font-size: 13px; color: #999; }
</style>
