<template>
    <van-nav-bar :title="title" left-arrow @click-left="goBack" fixed placeholder />
</template>

<script setup>
import { useRouter } from 'vue-router'
defineProps({ title: { type: String, required: true } })
const router = useRouter()
const goBack = () => router.back()
</script>
