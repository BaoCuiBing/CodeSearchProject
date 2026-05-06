<template>
    <div class="ranking-page">
        <van-nav-bar title="排行榜" left-arrow @click-left="goBack" fixed placeholder />
        <van-tabs v-model:active="activeTab">
            <van-tab title="文章热榜">
                <div class="ranking-list">
                    <div v-for="(item, index) in articleRanking" :key="item.post_id" class="ranking-item" @click="goToDetail(item.post_id)">
                        <div class="rank-badge" :class="{ top: index < 3 }">{{ index + 1 }}</div>
                        <div class="rank-info">
                            <h4>{{ item.title }}</h4>
                            <p>{{ item.author.username }} · 浏览 {{ item.view_count }} · 点赞 {{ item.like_count }}</p>
                        </div>
                        <div class="hot-score">{{ item.hot_score }}</div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="问题热榜">
                <div class="ranking-list">
                    <div v-for="(item, index) in questionRanking" :key="item.post_id" class="ranking-item" @click="goToDetail(item.post_id)">
                        <div class="rank-badge" :class="{ top: index < 3 }">{{ index + 1 }}</div>
                        <div class="rank-info">
                            <h4>{{ item.title }}</h4>
                            <p>{{ item.author.username }} · 浏览 {{ item.view_count }} · 回答 {{ item.comment_count }}</p>
                        </div>
                        <div class="hot-score">{{ item.hot_score }}</div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="贡献者">
                <div class="ranking-list">
                    <div v-for="(item, index) in contributorRanking" :key="item.user_id" class="ranking-item user-item">
                        <div class="rank-badge" :class="{ top: index < 3 }">{{ index + 1 }}</div>
                        <van-image round width="40px" height="40px" :src="item.avatar" />
                        <div class="rank-info">
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
    { post_id: 1, title: '如何在 Python 中实现多线程并发？', author: { username: '程序员小明' }, view_count: 1205, like_count: 86, hot_score: 8500 },
    { post_id: 2, title: 'Vue3 中的组合式 API 如何使用？', author: { username: '前端小王' }, view_count: 892, like_count: 64, hot_score: 7200 },
    { post_id: 3, title: 'MySQL 索引失效的常见场景', author: { username: 'DBA老张' }, view_count: 2341, like_count: 156, hot_score: 6800 },
    { post_id: 4, title: 'Docker 容器化部署实战', author: { username: '运维小李' }, view_count: 987, like_count: 72, hot_score: 5400 },
    { post_id: 5, title: '深入理解 Vue3 响应式原理', author: { username: '前端小王' }, view_count: 1567, like_count: 98, hot_score: 4900 }
])
const questionRanking = ref([
    { post_id: 6, title: 'Python 多线程与多进程的区别？', author: { username: '新手小白' }, view_count: 456, comment_count: 8, hot_score: 3200 },
    { post_id: 7, title: 'React useEffect 依赖数组问题', author: { username: '前端新人' }, view_count: 234, comment_count: 5, hot_score: 2100 },
    { post_id: 8, title: 'MySQL 性能优化的 10 个技巧', author: { username: '开发者' }, view_count: 678, comment_count: 12, hot_score: 4500 }
])
const contributorRanking = ref([
    { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', article_count: 56, like_count: 2341 },
    { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', article_count: 43, like_count: 1892 },
    { user_id: 3, username: 'DBA老张', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', article_count: 38, like_count: 1567 },
    { user_id: 4, username: '运维小李', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', article_count: 29, like_count: 1234 },
    { user_id: 5, username: 'AI大牛', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', article_count: 25, like_count: 987 }
])
const goBack = () => router.back()
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.ranking-page { background: #f5f5f5; min-height: 100vh; }
.ranking-list { padding: 12px; }
.ranking-item { display: flex; align-items: center; gap: 12px; background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.ranking-item.user-item { align-items: center; }
.rank-badge { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: #999; background: #f5f5f5; border-radius: 50%; flex-shrink: 0; }
.rank-badge.top { color: #fff; background: #ff6b6b; }
.rank-info { flex: 1; }
.rank-info h4 { margin: 0 0 4px; font-size: 15px; color: #333; }
.rank-info p { margin: 0; font-size: 13px; color: #999; }
.hot-score { font-size: 14px; color: #ff6b6b; font-weight: 600; }
</style>
