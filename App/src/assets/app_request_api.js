import { getUserId } from './local_storage.js'
import { showDialog, Toast } from 'vant'
const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const request = async (method, url, data, isFormData) => {
    const options = { method, headers: {} }
    if (isFormData) {
        options.body = data
    } else {
        options.headers['Content-Type'] = 'application/json'
        if (data) { options.body = JSON.stringify(data) }
    }
    try {
        const res = await fetch(`${BASE_URL}${url}`, options)
        const json = await res.json()
        if (json.code !== 200) {
            if (json.code === 403) {
                showDialog({ message: '权限不足' }).then(() => { window.location.hash = '#/login' })
            } else if (json.code === 404) {
                showDialog({ message: '资源不存在' })
            } else if (json.code >= 500) {
                showDialog({ message: '服务器繁忙，请稍后重试' })
            } else {
                showDialog({ message: json.msg || '请求失败' })
            }
            throw new Error(json.msg)
        }
        return json.data
    } catch (err) {
        if (err instanceof TypeError) {
            showDialog({ message: '网络连接失败，请检查网络' })
        }
        throw err
    }
}
const get = async (url, params) => {
    const query = []
    if (params) {
        for (const k in params) {
            if (params.hasOwnProperty(k) && params[k] !== null && params[k] !== undefined && params[k] !== '') {
                query.push(`${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
            }
        }
    }
    const fullUrl = query.length > 0 ? `${url}?${query.join('&')}` : url
    return request('GET', fullUrl)
}
const post = async (url, data, isFormData) => request('POST', url, data, isFormData)
const put = async (url, data) => request('PUT', url, data)
const del = async (url, params) => {
    const query = []
    if (params) {
        for (const k in params) {
            if (params.hasOwnProperty(k) && params[k] !== null && params[k] !== undefined && params[k] !== '') {
                query.push(`${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
            }
        }
    }
    const fullUrl = query.length > 0 ? `${url}?${query.join('&')}` : url
    return request('DELETE', fullUrl)
}
export const userApi = {
    register: (usernumber, username, password, email) => post('/api/user/register', { usernumber, username, password, email }),
    login: (usernumber, password) => post('/api/user/login', { usernumber, password })
}
export const profileApi = {
    getProfile: (userId) => get(`/api/profile/${userId}`, { current_user_id: getUserId() }),
    updateProfile: (data) => { data.user_id = getUserId(); return put('/api/profile', data) },
    changePassword: (oldPwd, newPwd) => put('/api/profile/password', { user_id: getUserId(), old_password: oldPwd, new_password: newPwd })
}
export const articleApi = {
    create: (data) => { data.user_id = getUserId(); return post('/api/article', data) },
    getDetail: (postId) => get(`/api/article/${postId}`, { user_id: getUserId() }),
    update: (data) => { data.user_id = getUserId(); return put('/api/article', data) },
    delete: (postId) => del(`/api/article/${postId}`, { user_id: getUserId() }),
    getList: (params = {}) => get('/api/article/list', params),
    toggleLike: (postId) => post('/api/article/like', { user_id: getUserId(), post_id: postId }),
    getRecommend: (type, limit) => get('/api/article/recommend', { type, limit }),
    getToc: (postId) => get(`/api/article/${postId}/toc`)
}
export const categoryApi = {
    getList: () => get('/api/category/list')
}
export const tagApi = {
    getList: (params) => get('/api/tag/list', params),
    getDetail: (tagId) => get(`/api/tag/${tagId}`),
    getArticles: (tagId, params) => get(`/api/tag/${tagId}/articles`, params),
    getHotTags: (limit) => get('/api/tag/hot', { limit })
}
export const commentApi = {
    getList: (postId, params = {}) => { params.user_id = getUserId(); return get(`/api/comment/list/${postId}`, params) },
    create: (postId, content, parentId) => post('/api/comment', { user_id: getUserId(), post_id: postId, content, parent_id: parentId }),
    delete: (commentId) => del(`/api/comment/${commentId}`, { user_id: getUserId() }),
    toggleLike: (commentId) => post('/api/comment/like', { user_id: getUserId(), comment_id: commentId })
}
export const followApi = {
    getFollowing: (followerId, page, pageSize) => get('/api/follow/following', { follower_id: followerId, page, page_size: pageSize }),
    getFollowers: (followingId, page, pageSize) => get('/api/follow/followers', { following_id: followingId, page, page_size: pageSize }),
    toggleFollow: (followingId) => post('/api/follow/user', { follower_id: getUserId(), following_id: followingId }),
    getUserFollowing: (followerId, page, pageSize) => get(`/api/follow/user/${followerId}/following`, { user_id: getUserId(), page, page_size: pageSize }),
    getUserFollowers: (followingId, page, pageSize) => get(`/api/follow/user/${followingId}/followers`, { user_id: getUserId(), page, page_size: pageSize })
}
export const favoriteApi = {
    getList: (params = {}) => { params.user_id = getUserId(); return get('/api/favorite/list', params) },
    batchDelete: (ids) => post('/api/favorite/batch-delete', { user_id: getUserId(), ids }),
    check: (postId) => get(`/api/favorite/check/${postId}`, { user_id: getUserId() }),
    toggle: (postId) => post('/api/favorite/toggle', { user_id: getUserId(), post_id: postId })
}
export const messageApi = {
    getNotifications: (params = {}) => { params.user_id = getUserId(); return get('/api/message/notifications', params) },
    markNotificationRead: (notificationId) => put('/api/message/notification/read', { user_id: getUserId(), notification_id: notificationId }),
    markAllNotificationsRead: () => put('/api/message/notifications/read-all', { user_id: getUserId() }),
    deleteNotification: (notificationId) => del(`/api/message/notification/${notificationId}`, { user_id: getUserId() }),
    getUnreadCount: () => get('/api/message/notification/unread-count', { user_id: getUserId() }),
    getConversations: (page, pageSize) => get('/api/message/conversations', { user_id: getUserId(), page, page_size: pageSize }),
    getConversationMessages: (toUserId, page, pageSize) => get(`/api/message/conversation/user/${toUserId}`, { user_id: getUserId(), page, page_size: pageSize }),
    sendMessage: (toUserId, content) => post('/api/message/send', { from_user_id: getUserId(), to_user_id: toUserId, content }),
    deleteConversation: (toUserId) => del(`/api/message/conversation/user/${toUserId}`, { user_id: getUserId() })
}
export const searchApi = {
    search: (keyword, params = {}) => { params.user_id = getUserId(); params.keyword = keyword; return get('/api/search', params) },
    suggest: (keyword, limit) => get('/api/search/suggest', { keyword, limit }),
    getHot: () => get('/api/search/hot'),
    getHistory: (page, pageSize) => get('/api/search/history', { user_id: getUserId(), page, page_size: pageSize }),
    clearHistory: () => del('/api/search/history/clear', { user_id: getUserId() }),
    deleteHistoryItem: (historyId) => del(`/api/search/history/${historyId}`, { user_id: getUserId() }),
    getFilters: (type) => get('/api/search/filters', { type })
}
export const rankingApi = {
    getList: (type, period, limit) => get('/api/ranking/list', { type, period, limit, user_id: getUserId() }),
    getMyRank: (type, period) => get('/api/ranking/my-rank', { user_id: getUserId(), type, period })
}
export const reportApi = {
    submit: (targetId, targetType, reason) => post('/api/report', { reporter_id: getUserId(), target_id: targetId, target_type: targetType, reason }),
    getMyReports: (params = {}) => { params.reporter_id = getUserId(); return get('/api/report/my-reports', params) }
}
export const uploadApi = {
    uploadFile: (file) => {
        const formData = new FormData()
        formData.append('file', file)
        if (getUserId()) { formData.append('user_id', getUserId()) }
        return post('/api/upload/file', formData, true)
    }
}
export const systemApi = {
    getCarousel: () => get('/api/system/carousel')
}
