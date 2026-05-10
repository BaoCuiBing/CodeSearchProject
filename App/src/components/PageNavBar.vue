<template>
    <van-nav-bar :title="title" left-arrow :right-text="rightText" @click-left="handleBack" @click-right="handleRight" fixed placeholder />
</template>

<script setup>
import { useRouter } from 'vue-router'
const props = defineProps({ title: { type: String, required: true }, rightText: { type: String, default: '' }, beforeBack: { type: Function, default: null } })
const emit = defineEmits(['click-left', 'click-right'])
const router = useRouter()
const handleBack = () => {
    emit('click-left')
    if (props.beforeBack) { props.beforeBack() }
    else { router.back() }
}
const handleRight = () => { emit('click-right') }
</script>