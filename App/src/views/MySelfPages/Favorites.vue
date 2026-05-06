<template>
    <div class="favorites-page">
        <van-nav-bar title="我的收藏" left-arrow @click-left="goBack" fixed placeholder />
        <van-tabs v-model:active="activeTab">
            <van-tab title="文章">
                <div class="article-list">
                    <div v-for="post in articles" :key="post.post_id" class="post-card" @click="goToDetail(post.post_id)">
                        <h4>{{ post.title }}</h4>
                        <p>{{ post.summary }}</p>
                        <div class="post-stats">
                            <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                            <span><van-icon name="good-job-o" /> {{ post.like_count }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="question-list">
                    <div v-for="q in questions" :key="q.question_id" class="question-card" @click="goToQuestion(q.question_id)">
                        <h4>{{ q.title }}</h4>
                        <p>{{ q.summary }}</p>
                        <div class="question-stats">
                            <span><van-icon name="eye-o" /> {{ q.view_count }}</span>
                            <span><van-icon name="chat-o" /> {{ q.answer_count }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const activeTab = ref(0)
const articles = ref([
    { post_id: 1, title: 'Python多线程实战', summary: '详细介绍Python多线程的使用方法', view_count: 1205, like_count: 86 },
    { post_id: 2, title: 'Python异步编程', summary: 'asyncio模块的使用技巧', view_count: 892, like_count: 64 }
])
const questions = ref([
    { question_id: 1, title: 'Python中如何实现多线程？', summary: '请问Python中如何实现多线程并发？', view_count: 325, answer_count: 12 }
])
const goBack = () => router.back()
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
const goToQuestion = (questionId) => { router.push({ path: '/question', query: { id: questionId } }) }
</script>

<style scoped>
.favorites-page { background: #f5f5f5; min-height: 100vh; }
.article-list, .question-list { padding: 12px; }
.post-card, .question-card { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.post-card h4, .question-card h4 { margin: 0 0 8px; font-size: 16px; }
.post-card p, .question-card p { margin: 0 0 12px; font-size: 14px; color: #666; }
.post-stats, .question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; }
</style>
