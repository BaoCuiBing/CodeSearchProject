<template>
    <div class="favorites-page">
        <PageNavBar title="我的收藏" />
        <van-tabs v-model:active="activeTab">
            <van-tab title="文章">
                <div class="article-list">
                    <PostCard v-for="post in articles" :key="post.post_id" :title="post.title" :summary="post.summary" @click="goToDetail(post.post_id)">
                        <template #footer>
                            <div class="post-stats">
                                <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                                <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="question-list">
                    <PostCard v-for="q in questions" :key="q.question_id" :title="q.title" :summary="q.summary" @click="goToQuestion(q.question_id)">
                        <template #footer>
                            <div class="question-stats">
                                <span><van-icon name="eye-o" /> {{ q.view_count }}</span>
                                <span><van-icon name="chat-o" /> {{ q.answer_count }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const activeTab = ref(0)
const articles = ref([
    { post_id: 1, title: 'Python多线程实战', summary: '详细介绍Python多线程的使用方法', view_count: 1205, like_count: 86 },
    { post_id: 2, title: 'Python异步编程', summary: 'asyncio模块的使用技巧', view_count: 892, like_count: 64 }
])
const questions = ref([
    { question_id: 1, title: 'Python中如何实现多线程？', summary: '请问Python中如何实现多线程并发？', view_count: 325, answer_count: 12 }
])
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const goToQuestion = (questionId) => { router.push({ path: '/question', query: { id: questionId } }) }
</script>

<style scoped>
.favorites-page { background: #f5f5f5; min-height: 100vh; }
.article-list, .question-list { padding: 12px; }
.post-stats, .question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
