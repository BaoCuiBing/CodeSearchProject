<template>
    <div class="security-page">
        <van-nav-bar title="账号与安全" left-arrow @click-left="goBack" fixed placeholder />
        <van-cell-group>
            <van-cell title="修改密码" is-link @click="changePassword" />
            <van-cell title="绑定邮箱" is-link @click="bindEmail" />
            <van-cell title="绑定手机" is-link @click="bindPhone" />
        </van-cell-group>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
const router = useRouter()
const goBack = () => router.back()
const changePassword = () => { showToast('修改密码') }
const bindEmail = () => { showToast('绑定邮箱') }
const bindPhone = () => { showToast('绑定手机') }
</script>

<style scoped>
.security-page { background: #f5f5f5; min-height: 100vh; }
</style>
