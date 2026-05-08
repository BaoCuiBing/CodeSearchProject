<template>
    <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
        <PostCard v-for="post in posts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="$emit('click', post)">
            <template #header>
                <slot name="header" :post="post" />
            </template>
            <template #tags>
                <slot name="tags" :post="post" />
            </template>
            <template #footer>
                <slot name="footer" :post="post" />
            </template>
        </PostCard>
    </van-list>
</template>

<script setup>
import { computed } from 'vue'
import PostCard from './PostCard.vue'
const props = defineProps({
    loading: { type: Boolean, default: false },
    finished: { type: Boolean, default: false },
    posts: { type: Array, default: () => [] }
})
const emit = defineEmits(['load', 'click'])
const loading = computed({
    get: () => props.loading,
    set: (val) => {}
})
const finished = computed({
    get: () => props.finished,
    set: (val) => {}
})
const onLoad = () => {
    emit('load')
}
</script>
