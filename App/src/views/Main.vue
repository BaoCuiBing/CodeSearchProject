<template>
    <div class="shouye-page">
        <van-nav-bar title="首页" fixed placeholder />
        <div class="search-header">
            <van-search v-model="searchKeyword" placeholder="搜索技术问题、代码..." @search="onSearch" @focus="onSearchFocus" />
        </div>
        <div v-if="initLoading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <div v-else-if="initError" class="error-wrap">
            <van-icon name="warn-o" size="48" color="#999" />
            <p class="error-text">{{ initError }}</p>
            <van-button type="primary" size="small" @click="loadInitData">重试</van-button>
        </div>
        <template v-else>
            <div class="banner-section">
                <van-swipe class="banner-swipe" :autoplay="3000" indicator-color="white">
                    <van-swipe-item v-for="(item, index) in banners" :key="index">
                        <div class="banner-item">
                            <van-image width="100%" height="100%" fit="cover" :src="item.img" />
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
                    <van-tag v-for="tag in hotTags" :key="tag.tag_id" :color="tag.color" class="hot-tag" @click="goToTag(tag.tag_id, tag.name)">{{ tag.name }}</van-tag>
                </div>
            </div>
            <div class="content-tabs">
                <van-tabs v-model:active="activeTab" sticky offset-top="0" @change="onTabChange">
                    <van-tab title="推荐">
                        <div class="post-list">
                            <van-empty v-if="recommendPosts.length === 0" description="暂无推荐" />
                            <PostCard v-for="post in recommendPosts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
                                <template #header>
                                    <div class="post-header">
                                        <van-image round width="32px" height="32px" :src="post.author?.avatar || ''" />
                                        <span class="author-name">{{ post.author?.username || '' }}</span>
                                        <span class="post-time">{{ post.created_at }}</span>
                                    </div>
                                </template>
                                <template #tags>
                                    <div class="post-tags">
                                        <van-tag v-for="tag in post.tags" :key="tag.tag_id" size="small" type="primary" plain>{{ tag.name }}</van-tag>
                                    </div>
                                </template>
                                <template #footer>
                                    <div class="post-stats">
                                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                                        <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ post.like_count }}</span>
                                        <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                                    </div>
                                </template>
                            </PostCard>
                        </div>
                    </van-tab>
                    <van-tab title="文章">
                        <div v-if="articleError" class="error-wrap">
                            <van-icon name="warn-o" size="48" color="#999" />
                            <p class="error-text">{{ articleError }}</p>
                            <van-button type="primary" size="small" @click="loadArticlePosts">重试</van-button>
                        </div>
                        <template v-else>
                            <van-empty v-if="!articleLoading && articlePosts.length === 0" description="暂无文章" />
                            <PostCardList v-else :loading="articleLoading" :finished="articleFinished" :posts="articlePosts" @load="loadArticlePosts" @click="goToDetail">
                                <template #header="{ post }">
                                    <div class="post-header">
                                        <van-image round width="32px" height="32px" :src="post.author?.avatar || ''" />
                                        <span class="author-name">{{ post.author?.username || '' }}</span>
                                        <span class="post-time">{{ post.created_at }}</span>
                                    </div>
                                </template>
                                <template #tags="{ post }">
                                    <div class="post-tags">
                                        <van-tag v-for="tag in post.tags" :key="tag.tag_id" size="small" type="primary" plain>{{ tag.name }}</van-tag>
                                    </div>
                                </template>
                                <template #footer="{ post }">
                                    <div class="post-stats">
                                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                                        <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ post.like_count }}</span>
                                        <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                                    </div>
                                </template>
                            </PostCardList>
                        </template>
                    </van-tab>
                    <van-tab title="问题">
                        <div v-if="questionError" class="error-wrap">
                            <van-icon name="warn-o" size="48" color="#999" />
                            <p class="error-text">{{ questionError }}</p>
                            <van-button type="primary" size="small" @click="loadQuestionPosts">重试</van-button>
                        </div>
                        <template v-else>
                            <van-empty v-if="!questionLoading && questionPosts.length === 0" description="暂无问题" />
                            <PostCardList v-else :loading="questionLoading" :finished="questionFinished" :posts="questionPosts" @load="loadQuestionPosts" @click="goToDetail">
                                <template #header="{ post }">
                                    <div class="post-header">
                                        <van-image round width="32px" height="32px" :src="post.author?.avatar || ''" />
                                        <span class="author-name">{{ post.author?.username || '' }}</span>
                                        <span class="post-time">{{ post.created_at }}</span>
                                    </div>
                                </template>
                                <template #tags="{ post }">
                                    <div class="post-tags">
                                        <van-tag v-for="tag in post.tags" :key="tag.tag_id" size="small" type="primary" plain>{{ tag.name }}</van-tag>
                                    </div>
                                </template>
                                <template #footer="{ post }">
                                    <div class="post-stats">
                                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                                        <span><van-icon name="good-job-o" color="#ff6b6b" /> {{ post.like_count }}</span>
                                        <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                                    </div>
                                </template>
                            </PostCardList>
                        </template>
                    </van-tab>
                </van-tabs>
            </div>
        </template>
        <div class="bottom-spacer"></div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog } from 'vant'
import { tagApi, articleApi, systemApi } from '@/assets/app_request_api.js'
import { setCache, getCache, isLogin } from '@/assets/local_storage.js'
import PostCard from '@/components/PostCard.vue'
import PostCardList from '@/components/PostCardList.vue'
const router = useRouter()
const searchKeyword = ref('')
const activeTab = ref(0)
const initLoading = ref(true)
const initError = ref('')
const banners = ref([])
const hotTags = ref([])
const recommendPosts = ref([])
const articlePosts = ref([])
const questionPosts = ref([])
const articlePage = ref(1)
const questionPage = ref(1)
const articleLoading = ref(false)
const questionLoading = ref(false)
const articleFinished = ref(false)
const questionFinished = ref(false)
const articleError = ref('')
const questionError = ref('')
const loadBanners = async () => {
    const cached = getCache('banners')
    if (cached) { banners.value = cached; return }
    const data = await systemApi.getCarousel()
    banners.value = (data || []).map(url => ({ img: url }))
    setCache('banners', banners.value, 30 * 60 * 1000)
}
const loadHotTags = async () => {
    const cached = getCache('hotTags')
    if (cached) { hotTags.value = cached; return }
    const data = await tagApi.getHotTags(6)
    hotTags.value = data
    setCache('hotTags', data, 10 * 60 * 1000)
}
const loadRecommendPosts = async () => {
    const cached = getCache('recommendPosts')
    if (cached) { recommendPosts.value = cached; return }
    const data = await articleApi.getRecommend('recommend_article', 10, true)
    recommendPosts.value = data
    setCache('recommendPosts', data, 5 * 60 * 1000)
}
const loadInitData = async () => {
    initLoading.value = true
    initError.value = ''
    try {
        await Promise.all([loadBanners(), loadHotTags(), loadRecommendPosts()])
    } catch (err) {
        initError.value = err.message || '加载失败'
    } finally {
        initLoading.value = false
    }
}
const loadArticlePosts = async () => {
    articleLoading.value = true
    articleError.value = ''
    try {
        const data = await articleApi.getList({ type: 'article', page: articlePage.value, page_size: 8, sort: 'hot' })
        const list = data.list || []
        articlePosts.value = [...articlePosts.value, ...list]
        articlePage.value++
        if (list.length === 0) { articleFinished.value = true }
    } catch (err) {
        articleError.value = err.message || '加载失败'
    } finally {
        articleLoading.value = false
    }
}
const loadQuestionPosts = async () => {
    questionLoading.value = true
    questionError.value = ''
    try {
        const data = await articleApi.getList({ type: 'question', page: questionPage.value, page_size: 8, sort: 'hot' })
        const list = data.list || []
        questionPosts.value = [...questionPosts.value, ...list]
        questionPage.value++
        if (list.length === 0) { questionFinished.value = true }
    } catch (err) {
        questionError.value = err.message || '加载失败'
    } finally {
        questionLoading.value = false
    }
}
const onTabChange = async (index) => {
    if (index === 1 && articlePosts.value.length === 0) { await loadArticlePosts() }
    if (index === 2 && questionPosts.value.length === 0) { await loadQuestionPosts() }
}
const onSearch = () => {
    if (searchKeyword.value.trim()) {
        router.push({ path: '/search', query: { keyword: searchKeyword.value } })
    }
}
const onSearchFocus = () => { router.push('/search') }
const goToTags = () => { router.push('/tags') }
const goToTag = (tagId, tagName) => { router.push({ path: '/tag', query: { id: tagId, name: tagName } }) }
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const handleLoginConfirm = () => { router.push('/login') }
onMounted(async () => {
    if (!isLogin()) { showDialog({ title: '提示', message: '请先登录', showCancelButton: false, confirmButtonText: '去登录' }).then(handleLoginConfirm); return }
    await loadInitData()
})
</script>

<style scoped>
.shouye-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.search-header { background: #fff; padding: 8px 12px; }
.banner-section { padding: 12px; }
.banner-swipe { border-radius: 8px; height: 140px; }
.banner-item { height: 100%; width: 100%; border-radius: 8px; overflow: hidden; }
.hot-tags { background: #fff; padding: 16px; margin-bottom: 8px; }
.section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 16px; font-weight: 500; }
.section-title .more { color: #1989fa; font-size: 14px; }
.tag-list { display: flex; flex-wrap: wrap; gap: 8px; }
.hot-tag { padding: 6px 12px; cursor: pointer; }
.content-tabs { background: #fff; }
.post-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.author-name { font-size: 14px; color: #333; font-weight: 500; }
.post-time { font-size: 12px; color: #999; margin-left: auto; }
.post-tags { display: flex; gap: 6px; margin-bottom: 8px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
.bottom-spacer { height: 80px; }
</style>