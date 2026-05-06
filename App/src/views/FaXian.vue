<template>
    <div class="faxian-page">
        <van-nav-bar title="发现" fixed placeholder />
        <div class="search-header">
            <van-search v-model="searchKeyword" placeholder="搜索技术问题、代码..." @search="onSearch" />
        </div>
        <div class="category-section">
            <div class="section-title">分类浏览</div>
            <div class="category-grid">
                <div v-for="cat in categories" :key="cat.category_id" class="category-item" @click="goToCategory(cat.category_id)">
                    <van-icon :name="cat.icon" size="28" color="#1989fa" />
                    <span>{{ cat.name }}</span>
                </div>
            </div>
        </div>
        <div class="ranking-section">
            <div class="section-title">
                <span>排行榜</span>
                <span class="more" @click="goToRankings">更多</span>
            </div>
            <div class="ranking-tabs">
                <van-tabs v-model:active="activeRankingTab">
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
        </div>
        <div class="recommend-section">
            <div class="section-title">推荐关注</div>
            <div class="user-list">
                <div v-for="user in recommendUsers" :key="user.user_id" class="user-card">
                    <van-image round width="48px" height="48px" :src="user.avatar" />
                    <div class="user-info">
                        <span class="user-name">{{ user.username }}</span>
                        <span class="user-bio">{{ user.bio }}</span>
                    </div>
                    <van-button size="small" :type="user.is_followed ? 'default' : 'primary'" @click="followUser(user)">{{ user.is_followed ? '已关注' : '关注' }}</van-button>
                </div>
            </div>
        </div>
        <div class="bottom-spacer"></div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const searchKeyword = ref('')
const activeRankingTab = ref(0)
const categories = ref([
    { category_id: 1, name: '后端开发', icon: 'cluster-o' },
    { category_id: 2, name: '前端开发', icon: 'desktop-o' },
    { category_id: 3, name: '移动开发', icon: 'phone-o' },
    { category_id: 4, name: '数据库', icon: 'records' },
    { category_id: 5, name: '运维部署', icon: 'setting-o' },
    { category_id: 6, name: '人工智能', icon: 'photo-fail' },
    { category_id: 7, name: '算法', icon: 'chart-trending-o' },
    { category_id: 8, name: '工具', icon: 'bag-o' }
])
const articleRanking = ref([
    { post_id: 1, type: 'article', title: '如何在 Python 中实现多线程并发？', author: { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 1, name: '后端开发' }, view_count: 1205, like_count: 86, comment_count: 23, favorite_count: 45, created_at: '2025-05-05 10:30:00', hot_score: 8500 },
    { post_id: 2, type: 'article', title: 'Vue3 中的组合式 API 如何使用？', author: { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 2, name: '前端开发' }, view_count: 892, like_count: 64, comment_count: 15, favorite_count: 32, created_at: '2025-05-04 14:20:00', hot_score: 7200 },
    { post_id: 3, type: 'article', title: 'MySQL 索引失效的常见场景', author: { user_id: 3, username: 'DBA老张', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 4, name: '数据库' }, view_count: 2341, like_count: 156, comment_count: 42, favorite_count: 89, created_at: '2025-05-03 09:15:00', hot_score: 6800 },
    { post_id: 4, type: 'article', title: 'Docker 容器化部署实战', author: { user_id: 4, username: '运维小李', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 5, name: '运维部署' }, view_count: 987, like_count: 72, comment_count: 18, favorite_count: 34, created_at: '2025-05-01 11:20:00', hot_score: 5400 },
    { post_id: 5, type: 'article', title: '深入理解 Vue3 响应式原理', author: { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 2, name: '前端开发' }, view_count: 1567, like_count: 98, comment_count: 31, favorite_count: 56, created_at: '2025-05-02 16:45:00', hot_score: 4900 }
])
const userRanking = ref([
    { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '热爱编程，乐于分享', article_count: 56, question_count: 12, follower_count: 2341, following_count: 128, like_count: 2341, view_count: 15678, is_followed: false },
    { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '专注前端技术', article_count: 43, question_count: 8, follower_count: 1892, following_count: 95, like_count: 1892, view_count: 12345, is_followed: true },
    { user_id: 3, username: 'DBA老张', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '数据库专家', article_count: 38, question_count: 5, follower_count: 1567, following_count: 67, like_count: 1567, view_count: 9876, is_followed: false },
    { user_id: 4, username: '运维小李', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'DevOps实践者', article_count: 29, question_count: 15, follower_count: 1234, following_count: 89, like_count: 1234, view_count: 8765, is_followed: false },
    { user_id: 5, username: 'AI大牛', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '人工智能研究者', article_count: 25, question_count: 20, follower_count: 987, following_count: 45, like_count: 987, view_count: 6543, is_followed: true }
])
const recommendUsers = ref([
    { user_id: 6, username: '全栈工程师', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '热爱技术，分享经验', article_count: 67, question_count: 23, follower_count: 3456, following_count: 156, like_count: 3456, view_count: 23456, is_followed: false },
    { user_id: 7, username: '数据分析师', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '专注数据分析与可视化', article_count: 45, question_count: 18, follower_count: 2345, following_count: 98, like_count: 2345, view_count: 15678, is_followed: false },
    { user_id: 8, username: '安全专家', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '网络安全从业者', article_count: 34, question_count: 12, follower_count: 1890, following_count: 76, like_count: 1890, view_count: 12345, is_followed: true }
])
const onSearch = () => {
    if (searchKeyword.value.trim()) {
        router.push({ path: '/search', query: { keyword: searchKeyword.value } })
    }
}
const goToCategory = (catId) => { router.push({ path: '/category', query: { id: catId } }) }
const goToRankings = () => { router.push('/rankings') }
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const followUser = (user) => { user.is_followed = !user.is_followed }
</script>

<style scoped>
.faxian-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.search-header { background: #fff; padding: 8px 12px; }
.category-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-size: 16px; font-weight: 500; }
.section-title .more { color: #1989fa; font-size: 14px; }
.category-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.category-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.category-item span { font-size: 13px; color: #666; }
.ranking-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.ranking-list { padding: 8px 0; }
.ranking-item { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid #f5f5f5; }
.ranking-item.user-rank { align-items: center; }
.rank-num { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; color: #999; }
.rank-num.top { color: #ff6b6b; }
.rank-content { flex: 1; }
.rank-content h4 { margin: 0 0 4px; font-size: 15px; color: #333; }
.rank-content p { margin: 0; font-size: 13px; color: #999; }
.recommend-section { background: #fff; padding: 16px; }
.user-list { display: flex; flex-direction: column; gap: 16px; }
.user-card { display: flex; align-items: center; gap: 12px; }
.user-info { flex: 1; display: flex; flex-direction: column; }
.user-name { font-size: 15px; color: #333; font-weight: 500; }
.user-bio { font-size: 13px; color: #999; }
.bottom-spacer { height: 80px; }
</style>
