# APP路由文档设计

## 数据库设计

参考[数据库设计.md](file:///workspace/数据库设计.md)，共17张表：users、reports、search_history、files、posts、tags、post_tags、comments、favorites、likes、follows、messages、system_messages、system_message_targets、system_settings、notifications、categories

## 通用约定

- 统一返回：成功{code,msg,data}，失败{code,msg}，见[global_error_code.md](file:///workspace/dev_docs/global_error_code.md)
- 鉴权：不使用任何请求头；APP端通过user_id标识用户（弱鉴权，不做防伪）
- 参数位置：以各接口文档为准；写操作通常Body(JSON)，查询通常Query
- 分页：page/page_size，默认1/20
- 派生字段：公开GET若允许不传user_id，则派生字段按false处理（如is_liked/is_favorited）

## 文档索引

| 模块 | URL前缀 | 路由文件 | 文档 |
| --- | --- | --- | --- |
| 用户 | /api/user | router/app_user_router.py | [app_user_router.md](file:///workspace/dev_docs/app_router/app_user_router.md) |
| 用户资料 | /api/profile | router/app_profile_router.py | [app_profile_router.md](file:///workspace/dev_docs/app_router/app_profile_router.md) |
| 文章/问题 | /api/article | router/app_article_router.py | [app_article_router.md](file:///workspace/dev_docs/app_router/app_article_router.md) |
| 分类 | /api/category | router/app_category_router.py | [app_category_router.md](file:///workspace/dev_docs/app_router/app_category_router.md) |
| 标签 | /api/tag | router/app_tag_router.py | [app_tag_router.md](file:///workspace/dev_docs/app_router/app_tag_router.md) |
| 评论 | /api/comment | router/app_comment_router.py | [app_comment_router.md](file:///workspace/dev_docs/app_router/app_comment_router.md) |
| 关注 | /api/follow | router/app_follow_router.py | [app_follow_router.md](file:///workspace/dev_docs/app_router/app_follow_router.md) |
| 收藏 | /api/favorite | router/app_favorite_router.py | [app_favorite_router.md](file:///workspace/dev_docs/app_router/app_favorite_router.md) |
| 消息通知 | /api/message | router/app_message_router.py | [app_message_router.md](file:///workspace/dev_docs/app_router/app_message_router.md) |
| 搜索 | /api/search | router/app_search_router.py | [app_search_router.md](file:///workspace/dev_docs/app_router/app_search_router.md) |
| 排行榜 | /api/ranking | router/app_ranking_router.py | [app_ranking_router.md](file:///workspace/dev_docs/app_router/app_ranking_router.md) |
| 举报 | /api/report | router/app_report_router.py | [app_report_router.md](file:///workspace/dev_docs/app_router/app_report_router.md) |

## 共享文档

- 上传接口：[upload_router.md](file:///workspace/dev_docs/upload_router.md)
- 主应用路由：[app.md](file:///workspace/dev_docs/app.md)
