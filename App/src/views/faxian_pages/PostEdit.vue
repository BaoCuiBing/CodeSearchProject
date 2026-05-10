<template>
    <div class="post-edit-page">
        <van-nav-bar title="发布内容" left-arrow @click-left="handleBack" fixed placeholder>
            <template #right>
                <van-popover v-model:show="showPublishPopover" :actions="publishActions" placement="bottom-end" @select="onPublishSelect">
                    <template #reference>
                        <span class="publish-btn">发布</span>
                    </template>
                </van-popover>
                <van-icon name="notes-o" size="22" color="#333" style="margin-left:12px" @click="showDraftPopup = true" />
            </template>
        </van-nav-bar>
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
        <van-popup v-model:show="showDraftPopup" position="right" :style="{ width: '70%', height: '100%' }">
            <div class="draft-popup">
                <div class="draft-header">
                    <span class="draft-header-title">历史草稿</span>
                    <van-icon name="cross" size="20" @click="showDraftPopup = false" />
                </div>
                <div v-if="draftLoading" class="draft-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                <van-empty v-else-if="drafts.length === 0" description="暂无草稿" />
                <div v-else class="draft-list">
                    <div v-for="draft in drafts" :key="draft.post_id" class="draft-item" @click="loadDraft(draft)">
                        <div class="draft-item-content">
                            <h4>{{ draft.title || '无标题' }}</h4>
                            <p>{{ draft.summary || '无内容' }}</p>
                            <span class="draft-time">{{ draft.updated_at }}</span>
                        </div>
                        <van-icon name="delete-o" size="18" color="#ee0a24" @click.stop="handleDeleteDraft(draft)" />
                    </div>
                </div>
            </div>
        </van-popup>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import TinymceEditor from '@tinymce/tinymce-vue'
import { articleApi, categoryApi, tagApi } from '@/assets/app_request_api.js'
const router = useRouter()
const showCategoryPicker = ref(false)
const showTagPicker = ref(false)
const showDraftPopup = ref(false)
const showPublishPopover = ref(false)
const tagSearchText = ref('')
const categoryColumns = ref([])
const availableTags = ref([])
const publishing = ref(false)
const draftLoading = ref(false)
const drafts = ref([])
const publishActions = [{ text: '发布文章' }, { text: '存为草稿' }]
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
const loadDrafts = async () => {
    draftLoading.value = true
    try {
        const data = await articleApi.getDrafts()
        drafts.value = data?.list || []
    } catch (err) {
        showToast(err.message || '加载失败')
    } finally {
        draftLoading.value = false
    }
}
const onCategoryConfirm = ({ selectedOptions }) => {
    if (selectedOptions && selectedOptions.length > 0) {
        postForm.value.category_id = selectedOptions[0].value
        postForm.value.category_name = selectedOptions[0].text
    }
    showCategoryPicker.value = false
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
const onPublishSelect = (action) => {
    showPublishPopover.value = false
    if (action.text === '发布文章') { handlePublish() }
    else if (action.text === '存为草稿') { saveDraftAndClear() }
}
const handlePublish = () => {
    showConfirmDialog({ title: '确认发布', message: '确定要发布此内容吗？' }).then(() => { publishPost() }).catch(() => {})
}
const publishPost = async () => {
    if (!postForm.value.title.trim()) { showToast('请输入标题'); return }
    if (!postForm.value.category_id) { showToast('请选择分类'); return }
    if (!postForm.value.content.trim()) { showToast('请输入内容'); return }
    publishing.value = true
    try {
        await articleApi.create({ ...postForm.value, tag_ids: postForm.value.tags.map(t => t.tag_id) })
        showToast('发布成功')
        setTimeout(() => { router.push(postForm.value.type === 'article' ? '/my-articles' : '/my-questions') }, 1000)
    } catch (err) {
        showToast(err.message || '发布失败')
    } finally {
        publishing.value = false
    }
}
const handleBack = () => {
    if (!postForm.value.title.trim() && !postForm.value.content.trim()) { router.back(); return }
    showConfirmDialog({ title: '提示', message: '是否需要存为草稿？', confirmButtonText: '存草稿', cancelButtonText: '不保存' }).then(() => { saveDraft() }).catch(() => { router.back() })
}
const saveDraft = async () => {
    try {
        await articleApi.saveDraft({ ...postForm.value, tag_ids: postForm.value.tags.map(t => t.tag_id) })
        showToast('已存为草稿')
        setTimeout(() => { router.back() }, 500)
    } catch (err) {
        showToast(err.message || '保存失败')
    }
}
const saveDraftAndClear = async () => {
    if (!postForm.value.title.trim() && !postForm.value.content.trim()) { showToast('无内容可保存'); return }
    try {
        await articleApi.saveDraft({ ...postForm.value, tag_ids: postForm.value.tags.map(t => t.tag_id) })
        showToast('已存为草稿')
        postForm.value = { title: '', type: 'article', category_id: null, category_name: '', tags: [], content: '' }
    } catch (err) {
        showToast(err.message || '保存失败')
    }
}
const handleDeleteDraft = (draft) => {
    showConfirmDialog({ title: '删除草稿', message: `是否删除草稿"${draft.title || '无标题'}"？` }).then(async () => {
        try {
            await articleApi.deleteDraft(draft.post_id)
            showToast('已删除')
            drafts.value = drafts.value.filter(d => d.post_id !== draft.post_id)
        } catch (err) {
            showToast(err.message || '删除失败')
        }
    }).catch(() => {})
}
const loadDraft = (draft) => {
    postForm.value = { title: draft.title, type: draft.type, category_id: draft.category_id, category_name: draft.category_name, tags: draft.tags || [], content: draft.content }
    showDraftPopup.value = false
    showToast('已加载草稿')
}
onMounted(() => { loadCategories(); loadTags() })
watch(showDraftPopup, (val) => { if (val) { loadDrafts() } })
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
.publish-btn { color: #1989fa; font-size: 14px; margin-left: 12px; cursor: pointer; }
.draft-popup { height: 100%; display: flex; flex-direction: column; }
.draft-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-bottom: 1px solid #f0f0f0; }
.draft-header-title { font-size: 16px; color: #333; }
.draft-loading { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.draft-list { flex: 1; overflow-y: auto; padding: 12px; }
.draft-item { background: #fff; border-radius: 8px; padding: 12px; margin-bottom: 10px; cursor: pointer; display: flex; align-items: center; }
.draft-item-content { flex: 1; min-width: 0; }
.draft-item-content h4 { margin: 0 0 6px; font-size: 15px; color: #333; }
.draft-item-content p { margin: 0 0 6px; font-size: 13px; color: #999; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.draft-time { font-size: 12px; color: #bbb; }
</style>