const SendLog = (function() {
    let config = { api_url: "/api/log/send", enabled: true };
    function log(level, message, module = "default", user_id = null) {
        if (!config.enabled) return;
        fetch(config.api_url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ level, message, module, user_id, timestamp: new Date().toISOString() })
        }).catch(err => console.error("日志发送失败:", err));
    }
    function setEnabled(enabled) { config.enabled = enabled; }
    function log_debug(message, module = "default", user_id = null) { log("debug", message, module, user_id); }
    function log_info(message, module = "default", user_id = null) { log("info", message, module, user_id); }
    function log_warning(message, module = "default", user_id = null) { log("warn", message, module, user_id); }
    function log_error(message, module = "default", user_id = null) { log("error", message, module, user_id); }
    function log_critical(message, module = "default", user_id = null) { log("critical", message, module, user_id); }
    return { log, log_debug, log_info, log_warning, log_error, log_critical, setEnabled };
})();
window.addEventListener("error", e => SendLog.log_error(`${e.message} at ${e.filename}:${e.lineno}`, "global"));
window.addEventListener("unhandledrejection", e => SendLog.log_error(`未捕获Promise错误: ${e.reason}`, "global"));
if (typeof module !== "undefined" && module.exports) module.exports = SendLog;