<template>
    <div class="my-questions-page">
        <PageNavBar title="我的提问" />
        <div v-if="loading && questions.length === 0" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <div v-else class="question-list">
            <van-empty v-if="!loading && questions.length === 0" description="暂无提问" />
            <PostCardList v-else :loading="loading" :finished="finished" :posts="questions" @load="loadQuestions" @click="goToDetail">
                <template #footer="{ post }">
                    <div class="question-stats">
                        <span><van-icon name="eye-o" /> {{ post.view_count }}</span>
                        <span><van-icon name="chat-o" /> {{ post.comment_count }}</span>
                    </div>
                </template>
            </PostCardList>
        </div>
        <van-floating-bubble :gap="{x: 30, y: 80}" icon="plus" @click="goToPostEdit" />
        <van-back-top right="30px" bottom="130px" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { articleApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCardList from '@/components/PostCardList.vue'
const router = useRouter()
const loading = ref(false)
const finished = ref(false)
const error = ref('')
const questions = ref([])
const page = ref(1)
const loadQuestions = async () => {
    if (loading.value || finished.value) return
    loading.value = true
    error.value = ''
    try {
        const data = await articleApi.getList({ user_id: getUserId(), type: 'question', page: page.value })
        const list = data?.list || []
        if (list.length === 0) { finished.value = true }
        else { questions.value = [...questions.value, ...list]; page.value++ }
    } catch (err) {
        error.value = err.message || '加载失败'
        finished.value = true
    } finally {
        loading.value = false
    }
}
const goToDetail = (post) => { router.push({ path: '/article', query: { id: post.post_id } }) }
const goToPostEdit = () => { router.push('/post-edit') }
onMounted(() => { loadQuestions() })
</script>

<style scoped>
.my-questions-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.question-list { padding: 12px; }
.question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>