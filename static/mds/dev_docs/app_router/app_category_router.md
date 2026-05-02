# 分类路由接口文档

## 文件路径
`router/app_category_router.py`

## 蓝图配置
- **蓝图名称**: `category`
- **URL前缀**: `/api/category`

## 接口列表

### 1. 获取分类列表（APP端）
- **路径**: `/api/category/list`
- **方法**: `GET`
- **函数名**: `get_categories`
- **OpenAPI摘要**: 获取所有分类列表（UI图15）

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | array | 分类列表 |
| data[].category_id | int | 分类ID |
| data[].name | string | 分类名称 |
| data[].icon | string | 分类图标 |
| data[].sort | int | 排序 |
| data[].post_count | int | 文章数量（动态查询posts表统计） |

#### 请求示例
```
GET /api/category/list
```

#### 响应示例（失败）
```json
{
    "code": 500,
    "msg": "服务器内部错误"
}
```
