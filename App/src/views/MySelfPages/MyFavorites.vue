<template>
    <div class="my-favorites-page">
        <van-nav-bar title="我的收藏" left-arrow @click-left="goBack" fixed placeholder />
        <van-tabs v-model:active="activeTab">
            <van-tab title="全部">
                <div class="fav-list">
                    <div v-for="item in favorites" :key="item.post_id" class="fav-item" @click="goToDetail(item.post_id)">
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.summary }}</p>
                        <div class="fav-meta">
                            <van-tag size="small" :type="item.type === 'article' ? 'primary' : 'success'">{{ item.type === 'article' ? '文章' : '问题' }}</van-tag>
                            <span>{{ item.created_at }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="文章">
                <div class="fav-list">
                    <div v-for="item in articleFavorites" :key="item.post_id" class="fav-item" @click="goToDetail(item.post_id)">
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.summary }}</p>
                        <div class="fav-meta">
                            <span>{{ item.created_at }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
            <van-tab title="问题">
                <div class="fav-list">
                    <div v-for="item in questionFavorites" :key="item.post_id" class="fav-item" @click="goToDetail(item.post_id)">
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.summary }}</p>
                        <div class="fav-meta">
                            <span>{{ item.created_at }}</span>
                        </div>
                    </div>
                </div>
            </van-tab>
        </van-tabs>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const activeTab = ref(0)
const favorites = ref([
    { post_id: 1, title: '如何在 Python 中实现多线程并发？', summary: '本文详细介绍了 Python 中多线程的使用方法...', type: 'question', created_at: '2025-05-05' },
    { post_id: 2, title: 'Vue3 中的组合式 API 如何使用？', summary: '组合式 API 是 Vue3 的重要特性...', type: 'article', created_at: '2025-05-04' },
    { post_id: 3, title: 'MySQL 索引失效的常见场景', summary: '总结 MySQL 索引失效的 10 种常见场景...', type: 'article', created_at: '2025-05-03' }
])
const articleFavorites = computed(() => favorites.value.filter(f => f.type === 'article'))
const questionFavorites = computed(() => favorites.value.filter(f => f.type === 'question'))
const goBack = () => router.back()
const goToDetail = (postId) => { router.push({ path: '/article', query: { id: postId } }) }
</script>

<style scoped>
.my-favorites-page { background: #f5f5f5; min-height: 100vh; }
.fav-list { padding: 12px; }
.fav-item { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.fav-item h4 { margin: 0 0 8px; font-size: 16px; color: #333; }
.fav-item p { margin: 0 0 12px; font-size: 14px; color: #666; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.fav-meta { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #999; }
</style>
