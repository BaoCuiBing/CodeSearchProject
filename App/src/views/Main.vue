<template>
    <div class="shouye-page">
        <van-nav-bar title="首页" fixed placeholder />
        <div class="search-header">
            <van-search v-model="searchKeyword" placeholder="搜索技术问题、代码..." @search="onSearch" @focus="onSearchFocus" />
        </div>
        <div class="banner-section">
            <van-swipe class="banner-swipe" :autoplay="3000" indicator-color="white">
                <van-swipe-item v-for="(item, index) in banners" :key="index" @click="goToSearchFromBanner(item)">
                    <div class="banner-item" :style="{ background: item.bg }">
                        <div class="banner-content">
                            <h3>{{ item.title }}</h3>
                            <p>{{ item.subtitle }}</p>
                        </div>
                    </div>
                </van-swipe-item>
            </van-swipe>
        </div>
        <div class="hot-tags">
            <div class="section-title">
                <span>热门标签</span>
                <span class="more" @click="goToTags">更多</span>
            </div>
            <div class="tag-list">
                <van-tag v-for="tag in hotTags" :key="tag.tag_id" :color="tag.color" class="hot-tag" @click="goToTag(tag.tag_id)">{{ tag.name }}</van-tag>
            </div>
        </div>
        <div class="content-tabs">
            <van-tabs v-model:active="activeTab" sticky offset-top="0">
                <van-tab title="推荐">
                    <div class="post-list">
                        <div v-for="post in recommendPosts" :key="post.post_id" class="post-card" @click="goToDetail(post.post_id)">
                            <div class="post-header">
                                <van-image round width="32px" height="32px" :src="post.author.avatar" />
                                <span class="author-name">{{ post.author.username }}</span>
                                <span class="post-time">{{ post.created_at }}</span>
                            </div>
                            <h4 class="post-title">{{ post.title }}</h4>
                            <p class="post-summary">{{ post.summary }}</p>
                            <div class="post-tags">
                                <van-tag v-for="tag in post.tags" :key="tag.tag_id" size="small" type="primary" plain>{{ tag.name }}</van-tag>
                            </div>
                            <div class="post-stats">
                                <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                                <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                                <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                            </div>
                        </div>
                    </div>
                </van-tab>
                <van-tab title="文章">
                    <div class="post-list">
                        <div v-for="post in articlePosts" :key="post.post_id" class="post-card" @click="goToDetail(post.post_id)">
                            <div class="post-header">
                                <van-image round width="32px" height="32px" :src="post.author.avatar" />
                                <span class="author-name">{{ post.author.username }}</span>
                                <span class="post-time">{{ post.created_at }}</span>
                            </div>
                            <h4 class="post-title">{{ post.title }}</h4>
                            <p class="post-summary">{{ post.summary }}</p>
                            <div class="post-tags">
                                <van-tag v-for="tag in post.tags" :key="tag.tag_id" size="small" type="primary" plain>{{ tag.name }}</van-tag>
                            </div>
                            <div class="post-stats">
                                <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                                <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                                <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                            </div>
                        </div>
                    </div>
                </van-tab>
                <van-tab title="问题">
                    <div class="post-list">
                        <div v-for="post in questionPosts" :key="post.post_id" class="post-card" @click="goToDetail(post.post_id)">
                            <div class="post-header">
                                <van-image round width="32px" height="32px" :src="post.author.avatar" />
                                <span class="author-name">{{ post.author.username }}</span>
                                <span class="post-time">{{ post.created_at }}</span>
                            </div>
                            <h4 class="post-title">{{ post.title }}</h4>
                            <p class="post-summary">{{ post.summary }}</p>
                            <div class="post-tags">
                                <van-tag v-for="tag in post.tags" :key="tag.tag_id" size="small" type="primary" plain>{{ tag.name }}</van-tag>
                            </div>
                            <div class="post-stats">
                                <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                                <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                                <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                            </div>
                        </div>
                    </div>
                </van-tab>
            </van-tabs>
        </div>
        <div class="bottom-spacer"></div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const searchKeyword = ref('')
const activeTab = ref(0)
const banners = ref([
    { title: '搜索技术问题', subtitle: '发现优质代码', bg: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
    { title: 'Python 进阶', subtitle: '从入门到精通', bg: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
    { title: 'Vue3 实战', subtitle: '构建现代前端应用', bg: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }
])
const hotTags = ref([
    { tag_id: 1, name: 'Python', color: '#1989fa' },
    { tag_id: 2, name: 'JavaScript', color: '#ff6b6b' },
    { tag_id: 3, name: 'Vue', color: '#42b883' },
    { tag_id: 4, name: 'React', color: '#61dafb' },
    { tag_id: 5, name: 'Docker', color: '#2496ed' },
    { tag_id: 6, name: 'MySQL', color: '#4479a1' }
])
const recommendPosts = ref([
    { post_id: 1, type: 'article', title: '如何在 Python 中实现多线程并发？', summary: '本文详细介绍了 Python 中多线程的使用方法，包括 threading 模块、线程池、以及 GIL 的影响...', author: { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 1, name: '后端开发' }, tags: [{ tag_id: 1, name: 'Python' }, { tag_id: 7, name: '并发' }], view_count: 1205, like_count: 86, comment_count: 23, favorite_count: 45, created_at: '2025-05-05 10:30:00', is_liked: false, is_favorited: false },
    { post_id: 2, type: 'article', title: 'Vue3 中的组合式 API 如何使用？', summary: '组合式 API 是 Vue3 的重要特性，本文通过实例讲解 setup、ref、reactive 等核心概念...', author: { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 2, name: '前端开发' }, tags: [{ tag_id: 3, name: 'Vue' }, { tag_id: 8, name: '前端' }], view_count: 892, like_count: 64, comment_count: 15, favorite_count: 32, created_at: '2025-05-04 14:20:00', is_liked: true, is_favorited: false },
    { post_id: 3, type: 'article', title: 'MySQL 索引失效的常见场景有哪些？', summary: '总结 MySQL 索引失效的 10 种常见场景，帮助你写出更高效的 SQL 查询...', author: { user_id: 3, username: 'DBA老张', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 4, name: '数据库' }, tags: [{ tag_id: 6, name: 'MySQL' }, { tag_id: 9, name: '数据库' }], view_count: 2341, like_count: 156, comment_count: 42, favorite_count: 89, created_at: '2025-05-03 09:15:00', is_liked: false, is_favorited: true }
])
const articlePosts = ref([
    { post_id: 4, type: 'article', title: '深入理解 Vue3 响应式原理', summary: '从源码角度解析 Vue3 的响应式系统，包括 Proxy、依赖收集、触发更新等核心机制...', author: { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 2, name: '前端开发' }, tags: [{ tag_id: 3, name: 'Vue' }], view_count: 1567, like_count: 98, comment_count: 31, favorite_count: 56, created_at: '2025-05-02 16:45:00', is_liked: false, is_favorited: false },
    { post_id: 5, type: 'article', title: 'Docker 容器化部署实战', summary: '从零开始学习 Docker，包括镜像构建、容器管理、Docker Compose 编排等...', author: { user_id: 4, username: '运维小李', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 5, name: '运维部署' }, tags: [{ tag_id: 5, name: 'Docker' }], view_count: 987, like_count: 72, comment_count: 18, favorite_count: 34, created_at: '2025-05-01 11:20:00', is_liked: true, is_favorited: false }
])
const questionPosts = ref([
    { post_id: 6, type: 'question', title: 'Python 多线程与多进程的区别？', summary: '最近在做高并发项目，想了解一下 Python 中多线程和多进程的使用场景和区别...', author: { user_id: 5, username: '新手小白', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 1, name: '后端开发' }, tags: [{ tag_id: 1, name: 'Python' }], view_count: 456, like_count: 12, comment_count: 8, favorite_count: 5, created_at: '2025-05-05 13:10:00', is_liked: false, is_favorited: false },
    { post_id: 7, type: 'question', title: 'React useEffect 依赖数组问题', summary: 'useEffect 的依赖数组总是导致无限循环，请问正确的使用方式是什么？', author: { user_id: 6, username: '前端新人', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, category: { category_id: 2, name: '前端开发' }, tags: [{ tag_id: 4, name: 'React' }], view_count: 234, like_count: 8, comment_count: 5, favorite_count: 3, created_at: '2025-05-04 17:30:00', is_liked: false, is_favorited: false }
])
const onSearch = () => {
    if (searchKeyword.value.trim()) {
        router.push({ path: '/search', query: { keyword: searchKeyword.value } })
    }
}
const onSearchFocus = () => { router.push('/search') }
const goToSearchFromBanner = (item) => { router.push({ path: '/search', query: { keyword: item.title } }) }
const goToTags = () => { router.push('/tags') }
const goToTag = (tagId) => { router.push({ path: '/tag', query: { id: tagId } }) }
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.shouye-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.search-header { background: #fff; padding: 8px 12px; }
.banner-section { padding: 12px; }
.banner-swipe { border-radius: 8px; height: 140px; }
.banner-item { height: 100%; display: flex; align-items: center; justify-content: center; color: #fff; padding: 20px; }
.banner-content h3 { margin: 0 0 8px; font-size: 20px; }
.banner-content p { margin: 0; font-size: 14px; opacity: 0.9; }
.hot-tags { background: #fff; padding: 12px; margin-bottom: 8px; }
.section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 16px; font-weight: 500; }
.section-title .more { color: #1989fa; font-size: 14px; }
.tag-list { display: flex; flex-wrap: wrap; gap: 8px; }
.hot-tag { padding: 4px 12px; }
.content-tabs { background: #fff; }
.post-list { padding: 12px; }
.post-card { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.post-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.author-name { font-size: 14px; color: #333; font-weight: 500; }
.post-time { font-size: 12px; color: #999; margin-left: auto; }
.post-title { margin: 0 0 8px; font-size: 16px; color: #333; line-height: 1.4; }
.post-summary { margin: 0 0 12px; font-size: 14px; color: #666; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.post-tags { display: flex; gap: 8px; margin-bottom: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; }
.post-stats span { display: flex; align-items: center; gap: 4px; }
.bottom-spacer { height: 80px; }
</style>
