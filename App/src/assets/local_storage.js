const USER_KEY = 'app_user'
const cache = new Map()
const DEFAULT_TTL = 5 * 60 * 1000
export const setCache = (key, value, ttl = DEFAULT_TTL) => {
    cache.set(key, { value, expire: Date.now() + ttl })
}
export const getCache = (key) => {
    const item = cache.get(key)
    if (!item) return null
    if (Date.now() > item.expire) {
        cache.delete(key)
        return null
    }
    return item.value
}
export const removeCache = (key) => cache.delete(key)
export const clearCache = () => cache.clear()
export const hasCache = (key) => {
    const item = cache.get(key)
    if (!item) return false
    if (Date.now() > item.expire) {
        cache.delete(key)
        return false
    }
    return true
}
export const setUser = (user) => localStorage.setItem(USER_KEY, JSON.stringify(user))
export const getUser = () => {
    const data = localStorage.getItem(USER_KEY)
    return data ? JSON.parse(data) : null
}
export const removeUser = () => localStorage.removeItem(USER_KEY)
export const getUserId = () => {
    const user = getUser()
    return user ? user.user_id : ''
}
export const isLogin = () => !!getUser()
export const logout = () => {
    removeUser()
    clearCache()
}
