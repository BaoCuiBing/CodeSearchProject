var appApi = {
    _userId: null,
    _baseUrl: '',
    setUserId: function(id) { this._userId = id; },
    getUserId: function() { return this._userId || ''; },
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
    user: {
        register: function(usernumber, username, password, email) { return appApi._post('/api/user/register', { usernumber: usernumber, username: username, password: password, email: email }); },
        login: function(usernumber, password) { return appApi._post('/api/user/login', { usernumber: usernumber, password: password }); }
    },
    profile: {
        getProfile: function(userId) { return appApi._get('/api/profile/' + userId, { current_user_id: appApi.getUserId() }); },
        updateProfile: function(data) { data.user_id = appApi.getUserId(); return appApi._put('/api/profile', data); },
        changePassword: function(oldPwd, newPwd) { return appApi._put('/api/profile/password', { user_id: appApi.getUserId(), old_password: oldPwd, new_password: newPwd }); }
    },
    article: {
        create: function(data) { data.user_id = appApi.getUserId(); return appApi._post('/api/article', data); },
        getDetail: function(postId) { return appApi._get('/api/article/' + postId, { user_id: appApi.getUserId() }); },
        update: function(data) { data.user_id = appApi.getUserId(); return appApi._put('/api/article', data); },
        delete: function(postId) { return appApi._delete('/api/article/' + postId, { user_id: appApi.getUserId() }); },
        getList: function(params) { params = params || {}; params.user_id = appApi.getUserId(); return appApi._get('/api/article/list', params); },
        toggleLike: function(postId) { return appApi._post('/api/article/like', { user_id: appApi.getUserId(), post_id: postId }); },
        getRecommend: function(type, limit) { return appApi._get('/api/article/recommend', { type: type, limit: limit }); },
        getToc: function(postId) { return appApi._get('/api/article/' + postId + '/toc'); }
    },
    category: {
        getList: function() { return appApi._get('/api/category/list'); }
    },
    tag: {
        getList: function(params) { return appApi._get('/api/tag/list', params); },
        getDetail: function(tagId) { return appApi._get('/api/tag/' + tagId); },
        getArticles: function(tagId, params) { return appApi._get('/api/tag/' + tagId + '/articles', params); },
        getHotTags: function(limit) { return appApi._get('/api/tag/hot', { limit: limit }); }
    },
    comment: {
        getList: function(postId, params) { params = params || {}; params.user_id = appApi.getUserId(); return appApi._get('/api/comment/list/' + postId, params); },
        create: function(postId, content, parentId) { return appApi._post('/api/comment', { user_id: appApi.getUserId(), post_id: postId, content: content, parent_id: parentId }); },
        delete: function(commentId) { return appApi._delete('/api/comment/' + commentId, { user_id: appApi.getUserId() }); },
        toggleLike: function(commentId) { return appApi._post('/api/comment/like', { user_id: appApi.getUserId(), comment_id: commentId }); }
    },
    follow: {
        getFollowing: function(followerId, page, pageSize) { return appApi._get('/api/follow/following', { follower_id: followerId, page: page, page_size: pageSize }); },
        getFollowers: function(followingId, page, pageSize) { return appApi._get('/api/follow/followers', { following_id: followingId, page: page, page_size: pageSize }); },
        toggleFollow: function(followingId) { return appApi._post('/api/follow/user', { follower_id: appApi.getUserId(), following_id: followingId }); },
        getUserFollowing: function(followerId, page, pageSize) { return appApi._get('/api/follow/user/' + followerId + '/following', { user_id: appApi.getUserId(), page: page, page_size: pageSize }); },
        getUserFollowers: function(followingId, page, pageSize) { return appApi._get('/api/follow/user/' + followingId + '/followers', { user_id: appApi.getUserId(), page: page, page_size: pageSize }); }
    },
    favorite: {
        getList: function(params) { params = params || {}; params.user_id = appApi.getUserId(); return appApi._get('/api/favorite/list', params); },
        batchDelete: function(ids) { return appApi._post('/api/favorite/batch-delete', { user_id: appApi.getUserId(), ids: ids }); },
        check: function(postId) { return appApi._get('/api/favorite/check/' + postId, { user_id: appApi.getUserId() }); },
        toggle: function(postId) { return appApi._post('/api/favorite/toggle', { user_id: appApi.getUserId(), post_id: postId }); }
    },
    message: {
        getNotifications: function(params) { params = params || {}; params.user_id = appApi.getUserId(); return appApi._get('/api/message/notifications', params); },
        markNotificationRead: function(notificationId) { return appApi._put('/api/message/notification/read', { user_id: appApi.getUserId(), notification_id: notificationId }); },
        markAllNotificationsRead: function() { return appApi._put('/api/message/notifications/read-all', { user_id: appApi.getUserId() }); },
        deleteNotification: function(notificationId) { return appApi._delete('/api/message/notification/' + notificationId, { user_id: appApi.getUserId() }); },
        getUnreadCount: function() { return appApi._get('/api/message/notification/unread-count', { user_id: appApi.getUserId() }); },
        getConversations: function(page, pageSize) { return appApi._get('/api/message/conversations', { user_id: appApi.getUserId(), page: page, page_size: pageSize }); },
        getConversationMessages: function(toUserId, page, pageSize) { return appApi._get('/api/message/conversation/user/' + toUserId, { user_id: appApi.getUserId(), page: page, page_size: pageSize }); },
        sendMessage: function(toUserId, content) { return appApi._post('/api/message/send', { from_user_id: appApi.getUserId(), to_user_id: toUserId, content: content }); },
        deleteConversation: function(toUserId) { return appApi._delete('/api/message/conversation/user/' + toUserId, { user_id: appApi.getUserId() }); }
    },
    search: {
        search: function(keyword, params) { params = params || {}; params.user_id = appApi.getUserId(); params.keyword = keyword; return appApi._get('/api/search', params); },
        suggest: function(keyword, limit) { return appApi._get('/api/search/suggest', { keyword: keyword, limit: limit }); },
        getHot: function() { return appApi._get('/api/search/hot'); },
        getHistory: function(page, pageSize) { return appApi._get('/api/search/history', { user_id: appApi.getUserId(), page: page, page_size: pageSize }); },
        clearHistory: function() { return appApi._delete('/api/search/history/clear', { user_id: appApi.getUserId() }); },
        deleteHistoryItem: function(historyId) { return appApi._delete('/api/search/history/' + historyId, { user_id: appApi.getUserId() }); },
        getFilters: function(type) { return appApi._get('/api/search/filters', { type: type }); }
    },
    ranking: {
        getList: function(type, period, limit) { return appApi._get('/api/ranking/list', { type: type, period: period, limit: limit, user_id: appApi.getUserId() }); },
        getMyRank: function(type, period) { return appApi._get('/api/ranking/my-rank', { user_id: appApi.getUserId(), type: type, period: period }); }
    },
    report: {
        submit: function(targetId, targetType, reason) { return appApi._post('/api/report', { reporter_id: appApi.getUserId(), target_id: targetId, target_type: targetType, reason: reason }); },
        getMyReports: function(params) { params = params || {}; params.reporter_id = appApi.getUserId(); return appApi._get('/api/report/my-reports', params); }
    },
    upload: {
        uploadFile: function(file) {
            var formData = new FormData();
            formData.append('file', file);
            if (appApi.getUserId()) { formData.append('user_id', appApi.getUserId()); }
            return appApi._post('/api/upload/file', formData, true);
        }
    }
};