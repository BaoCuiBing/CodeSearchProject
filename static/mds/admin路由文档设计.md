# admin路由文档设计

## 数据库设计

参考[数据库设计.md](file:///workspace/数据库设计.md)，共17张表：users、reports、search_history、files、posts、tags、post_tags、comments、favorites、likes、follows、messages、system_messages、system_message_targets、system_settings、notifications、categories

## 通用约定

- 统一返回：成功{code,msg,data}，失败{code,msg}，见[global_error_code.md](file:///workspace/dev_docs/global_error_code.md)
- 鉴权：不使用任何请求头；管理端通过admin_id标识管理员并校验users.role=admin
- 参数位置：GET用Query传admin_id；写操作（POST/PUT）用Body(JSON)传admin_id
- 分页：page/page_size，默认1/20
- 导出：同步导出并返回data.filename/data.file_url（不做task_id/download_url）

## 文档索引（API）

| 模块 | URL前缀 | 路由文件 | 文档 |
| --- | --- | --- | --- |
| 登录认证 | /api/admin/auth | router/admin_auth_router.py | [admin_auth_router.md](file:///workspace/dev_docs/admin_router/admin_auth_router.md) |
| 用户管理 | /api/admin/user | router/admin_user_router.py | [admin_user_router.md](file:///workspace/dev_docs/admin_router/admin_user_router.md) |
| 文章管理 | /api/admin/article | router/admin_article_router.py | [admin_article_router.md](file:///workspace/dev_docs/admin_router/admin_article_router.md) |
| 评论管理 | /api/admin/comment | router/admin_comment_router.py | [admin_comment_router.md](file:///workspace/dev_docs/admin_router/admin_comment_router.md) |
| 分类管理 | /api/admin/category | router/admin_category_router.py | [admin_category_router.md](file:///workspace/dev_docs/admin_router/admin_category_router.md) |
| 标签管理 | /api/admin/tag | router/admin_tag_router.py | [admin_tag_router.md](file:///workspace/dev_docs/admin_router/admin_tag_router.md) |
| 举报管理 | /api/admin/report | router/admin_report_router.py | [admin_report_router.md](file:///workspace/dev_docs/admin_router/admin_report_router.md) |
| 系统消息 | /api/admin/system_messages | router/admin_message_router.py | [admin_message_router.md](file:///workspace/dev_docs/admin_router/admin_message_router.md) |
| 私信管理 | /api/admin/private_message | router/admin_private_message_router.py | [admin_private_message_router.md](file:///workspace/dev_docs/admin_router/admin_private_message_router.md) |
| 数据统计 | /api/admin/stats | router/admin_stats_router.py | [admin_stats_router.md](file:///workspace/dev_docs/admin_router/admin_stats_router.md) |
| 系统设置 | /api/admin/system | router/admin_system_router.py | [admin_system_router.md](file:///workspace/dev_docs/admin_router/admin_system_router.md) |
| 文件管理 | /api/admin/file | router/admin_file_router.py | [admin_file_router.md](file:///workspace/dev_docs/admin_router/admin_file_router.md) |
| 搜索记录 | /api/admin/search-history | router/admin_search_history_router.py | [admin_search_history_router.md](file:///workspace/dev_docs/admin_router/admin_search_history_router.md) |
| 点赞管理 | /api/admin/like | router/admin_like_router.py | [admin_like_router.md](file:///workspace/dev_docs/admin_router/admin_like_router.md) |
| 关注管理 | /api/admin/follow | router/admin_follow_router.py | [admin_follow_router.md](file:///workspace/dev_docs/admin_router/admin_follow_router.md) |
| 收藏管理 | /api/admin/favorite | router/admin_favorite_router.py | [admin_favorite_router.md](file:///workspace/dev_docs/admin_router/admin_favorite_router.md) |

## 文档索引（页面）

| 模块 | 路由文件 | 文档 |
| --- | --- | --- |
| 管理端页面路由 | router/admin_view_router.py | [admin_view_router.md](file:///workspace/dev_docs/admin_router/admin_view_router.md) |

## 共享文档

- 上传接口：[upload_router.md](file:///workspace/dev_docs/upload_router.md)
