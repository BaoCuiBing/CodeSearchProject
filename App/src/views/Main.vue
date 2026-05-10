<template>
    <div class="shouye-page">
        <van-nav-bar title="首页" fixed placeholder />
        <div class="search-header">
            <van-search v-model="searchKeyword" placeholder="搜索技术问题、代码..." @search="onSearch" @focus="onSearchFocus" />
        </div>
        <div class="banner-section">
            <div v-if="bannerLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
            <van-empty v-else-if="bannerError" :description="bannerError" />
            <van-swipe v-else class="banner-swipe" :autoplay="3000" indicator-color="white">
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
            <div v-if="hotTagsLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
            <van-empty v-else-if="hotTagsError" :description="hotTagsError" />
            <div v-else class="tag-list">
                <van-tag v-for="tag in hotTags" :key="tag.tag_id" :color="tag.color" class="hot-tag" @click="goToTag(tag.tag_id, tag.name)">{{ tag.name }}</van-tag>
            </div>
        </div>
        <div class="content-tabs">
            <van-tabs v-model:active="activeTab" @change="onTabChange">
                <van-tab title="推荐">
                    <div class="post-list">
                        <div v-if="recommendLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                        <van-empty v-else-if="recommendError" :description="recommendError" />
                        <van-empty v-else-if="recommendPosts.length === 0" description="暂无推荐" />
                        <PostCard v-else v-for="post in recommendPosts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post)">
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
                    <van-empty v-if="articleError" :description="articleError" />
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
                    <van-empty v-if="questionError" :description="questionError" />
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
        <van-back-top right="30px" bottom="80px" />
    </div>
</template>

<script setup>
import { ref, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog } from 'vant'
import { tagApi, articleApi, systemApi } from '@/assets/app_request_api.js'
import { setCache, getCache, isLogin } from '@/assets/local_storage.js'
import PostCard from '@/components/PostCard.vue'
import PostCardList from '@/components/PostCardList.vue'
const router = useRouter()
const searchKeyword = ref('')
const activeTab = ref(0)
const bannerLoading = ref(true)
const bannerError = ref('')
const hotTagsLoading = ref(true)
const hotTagsError = ref('')
const recommendLoading = ref(true)
const recommendError = ref('')
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
    bannerLoading.value = true
    bannerError.value = ''
    try {
        const cached = getCache('banners')
        if (cached) { banners.value = cached; bannerLoading.value = false; return }
        const data = await systemApi.getCarousel()
        banners.value = (data || []).map(url => ({ img: url }))
        setCache('banners', banners.value, 30 * 60 * 1000)
    } catch (err) {
        bannerError.value = err.message || '加载失败'
    } finally {
        bannerLoading.value = false
    }
}
const loadHotTags = async () => {
    hotTagsLoading.value = true
    hotTagsError.value = ''
    try {
        const cached = getCache('hotTags')
        if (cached) { hotTags.value = cached; hotTagsLoading.value = false; return }
        const data = await tagApi.getHotTags(6)
        hotTags.value = data
        setCache('hotTags', data, 10 * 60 * 1000)
    } catch (err) {
        hotTagsError.value = err.message || '加载失败'
    } finally {
        hotTagsLoading.value = false
    }
}
const loadRecommendPosts = async () => {
    recommendLoading.value = true
    recommendError.value = ''
    try {
        const cached = getCache('recommendPosts')
        if (cached) { recommendPosts.value = cached; recommendLoading.value = false; return }
        const data = await articleApi.getRecommend('recommend_article', 10, true)
        recommendPosts.value = data
        setCache('recommendPosts', data, 5 * 60 * 1000)
    } catch (err) {
        recommendError.value = err.message || '加载失败'
    } finally {
        recommendLoading.value = false
    }
}
const checkLogin = () => {
    if (!isLogin()) { showDialog({ title: '提示', message: '请先登录', showCancelButton: false, confirmButtonText: '去登录' }).then(handleLoginConfirm); return false }
    return true
}
onMounted(() => { if (checkLogin()) { loadBanners(); loadHotTags(); loadRecommendPosts() } })
onActivated(() => { if (checkLogin()) { loadBanners(); loadHotTags(); loadRecommendPosts() } })
const loadArticlePosts = async () => {
    if (articleLoading.value || articleFinished.value) return
    articleLoading.value = true
    try {
        const data = await articleApi.getList({ type: 'article', page: articlePage.value, page_size: 8, sort: 'hot' })
        const list = data.list || []
        articlePosts.value = [...articlePosts.value, ...list]
        articlePage.value++
        if (list.length === 0) { articleFinished.value = true }
    } catch (err) {
        articleError.value = err.message || '加载失败'
        articleFinished.value = true
    } finally {
        articleLoading.value = false
    }
}
const loadQuestionPosts = async () => {
    if (questionLoading.value || questionFinished.value) return
    questionLoading.value = true
    try {
        const data = await articleApi.getList({ type: 'question', page: questionPage.value, page_size: 8, sort: 'hot' })
        const list = data.list || []
        questionPosts.value = [...questionPosts.value, ...list]
        questionPage.value++
        if (list.length === 0) { questionFinished.value = true }
    } catch (err) {
        questionError.value = err.message || '加载失败'
        questionFinished.value = true
    } finally {
        questionLoading.value = false
    }
}
const onTabChange = async (index) => {
    if (index === 1 && articlePosts.value.length === 0 && !articleFinished.value) { await loadArticlePosts() }
    if (index === 2 && questionPosts.value.length === 0 && !questionFinished.value) { await loadQuestionPosts() }
}
const onSearch = () => {
    if (searchKeyword.value.trim()) {
        router.push({ path: '/search', query: { keyword: searchKeyword.value } })
    }
}
const onSearchFocus = () => { router.push('/search') }
const goToTags = () => { router.push('/tags') }
const goToTag = (tagId, tagName) => { router.push({ path: '/tag', query: { id: tagId, name: tagName } }) }
const goToDetail = (post) => { router.push({ path: '/article', query: { id: post.post_id } }) }
const handleLoginConfirm = () => { router.push('/login') }
</script>

<style scoped>
.shouye-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.section-loading { display: flex; justify-content: center; align-items: center; padding: 40px 0; }
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