<template>
    <div class="article-detail-page">
        <PageNavBar title="文章详情" />
        <div v-if="articleLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
        <van-empty v-else-if="articleError" :description="articleError" />
        <template v-else>
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
                <div class="article-body" v-html="article.content"></div>
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
                    <div class="action-item" @click="showCommentSheet = true">
                        <van-icon name="comment-o" color="#999" size="24" />
                        <span>{{ article.comment_count }}</span>
                    </div>
                    <div class="action-item" @click="showShareSheet = true">
                        <van-icon name="share-o" color="#999" size="24" />
                        <span>分享</span>
                    </div>
                </div>
            </div>
            <van-share-sheet v-model:show="showShareSheet" title="分享" :options="shareOptions" @select="onShareSelect" />
            <van-action-sheet v-model:show="showCommentSheet" title="评论">
                <div class="comment-input-wrapper">
                    <van-field v-model="commentContent" rows="3" autosize type="textarea" placeholder="请输入评论..." show-word-limit />
                    <van-button type="primary" size="small" @click="submitComment" :loading="commentLoading">发送</van-button>
                </div>
            </van-action-sheet>
            <div class="comment-section">
                <div class="comment-header">
                    <span>评论 ({{ comments.length }})</span>
                </div>
                <div v-if="commentsLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                <van-empty v-else-if="commentsError" :description="commentsError" />
                <div v-else v-for="comment in comments" :key="comment.comment_id" :id="'comment-' + comment.comment_id" class="comment-item" :class="{ 'highlight-comment': highlightedComment === comment.comment_id }">
                    <van-image round width="32px" height="32px" :src="comment.user?.avatar || ''" />
                    <div class="comment-body">
                        <div class="comment-user">{{ comment.user?.username || '' }}</div>
                        <div class="comment-text">{{ comment.content }}</div>
                        <div class="comment-time">{{ comment.created_at }}</div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { showToast } from 'vant'
import { articleApi, commentApi, followApi, favoriteApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
const route = useRoute()
const articleLoading = ref(true)
const articleError = ref('')
const commentsLoading = ref(true)
const commentsError = ref('')
const article = ref({ title: '', content: '', author: {}, tags: [], like_count: 0, favorite_count: 0, comment_count: 0, view_count: 0, is_liked: false, is_favorited: false, is_followed: false, created_at: '' })
const comments = ref([])
const showCommentSheet = ref(false)
const commentContent = ref('')
const commentLoading = ref(false)
const showShareSheet = ref(false)
const highlightedComment = ref(null)
const shareOptions = [{ name: '复制链接', icon: 'link' }]
const onShareSelect = (option) => {
    if (option.name === '复制链接') {
        const link = window.location.href
        navigator.clipboard.writeText(link).then(() => {
            showToast('已复制链接，粘贴链接以分享')
        })
    }
    showShareSheet.value = false
}
const loadArticle = async () => {
    articleLoading.value = true
    articleError.value = ''
    try {
        const postId = route.query.id
        const data = await articleApi.getDetail(postId)
        article.value = { ...data, tags: data.tags || [], author: data.author || {} }
    } catch (err) {
        articleError.value = err.message || '加载失败'
    } finally {
        articleLoading.value = false
    }
}
const loadComments = async () => {
    commentsLoading.value = true
    commentsError.value = ''
    try {
        const postId = route.query.id
        const data = await commentApi.getList(postId, { page: 1 })
        comments.value = data?.list || []
    } catch (err) {
        commentsError.value = err.message || '加载失败'
    } finally {
        commentsLoading.value = false
    }
}
const loadAll = async () => {
    await Promise.all([loadArticle(), loadComments()])
    const highlight = route.query.highlight_comment
    if (highlight === 'all') {
        await nextTick()
        const commentSection = document.querySelector('.comment-section')
        if (commentSection) { commentSection.scrollIntoView({ behavior: 'smooth', block: 'start' }) }
    } else if (highlight === 'input') {
        await nextTick()
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    }
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
const submitComment = async () => {
    const content = commentContent.value.trim()
    if (!content) return
    commentLoading.value = true
    try {
        const postId = route.query.id
        await commentApi.create(postId, content, null)
        commentContent.value = ''
        showCommentSheet.value = false
        await loadComments()
        const detail = await articleApi.getDetail(postId)
        article.value.comment_count = detail.comment_count
    } finally {
        commentLoading.value = false
    }
}
onMounted(() => { loadAll() })
</script>

<style scoped>
.article-detail-page { background: #f5f5f5; min-height: 100vh; padding-bottom: 60px; overflow-x: hidden; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.section-loading { display: flex; justify-content: center; align-items: center; padding: 40px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.article-content { background: #fff; padding: 16px; margin-bottom: 8px; }
.article-title { margin: 0 0 16px; font-size: 20px; color: #333; line-height: 1.4; }
.article-meta { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.meta-info { flex: 1; display: flex; flex-direction: column; }
.author-name { font-size: 14px; color: #333; font-weight: 500; }
.publish-time { font-size: 12px; color: #999; }
.article-body { font-size: 15px; color: #333; line-height: 1.8; margin-bottom: 16px; max-width: 98%; overflow-x: auto; }
.article-tags { display: flex; gap: 8px; margin-bottom: 16px; }
.article-actions { display: flex; justify-content: space-around; padding: 16px 0; border-top: 1px solid #eee; }
.action-item { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 12px; color: #666; }
.comment-section { background: #fff; padding: 16px; }
.comment-header { font-size: 16px; font-weight: 500; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #eee; }
.comment-item { display: flex; gap: 12px; margin-bottom: 16px; transition: background-color 0.3s; }
.highlight-comment { background-color: #fff3e0; border-radius: 8px; padding: 8px; }
.comment-body { flex: 1; }
.comment-user { font-size: 14px; color: #333; font-weight: 500; margin-bottom: 4px; }
.comment-text { font-size: 14px; color: #666; line-height: 1.5; margin-bottom: 4px; }
.comment-time { font-size: 12px; color: #999; }
.comment-input-wrapper { padding: 16px; display: flex; gap: 12px; align-items: flex-end; }
.comment-input-wrapper .van-field { flex: 1; }
</style>