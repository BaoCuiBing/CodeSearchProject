<template>
    <div class="post-edit-page">
        <PageNavBar title="发布内容" right-text="发布" @click-right="publishPost" />
        <div class="edit-form">
            <van-field v-model="postForm.title" placeholder="请输入标题（最多50字）" maxlength="50" />
            <div class="type-selector">
                <van-radio-group v-model="postForm.type" direction="horizontal">
                    <van-radio name="article">文章</van-radio>
                    <van-radio name="question">问题</van-radio>
                </van-radio-group>
            </div>
            <div class="category-selector">
                <van-field v-model="postForm.category_name" readonly is-link placeholder="选择分类" @click="showCategoryPicker = true" />
                <van-popup v-model:show="showCategoryPicker" position="bottom" round>
                    <van-picker :columns="categoryColumns" @confirm="onCategoryConfirm" @cancel="showCategoryPicker = false" />
                </van-popup>
            </div>
            <div class="tag-selector">
                <van-field v-model="tagSearchText" readonly is-link placeholder="选择标签（最多5个）" @click="showTagPicker = true" />
                <van-popup v-model:show="showTagPicker" position="bottom" round>
                    <div class="tag-picker-header">
                        <span>选择标签</span>
                        <span class="tag-picker-count">{{ postForm.tags.length }}/5</span>
                    </div>
                    <div class="tag-picker-list">
                        <van-tag v-for="tag in availableTags" :key="tag.tag_id" :type="isTagSelected(tag.tag_id) ? 'primary' : 'default'" size="large" @click="toggleTag(tag)">{{ tag.name }}</van-tag>
                    </div>
                    <div class="tag-picker-footer">
                        <van-button block type="primary" @click="showTagPicker = false">确定</van-button>
                    </div>
                </van-popup>
                <div class="tag-list">
                    <van-tag v-for="tag in postForm.tags" :key="tag.tag_id" closeable size="medium" type="primary" @close="removeTag(tag.tag_id)">{{ tag.name }}</van-tag>
                </div>
            </div>
            <div class="editor-wrapper">
                <tinymce-editor v-model="postForm.content" :init="editorConfig" :tinymce-script-src="tinymceScriptSrc" :license-key="licenseKey" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showSuccessToast } from 'vant'
import TinymceEditor from '@tinymce/tinymce-vue'
import { articleApi, categoryApi, tagApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
const router = useRouter()
const showCategoryPicker = ref(false)
const showTagPicker = ref(false)
const tagSearchText = ref('')
const categoryColumns = ref([])
const availableTags = ref([])
const publishing = ref(false)
const postForm = ref({ title: '', type: 'article', category_id: null, category_name: '', tags: [], content: '' })
const editorConfig = {
    language_url: '/tinymce/langs/zh_CN.js',
    language: 'zh_CN',
    skin_url: '/tinymce/skins/ui/oxide',
    content_css: '/tinymce/skins/content/default/content.min.css',
    plugins: 'lists code image link table codesample fullscreen preview wordcount',
    toolbar: ['undo redo | bold italic underline strikethrough', 'alignleft aligncenter alignright | bullist numlist', 'table forecolor backcolor | codesample image link', 'fullscreen preview code'],
    width: '100%',
    height: 700,
    branding: false,
    statusbar: true,
    paste_data_images: true,
    license_key: 'gpl'
}
const tinymceScriptSrc = '/tinymce/tinymce.min.js'
const licenseKey = 'gpl'
const loadCategories = async () => {
    const data = await categoryApi.getList()
    categoryColumns.value = (data || []).map(c => ({ text: c.name, value: c.category_id }))
}
const loadTags = async () => {
    const data = await tagApi.getList({ page: 1, page_size: 100 })
    availableTags.value = data?.list || []
}
const isTagSelected = (tagId) => postForm.value.tags.some(t => t.tag_id === tagId)
const toggleTag = (tag) => {
    if (isTagSelected(tag.tag_id)) {
        postForm.value.tags = postForm.value.tags.filter(t => t.tag_id !== tag.tag_id)
    } else if (postForm.value.tags.length < 5) {
        postForm.value.tags.push({ tag_id: tag.tag_id, name: tag.name })
    }
}
const removeTag = (tagId) => { postForm.value.tags = postForm.value.tags.filter(t => t.tag_id !== tagId) }
const publishPost = async () => {
    if (!postForm.value.title.trim()) { showToast('请输入标题'); return }
    if (!postForm.value.category_id) { showToast('请选择分类'); return }
    if (!postForm.value.content.trim()) { showToast('请输入内容'); return }
    publishing.value = true
    try {
        await articleApi.create({ ...postForm.value, tag_ids: postForm.value.tags.map(t => t.tag_id) })
        showSuccessToast('发布成功')
        setTimeout(() => { router.back() }, 1000)
    } catch (err) {
        showToast(err.message || '发布失败')
    } finally {
        publishing.value = false
    }
}
onMounted(() => { loadCategories(); loadTags() })
</script>

<style scoped>
.post-edit-page { background: #f5f5f5; min-height: 100vh; overflow-x: hidden; }
.edit-form { padding: 0; max-width: 100%; overflow-x: hidden; width: 100%; }
.type-selector { padding: 12px 16px; background: #fff; border-bottom: 1px solid #f0f0f0; }
.category-selector { background: #fff; }
.tag-selector { background: #fff; padding-bottom: 12px; }
.tag-picker-header { display: flex; justify-content: space-between; align-items: center; padding: 16px; font-size: 16px; font-weight: bold; }
.tag-picker-count { font-size: 14px; color: #999; font-weight: normal; }
.tag-picker-list { display: flex; flex-wrap: wrap; gap: 10px; padding: 0 16px 16px; max-height: 300px; overflow-y: auto; }
.tag-picker-footer { padding: 0 16px 16px; }
.tag-list { display: flex; flex-wrap: wrap; gap: 8px; padding: 0 16px 8px; }
.editor-wrapper { background: #fff; z-index: 100; padding: 12px 16px; max-width: 100%; box-sizing: border-box; width: 100%; }
</style>