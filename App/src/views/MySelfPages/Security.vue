<template>
    <div class="security-page">
        <PageNavBar title="账号与安全" />
        <van-cell-group>
            <van-cell title="修改密码" is-link @click="changePassword" />
            <van-cell title="绑定邮箱" is-link @click="bindEmail" />
            <van-cell title="绑定手机" is-link @click="bindPhone" />
        </van-cell-group>
    </div>
</template>

<script setup>
import { showToast } from 'vant'
import PageNavBar from '@/components/PageNavBar.vue'
const changePassword = () => { showToast('修改密码') }
const bindEmail = () => { showToast('绑定邮箱') }
const bindPhone = () => { showToast('绑定手机') }
</script>

<style scoped>
.security-page { background: #f5f5f5; min-height: 100vh; }
</style>
