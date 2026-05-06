var adminApi = {
    _adminId: null,
    _baseUrl: '',
    setAdminId: function(id) { this._adminId = id; },
    getAdminId: function() { return this._adminId || ''; },
    _request: function(method, url, data, isFormData) {
        var self = this;
        var options = { method: method, headers: {} };
        if (isFormData) {
            options.body = data;
        } else {
            options.headers['Content-Type'] = 'application/json';
            if (data) { options.body = JSON.stringify(data); }
        }
        return fetch(self._baseUrl + url, options).then(function(res) { return res.json(); });
    },
    _get: function(url, params) {
        var query = [];
        if (params) { for (var k in params) { if (params.hasOwnProperty(k) && params[k] !== null && params[k] !== undefined && params[k] !== '') { query.push(encodeURIComponent(k) + '=' + encodeURIComponent(params[k])); } } }
        var fullUrl = url + (query.length > 0 ? '?' + query.join('&') : '');
        return this._request('GET', fullUrl);
    },
    _post: function(url, data, isFormData) { return this._request('POST', url, data, isFormData); },
    _put: function(url, data) { return this._request('PUT', url, data); },
    _delete: function(url, params) {
        var query = [];
        if (params) { for (var k in params) { if (params.hasOwnProperty(k) && params[k] !== null && params[k] !== undefined && params[k] !== '') { query.push(encodeURIComponent(k) + '=' + encodeURIComponent(params[k])); } } }
        var fullUrl = url + (query.length > 0 ? '?' + query.join('&') : '');
        return this._request('DELETE', fullUrl);
    },
    auth: {
        login: function(usernumber, password) { return adminApi._post('/api/admin/auth/login', { usernumber: usernumber, password: password }); },
        getMe: function() { return adminApi._get('/api/admin/auth/me', { admin_id: adminApi.getAdminId() }); },
        changePassword: function(newPwd, confirmPwd) { return adminApi._put('/api/admin/auth/change-password', { admin_id: adminApi.getAdminId(), new_password: newPwd, confirm_password: confirmPwd }); }
    },
    user: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/user/list', params); },
        getDetail: function(userId) { return adminApi._get('/api/admin/user/' + userId, { admin_id: adminApi.getAdminId() }); },
        ban: function(userId, action, reason, duration) { return adminApi._post('/api/admin/user/ban', { admin_id: adminApi.getAdminId(), user_id: userId, action: action, reason: reason, duration: duration }); },
        toggleStatus: function(userId) { return adminApi._post('/api/admin/user/ban', { admin_id: adminApi.getAdminId(), user_id: userId, action: 'toggle' }); },
        delete: function(userId) { return adminApi._delete('/api/admin/user/' + userId, { admin_id: adminApi.getAdminId() }); },
        edit: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._put('/api/admin/user/', data); },
        resetPassword: function(userId, newPwd) { return adminApi._post('/api/admin/user/reset-password', { admin_id: adminApi.getAdminId(), user_id: userId, new_password: newPwd }); },
        batchAction: function(ids, action) { return adminApi._post('/api/admin/user/batch-action', { admin_id: adminApi.getAdminId(), ids: ids, action: action }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/user/batch-delete', { admin_id: adminApi.getAdminId(), ids: ids }); },
        exportData: function() { return adminApi._post('/api/admin/user/export', { admin_id: adminApi.getAdminId() }); },
        getStatsOverview: function(period) { return adminApi._get('/api/admin/user/stats/overview', { admin_id: adminApi.getAdminId(), period: period }); },
        create: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/user/', data); },
        sendNotify: function(userId, title, content) { return adminApi._post('/api/admin/user/' + userId + '/notify', { title: title, content: content }); }
    },
    article: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/article/list', params); },
        getDetail: function(postId) { return adminApi._get('/api/admin/article/' + postId, { admin_id: adminApi.getAdminId() }); },
        create: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/article/', data); },
        edit: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._put('/api/admin/article/', data); },
        delete: function(postId) { return adminApi._delete('/api/admin/article/' + postId, { admin_id: adminApi.getAdminId() }); },
        batchAction: function(ids, action) { return adminApi._post('/api/admin/article/batch-action', { admin_id: adminApi.getAdminId(), ids: ids, action: action }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/article/batch-action', { admin_id: adminApi.getAdminId(), ids: ids, action: 'delete' }); },
        toggleTop: function(postId, isTop) { return adminApi._post('/api/admin/article/top', { admin_id: adminApi.getAdminId(), post_id: postId, is_top: isTop }); },
        toggleStatus: function(postId) { return adminApi._post('/api/admin/article/toggle-status', { admin_id: adminApi.getAdminId(), post_id: postId }); },
        getStatsOverview: function(period) { return adminApi._get('/api/admin/article/stats/overview', { admin_id: adminApi.getAdminId(), period: period }); },
        exportData: function() { return adminApi._post('/api/admin/article/export', { admin_id: adminApi.getAdminId() }); }
    },
    category: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/category/list', params); },
        create: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/category/', data); },
        edit: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._put('/api/admin/category/', data); },
        delete: function(categoryId, moveToId) { return adminApi._delete('/api/admin/category/' + categoryId, { admin_id: adminApi.getAdminId(), move_to_id: moveToId }); },
        batchAction: function(ids, action) { return adminApi._post('/api/admin/category/batch-action', { admin_id: adminApi.getAdminId(), ids: ids, action: action }); }
    },
    tag: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/tag/list', params); },
        getDetail: function(tagId) { return adminApi._get('/api/admin/tag/' + tagId, { admin_id: adminApi.getAdminId() }); },
        create: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/tag/', data); },
        edit: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._put('/api/admin/tag/', data); },
        delete: function(tagId) { return adminApi._delete('/api/admin/tag/' + tagId, { admin_id: adminApi.getAdminId() }); },
        batchAction: function(ids, action) { return adminApi._post('/api/admin/tag/batch-action', { admin_id: adminApi.getAdminId(), ids: ids, action: action }); },
        getStatsOverview: function() { return adminApi._get('/api/admin/tag/stats/overview', { admin_id: adminApi.getAdminId() }); }
    },
    comment: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/comment/list', params); },
        getDetail: function(commentId) { return adminApi._get('/api/admin/comment/' + commentId, { admin_id: adminApi.getAdminId() }); },
        reply: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/comment/reply', data); },
        delete: function(commentId, deleteReplies) { return adminApi._delete('/api/admin/comment/' + commentId, { admin_id: adminApi.getAdminId(), delete_replies: deleteReplies ? 'true' : 'false' }); },
        toggleVisibility: function(commentId, isHidden) { return adminApi._put('/api/admin/comment/visibility', { admin_id: adminApi.getAdminId(), comment_id: commentId, is_hidden: isHidden }); },
        batchAction: function(ids, action) { return adminApi._post('/api/admin/comment/batch-action', { admin_id: adminApi.getAdminId(), ids: ids, action: action }); },
        getStatsOverview: function(period) { return adminApi._get('/api/admin/comment/stats/overview', { admin_id: adminApi.getAdminId(), period: period }); },
        exportData: function() { return adminApi._post('/api/admin/comment/export', { admin_id: adminApi.getAdminId() }); }
    },
    message: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/system_messages/list', params); },
        create: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/system_messages/', data); },
        edit: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._put('/api/admin/system_messages/', data); },
        delete: function(messageId) { return adminApi._delete('/api/admin/system_messages/' + messageId, { admin_id: adminApi.getAdminId() }); },
        send: function(messageId) { return adminApi._post('/api/admin/system_messages/send', { admin_id: adminApi.getAdminId(), system_message_id: messageId }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/system_messages/batch-delete', { admin_id: adminApi.getAdminId(), ids: ids }); },
        getStatsOverview: function() { return adminApi._get('/api/admin/system_messages/stats/overview', { admin_id: adminApi.getAdminId() }); },
        getDetail: function(messageId) { return adminApi._get('/api/admin/system_messages/' + messageId + '/detail', { admin_id: adminApi.getAdminId() }); },
        sendToUser: function(userId, title, content) { return adminApi._post('/api/admin/system_messages/send-to-user', { admin_id: adminApi.getAdminId(), user_id: userId, title: title, content: content }); }
    },
    report: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/report/list', params); },
        getDetail: function(reportId) { return adminApi._get('/api/admin/report/' + reportId, { admin_id: adminApi.getAdminId() }); },
        handle: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/report/handle', data); },
        batchHandle: function(ids, action, handleNote) { return adminApi._post('/api/admin/report/batch-handle', { admin_id: adminApi.getAdminId(), ids: ids, action: action, handle_note: handleNote }); },
        handleArticle: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/report/article/handle', data); },
        handleComment: function(data) { data.admin_id = adminApi.getAdminId(); return adminApi._post('/api/admin/report/comment/handle', data); }
    },
    stats: {
        getDashboard: function(period) { return adminApi._get('/api/admin/stats/dashboard', { admin_id: adminApi.getAdminId(), period: period }); },
        getUsers: function(period) { return adminApi._get('/api/admin/stats/users', { admin_id: adminApi.getAdminId(), period: period }); },
        getContent: function(period) { return adminApi._get('/api/admin/stats/content', { admin_id: adminApi.getAdminId(), period: period }); },
        getSearchKeywords: function(period, limit) { return adminApi._get('/api/admin/stats/search-keywords', { admin_id: adminApi.getAdminId(), period: period, limit: limit }); },
        exportReport: function() { return adminApi._post('/api/admin/stats/export-report', { admin_id: adminApi.getAdminId() }); },
        compare: function(metric, p1s, p1e, p2s, p2e) { return adminApi._get('/api/admin/stats/compare', { admin_id: adminApi.getAdminId(), metric: metric, period1_start: p1s, period1_end: p1e, period2_start: p2s, period2_end: p2e }); }
    },
    system: {
        getSettings: function(key) { return adminApi._get('/api/admin/system/settings', { admin_id: adminApi.getAdminId(), key: key }); },
        updateSettings: function(key, value, description) { return adminApi._put('/api/admin/system/settings', { admin_id: adminApi.getAdminId(), key: key, value: value, description: description }); },
        resetSettings: function(key) { return adminApi._post('/api/admin/system/settings/reset', { admin_id: adminApi.getAdminId(), key: key }); },
        testEmail: function(toEmail) { return adminApi._post('/api/admin/system/test-email', { admin_id: adminApi.getAdminId(), to_email: toEmail }); },
        clearCache: function(cacheTypes) { return adminApi._post('/api/admin/system/clear-cache', { admin_id: adminApi.getAdminId(), cache_types: cacheTypes || ['all'] }); }
    },
    file: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/file/list', params); },
        delete: function(fileId) { return adminApi._delete('/api/admin/file/' + fileId, { admin_id: adminApi.getAdminId() }); }
    },
    upload: {
        uploadFile: function(file, userId) {
            var formData = new FormData();
            formData.append('file', file);
            if (userId) { formData.append('user_id', userId); }
            return adminApi._post('/api/upload/file', formData, true);
        }
    },
    favorite: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/favorite/list', params); },
        delete: function(favoriteId) { return adminApi._delete('/api/admin/favorite/' + favoriteId, { admin_id: adminApi.getAdminId() }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/favorite/batch-delete', { admin_id: adminApi.getAdminId(), ids: ids }); }
    },
    like: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/like/list', params); },
        delete: function(likeId) { return adminApi._delete('/api/admin/like/' + likeId, { admin_id: adminApi.getAdminId() }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/like/batch-delete', { admin_id: adminApi.getAdminId(), ids: ids }); }
    },
    follow: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/follow/list', params); },
        delete: function(followId) { return adminApi._delete('/api/admin/follow/' + followId, { admin_id: adminApi.getAdminId() }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/follow/batch-delete', { admin_id: adminApi.getAdminId(), ids: ids }); }
    },
    privateMessage: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/private_message/list', params); },
        getDetail: function(messageId) { return adminApi._get('/api/admin/private_message/' + messageId + '/detail', { admin_id: adminApi.getAdminId() }); },
        delete: function(messageId) { return adminApi._delete('/api/admin/private_message/' + messageId, { admin_id: adminApi.getAdminId() }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/private_message/batch-delete', { admin_id: adminApi.getAdminId(), ids: ids }); }
    },
    searchHistory: {
        getList: function(params) { params = params || {}; params.admin_id = adminApi.getAdminId(); return adminApi._get('/api/admin/search-history/list', params); },
        delete: function(searchId) { return adminApi._delete('/api/admin/search-history/' + searchId, { admin_id: adminApi.getAdminId() }); },
        batchDelete: function(ids) { return adminApi._post('/api/admin/search-history/batch-delete', { admin_id: adminApi.getAdminId(), ids: ids }); }
    }
};
