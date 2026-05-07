<template>
    <div class="article-detail-page">
        <PageNavBar title="文章详情" />
        <div class="article-content">
            <h1 class="article-title">{{ article.title }}</h1>
            <div class="article-meta">
                <van-image round width="36px" height="36px" :src="article.author?.avatar || ''" />
                <div class="meta-info">
                    <span class="author-name">{{ article.author?.username || '' }}</span>
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
                    <van-icon name="good-job" :color="article.is_liked ? '#ff6b6b' : '#999'" size="24" />
                    <span>{{ article.like_count }}</span>
                </div>
                <div class="action-item" @click="toggleFavorite">
                    <van-icon name="star" :color="article.is_favorited ? '#ffd700' : '#999'" size="24" />
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
                <van-image round width="32px" height="32px" :src="comment.user?.avatar || ''" />
                <div class="comment-body">
                    <div class="comment-user">{{ comment.user?.username || '' }}</div>
                    <div class="comment-text">{{ comment.content }}</div>
                    <div class="comment-time">{{ comment.created_at }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { articleApi, commentApi, followApi, favoriteApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
const route = useRoute()
const article = ref({ title: '', content: '', author: {}, tags: [], like_count: 0, favorite_count: 0, comment_count: 0, view_count: 0, is_liked: false, is_favorited: false, is_followed: false, created_at: '' })
const comments = ref([])
const loadArticle = async () => {
    const postId = route.query.id
    const data = await articleApi.getDetail(postId)
    article.value = { ...data, tags: data.tags || [], author: data.author || {} }
}
const loadComments = async () => {
    const postId = route.query.id
    const data = await commentApi.getList(postId, { page: 1 })
    comments.value = data?.list || []
}
const toggleLike = async () => {
    const postId = route.query.id
    const data = await articleApi.toggleLike(postId)
    article.value.is_liked = data.is_liked !== undefined ? data.is_liked : !article.value.is_liked
    article.value.like_count += article.value.is_liked ? 1 : -1
}
const toggleFavorite = async () => {
    const postId = route.query.id
    const data = await favoriteApi.toggle(postId)
    article.value.is_favorited = data.is_favorited !== undefined ? data.is_favorited : !article.value.is_favorited
    article.value.favorite_count += article.value.is_favorited ? 1 : -1
}
const toggleFollow = async () => {
    const authorId = article.value.author?.user_id
    if (!authorId) return
    const data = await followApi.toggleFollow(authorId)
    article.value.is_followed = data.is_followed !== undefined ? data.is_followed : !article.value.is_followed
}
onMounted(async () => {
    await Promise.all([loadArticle(), loadComments()])
})
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
