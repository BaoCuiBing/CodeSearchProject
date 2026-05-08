<template>
    <div class="security-page">
        <PageNavBar title="账号与安全" />
        <van-cell-group>
            <van-cell title="修改密码" is-link @click="showPasswordDialog = true" />
            <van-cell title="绑定邮箱" is-link @click="showEmailDialog = true" />
            <van-cell title="绑定手机" is-link @click="showPhoneDialog = true" />
        </van-cell-group>
        <van-dialog v-model:show="showPasswordDialog" title="修改密码" show-cancel-button @confirm="handleChangePassword" :before-close="beforePasswordClose">
            <div class="dialog-form">
                <van-field v-model="oldPassword" type="password" label="原密码" placeholder="请输入原密码" />
                <van-field v-model="newPassword" type="password" label="新密码" placeholder="请输入新密码（6-20位）" />
                <van-field v-model="confirmPassword" type="password" label="确认密码" placeholder="请再次输入新密码" />
            </div>
        </van-dialog>
        <van-dialog v-model:show="showEmailDialog" title="绑定邮箱" show-cancel-button @confirm="handleBindEmail">
            <div class="dialog-form">
                <van-field v-model="email" type="text" label="邮箱" placeholder="请输入邮箱地址" />
            </div>
        </van-dialog>
        <van-dialog v-model:show="showPhoneDialog" title="绑定手机" show-cancel-button @confirm="handleBindPhone">
            <div class="dialog-form">
                <van-field v-model="phone" type="tel" label="手机号" placeholder="请输入手机号" />
            </div>
        </van-dialog>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { showToast } from 'vant'
import { profileApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
const showPasswordDialog = ref(false)
const showEmailDialog = ref(false)
const showPhoneDialog = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const email = ref('')
const phone = ref('')
const beforePasswordClose = (action) => {
    if (action === 'confirm') {
        if (!oldPassword.value || !newPassword.value || !confirmPassword.value) { showToast('请填写完整信息'); return false }
        if (newPassword.value.length < 6) { showToast('新密码不能少于6位'); return false }
        if (newPassword.value !== confirmPassword.value) { showToast('两次密码不一致'); return false }
    }
    return true
}
const handleChangePassword = async () => {
    try {
        await profileApi.changePassword(oldPassword.value, newPassword.value)
        showToast('密码修改成功')
        oldPassword.value = ''
        newPassword.value = ''
        confirmPassword.value = ''
    } catch (err) {
        showToast(err.message || '修改失败')
    }
}
const handleBindEmail = async () => {
    if (!email.value) { showToast('请输入邮箱'); return }
    try {
        await profileApi.updateProfile({ email: email.value })
        showToast('邮箱绑定成功')
        email.value = ''
    } catch (err) {
        showToast(err.message || '绑定失败')
    }
}
const handleBindPhone = async () => {
    if (!phone.value) { showToast('请输入手机号'); return }
    try {
        await profileApi.updateProfile({ phone: phone.value })
        showToast('手机号绑定成功')
        phone.value = ''
    } catch (err) {
        showToast(err.message || '绑定失败')
    }
}
</script>

<style scoped>
.security-page { background: #f5f5f5; min-height: 100vh; }
.dialog-form { padding: 12px 0; }
</style>