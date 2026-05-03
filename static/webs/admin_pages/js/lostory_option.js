var lostoryOption = {
    _cache: {},
    _cacheExpire: 60000,
    getLayer: function() { return (typeof parent !== 'undefined' && parent.layer) ? parent.layer : layer; },
    _setCache: function(key, data) {
        var item = { data: data, time: Date.now() };
        this._cache[key] = item;
        try { localStorage.setItem('lostory_cache_' + key, JSON.stringify(item)); } catch(e) {}
    },
    _getCache: function(key) {
        var item = this._cache[key];
        if (!item) {
            try {
                var raw = localStorage.getItem('lostory_cache_' + key);
                if (raw) { item = JSON.parse(raw); this._cache[key] = item; }
            } catch(e) {}
        }
        if (item && (Date.now() - item.time) < this._cacheExpire) { return item.data; }
        return null;
    },
    _clearCache: function(key) {
        if (key) { delete this._cache[key]; try { localStorage.removeItem('lostory_cache_' + key); } catch(e) {} }
        else { this._cache = {}; try { var keys = Object.keys(localStorage); keys.forEach(function(k) { if (k.indexOf('lostory_cache_') === 0) { localStorage.removeItem(k); } }); } catch(e) {} }
    },
    getAdminId: function() {
        var id = this._getCache('admin_id');
        if (!id) { id = localStorage.getItem('admin_id'); if (id) { this._setCache('admin_id', id); } }
        return id;
    },
    setAdminId: function(id) {
        localStorage.setItem('admin_id', id);
        this._setCache('admin_id', id);
    },
    getAdminName: function() {
        var name = this._getCache('admin_name');
        if (!name) { name = localStorage.getItem('admin_name'); if (name) { this._setCache('admin_name', name); } }
        return name;
    },
    setAdminName: function(name) {
        localStorage.setItem('admin_name', name);
        this._setCache('admin_name', name);
    },
    getCurrentPage: function() {
        var page = this._getCache('current_page');
        if (!page) { page = localStorage.getItem('current_page'); if (page) { this._setCache('current_page', page); } }
        return page || '/admin/dashboard';
    },
    setCurrentPage: function(page) {
        localStorage.setItem('current_page', page);
        this._setCache('current_page', page);
    },
    clearAuth: function() {
        localStorage.removeItem('admin_id');
        localStorage.removeItem('admin_name');
        this._clearCache();
    },
    checkAuth: function() {
        var id = this.getAdminId();
        if (!id) { window.location.href = '/admin/login'; return false; }
        return true;
    },
    openDialog: function(title, url, area) {
        var a = area || ['600px', '400px'];
        return this.getLayer().open({ type: 2, title: title, area: a, shade: 0.6, shadeClose: true, maxmin: false, content: url });
    },
    openPageDialog: function(title, html, area) {
        var a = area || ['500px', '300px'];
        return this.getLayer().open({ type: 1, title: title, area: a, shade: 0.6, shadeClose: true, maxmin: false, content: '<div style="padding:15px;">' + html + '</div>' });
    },
    confirmDialog: function(msg, callback) {
        var L = this.getLayer();
        L.confirm(msg, { btn: ['确认', '取消'] }, function(index) { callback(); L.close(index); });
    },
    msg: function(text, icon) {
        this.getLayer().msg(text, { icon: icon || 1, time: 2000 });
    }
};
