<template>
    <div class="my-articles-page">
        <PageNavBar title="我的文章" />
        <div class="article-list">
            <van-empty v-if="articles.length === 0" description="暂无文章" />
            <PostCard v-for="post in articles" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
                <template #footer>
                    <div class="post-stats">
                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                        <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                    </div>
                </template>
            </PostCard>
        </div>
        <van-floating-bubble :gap="{x: 30, y: 80}" icon="plus" @click="goToPostEdit" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { articleApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const articles = ref([])
const loadArticles = async () => {
    const data = await articleApi.getList({ user_id: getUserId(), type: 'article', page: 1 })
    articles.value = data?.list || []
}
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const goToPostEdit = () => { router.push('/post-edit') }
onMounted(() => { loadArticles() })
</script>

<style scoped>
.my-articles-page { background: #f5f5f5; min-height: 100vh; }
.article-list { padding: 12px; }
.post-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
