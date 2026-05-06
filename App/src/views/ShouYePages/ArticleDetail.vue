<template>
    <div class="article-detail-page">
        <van-nav-bar title="文章详情" left-arrow @click-left="goBack" fixed placeholder />
        <div class="article-content">
            <h1 class="article-title">{{ article.title }}</h1>
            <div class="article-meta">
                <van-image round width="36px" height="36px" :src="article.author.avatar" />
                <div class="meta-info">
                    <span class="author-name">{{ article.author.username }}</span>
                    <span class="publish-time">{{ article.created_at }}</span>
                </div>
                <van-button size="small" :type="article.is_followed ? 'default' : 'primary'" @click="toggleFollow">{{ article.is_followed ? '已关注' : '关注' }}</van-button>
            </div>
            <div class="article-body">
                <p>{{ article.content }}</p>
            </div>
            <div class="article-tags">
                <van-tag v-for="tag in article.tags" :key="tag.tag_id" type="primary" plain>{{ tag.name }}</van-tag>
            </div>
            <div class="article-actions">
                <div class="action-item" @click="toggleLike">
                    <van-icon name="good-job" :color="article.is_liked ? '#1989fa' : '#999'" size="24" />
                    <span>{{ article.like_count }}</span>
                </div>
                <div class="action-item" @click="toggleFavorite">
                    <van-icon name="star" :color="article.is_favorited ? '#ff6b6b' : '#999'" size="24" />
                    <span>{{ article.favorite_count }}</span>
                </div>
                <div class="action-item">
                    <van-icon name="comment-o" color="#999" size="24" />
                    <span>{{ article.comment_count }}</span>
                </div>
                <div class="action-item">
                    <van-icon name="share-o" color="#999" size="24" />
                    <span>分享</span>
                </div>
            </div>
        </div>
        <div class="comment-section">
            <div class="comment-header">
                <span>评论 ({{ comments.length }})</span>
            </div>
            <div v-for="comment in comments" :key="comment.comment_id" class="comment-item">
                <van-image round width="32px" height="32px" :src="comment.user.avatar" />
                <div class="comment-body">
                    <div class="comment-user">{{ comment.user.username }}</div>
                    <div class="comment-text">{{ comment.content }}</div>
                    <div class="comment-time">{{ comment.created_at }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
const article = ref({
    post_id: route.query.id || 1,
    type: 'article',
    title: '如何在 Python 中实现多线程并发？',
    content: 'Python 中的多线程可以通过 threading 模块实现。虽然由于 GIL（全局解释器锁）的存在，多线程在 CPU 密集型任务中无法真正实现并行，但在 I/O 密集型任务中仍然非常有用。\n\n首先，我们需要导入 threading 模块：\n\nimport threading\n\n然后，可以创建一个线程类或者使用 Thread 类的 target 参数来指定线程执行的函数。',
    summary: '本文详细介绍了 Python 中多线程的使用方法，包括 threading 模块、线程池、以及 GIL 的影响...',
    cover_image: ['https://img.yzcdn.cn/vant/cat.jpeg'],
    author: { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' },
    category: { category_id: 1, name: '后端开发' },
    tags: [{ tag_id: 1, name: 'Python' }, { tag_id: 7, name: '并发' }],
    like_count: 86,
    favorite_count: 45,
    comment_count: 23,
    view_count: 1205,
    is_liked: false,
    is_favorited: false,
    is_followed: false,
    created_at: '2025-05-05 10:30:00',
    updated_at: '2025-05-05 10:30:00'
})
const comments = ref([
    { comment_id: 1, user: { user_id: 10, username: '用户A', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, content: '写得很详细，感谢分享！', like_count: 5, created_at: '2025-05-05 14:30:00' },
    { comment_id: 2, user: { user_id: 11, username: '用户B', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, content: 'GIL 的问题确实让人头疼，多进程会不会更好一些？', like_count: 3, created_at: '2025-05-05 15:20:00' },
    { comment_id: 3, user: { user_id: 12, username: '用户C', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, content: '收藏了，后面慢慢看', like_count: 1, created_at: '2025-05-05 16:00:00' }
])
const goBack = () => router.back()
const toggleLike = () => { article.value.is_liked = !article.value.is_liked; article.value.like_count += article.value.is_liked ? 1 : -1 }
const toggleFavorite = () => { article.value.is_favorited = !article.value.is_favorited; article.value.favorite_count += article.value.is_favorited ? 1 : -1 }
const toggleFollow = () => { article.value.is_followed = !article.value.is_followed }
</script>

<style scoped>
.article-detail-page { background: #f5f5f5; min-height: 100vh; padding-bottom: 60px; }
.article-content { background: #fff; padding: 16px; margin-bottom: 8px; }
.article-title { margin: 0 0 16px; font-size: 20px; color: #333; line-height: 1.4; }
.article-meta { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.meta-info { flex: 1; display: flex; flex-direction: column; }
.author-name { font-size: 14px; color: #333; font-weight: 500; }
.publish-time { font-size: 12px; color: #999; }
.article-body { font-size: 15px; color: #333; line-height: 1.8; margin-bottom: 16px; }
.article-tags { display: flex; gap: 8px; margin-bottom: 16px; }
.article-actions { display: flex; justify-content: space-around; padding: 16px 0; border-top: 1px solid #eee; }
.action-item { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 12px; color: #666; }
.comment-section { background: #fff; padding: 16px; }
.comment-header { font-size: 16px; font-weight: 500; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #eee; }
.comment-item { display: flex; gap: 12px; margin-bottom: 16px; }
.comment-body { flex: 1; }
.comment-user { font-size: 14px; color: #333; font-weight: 500; margin-bottom: 4px; }
.comment-text { font-size: 14px; color: #666; line-height: 1.5; margin-bottom: 4px; }
.comment-time { font-size: 12px; color: #999; }
</style>
