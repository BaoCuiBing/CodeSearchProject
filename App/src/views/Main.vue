<template>
    <div class="shouye-page">
        <van-nav-bar title="首页" fixed placeholder />
        <div class="search-header">
            <van-search v-model="searchKeyword" placeholder="搜索技术问题、代码..." @search="onSearch" @focus="onSearchFocus" />
        </div>
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
                                    <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                                    <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                                </div>
                            </template>
                        </PostCard>
                    </div>
                </van-tab>
                <van-tab title="文章">
                    <div class="post-list">
                        <van-empty v-if="articlePosts.length === 0" description="暂无文章" />
                        <PostCard v-for="post in articlePosts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
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
                                    <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                                    <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                                </div>
                            </template>
                        </PostCard>
                    </div>
                </van-tab>
                <van-tab title="问题">
                    <div class="post-list">
                        <van-empty v-if="questionPosts.length === 0" description="暂无问题" />
                        <PostCard v-for="post in questionPosts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
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
                                    <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                                    <span><van-icon name="comment-o" /> {{ post.comment_count }}</span>
                                </div>
                            </template>
                        </PostCard>
                    </div>
                </van-tab>
            </van-tabs>
        </div>
        <div class="bottom-spacer"></div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { tagApi, articleApi, systemApi } from '@/assets/app_request_api.js'
import { setCache, getCache, isLogin } from '@/assets/local_storage.js'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const searchKeyword = ref('')
const activeTab = ref(0)
const banners = ref([])
const hotTags = ref([])
const recommendPosts = ref([])
const articlePosts = ref([])
const questionPosts = ref([])
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
    const data = await articleApi.getRecommend('recommend_article', 20)
    recommendPosts.value = data
    setCache('recommendPosts', data, 5 * 60 * 1000)
}
const loadArticlePosts = async () => {
    const data = await articleApi.getList({ type: 'article', page: 1, sort: 'hot' })
    articlePosts.value = data.list || []
}
const loadQuestionPosts = async () => {
    const data = await articleApi.getList({ type: 'question', page: 1, sort: 'hot' })
    questionPosts.value = data.list || []
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
onMounted(async () => {
    if (!isLogin()) { router.replace('/login'); return }
    await Promise.all([loadBanners(), loadHotTags(), loadRecommendPosts()])
})
</script>

<style scoped>
.shouye-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.search-header { background: #fff; padding: 8px 12px; }
.banner-section { padding: 12px; }
.banner-swipe { border-radius: 8px; height: 140px; }
.banner-item { height: 100%; width: 100%; border-radius: 8px; overflow: hidden; }
.hot-tags { background: #fff; padding: 12px; margin-bottom: 8px; }
.section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 16px; font-weight: 500; }
.section-title .more { color: #1989fa; font-size: 14px; }
.tag-list { display: flex; flex-wrap: wrap; gap: 8px; }
.hot-tag { padding: 4px 12px; }
.content-tabs { background: #fff; }
.post-list { padding: 12px; }
.post-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.author-name { font-size: 14px; color: #333; font-weight: 500; }
.post-time { font-size: 12px; color: #999; margin-left: auto; }
.post-tags { display: flex; gap: 8px; margin-bottom: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
.post-stats span { display: flex; align-items: center; gap: 4px; }
.bottom-spacer { height: 80px; }
</style>
