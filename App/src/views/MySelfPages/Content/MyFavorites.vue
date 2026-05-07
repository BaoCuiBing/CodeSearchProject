<template>
    <div class="my-favorites-page">
        <PageNavBar title="我的收藏" />
        <van-tabs v-model:active="activeTab">
            <van-tab title="全部">
                <div class="fav-list">
                    <van-empty v-if="favorites.length === 0" description="暂无收藏" />
                    <PostCard v-for="item in favorites" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="fav-meta">
                                <van-tag size="small" :type="item.type === 'article' ? 'primary' : 'success'">{{ item.type === 'article' ? '文章' : '问题' }}</van-tag>
                                <span>{{ item.created_at }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="文章">
                <div class="fav-list">
                    <van-empty v-if="articleFavorites.length === 0" description="暂无收藏文章" />
                    <PostCard v-for="item in articleFavorites" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="fav-meta">
                                <span>{{ item.created_at }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="fav-list">
                    <van-empty v-if="questionFavorites.length === 0" description="暂无收藏问题" />
                    <PostCard v-for="item in questionFavorites" :key="item.post_id" :title="item.title" :summary="item.summary" @click="goToDetail(item.post_id)">
                        <template #footer>
                            <div class="fav-meta">
                                <span>{{ item.created_at }}</span>
                            </div>
                        </template>
                    </PostCard>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const activeTab = ref(0)
const favorites = ref([
    { post_id: 1, title: '如何在 Python 中实现多线程并发？', summary: '本文详细介绍了 Python 中多线程的使用方法...', type: 'question', created_at: '2025-05-05' },
    { post_id: 2, title: 'Vue3 中的组合式 API 如何使用？', summary: '组合式 API 是 Vue3 的重要特性...', type: 'article', created_at: '2025-05-04' },
    { post_id: 3, title: 'MySQL 索引失效的常见场景', summary: '总结 MySQL 索引失效的 10 种常见场景...', type: 'article', created_at: '2025-05-03' }
])
const articleFavorites = computed(() => favorites.value.filter(f => f.type === 'article'))
const questionFavorites = computed(() => favorites.value.filter(f => f.type === 'question'))
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.my-favorites-page { background: #f5f5f5; min-height: 100vh; }
.fav-list { padding: 12px; }
.fav-meta { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #999; margin-top: 12px; }
</style>
