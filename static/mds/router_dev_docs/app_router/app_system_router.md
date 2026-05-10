# 系统路由接口文档

## 文件路径
`router/app_system_router.py`

## 蓝图配置
- **蓝图名称**: `system`
- **URL前缀**: `/api/system`

## 接口列表

### 1. 获取首页轮播图（APP端）
- **路径**: `/api/system/carousel`
- **方法**: `GET`
- **函数名**: `get_carousel`
- **OpenAPI摘要**: 获取首页轮播图

#### 请求参数
无

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | array | 轮播图URL列表 |

#### 请求示例
```
GET /api/system/carousel
```

#### 响应示例（成功）
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": ["/static/uploads/carousel1.jpg", "/static/uploads/carousel2.jpg"]
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "轮播图配置不存在"
}
```

---

### 2. 获取关于我们页面配置（APP端）
- **路径**: `/api/system/about`
- **方法**: `GET`
- **函数名**: `get_about_config`
- **OpenAPI摘要**: 获取关于我们页面配置

#### 请求参数
无

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 关于我们配置数据 |

#### 请求示例
```
GET /api/system/about
```

#### 响应示例（成功）
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "content": "关于我们的详细介绍...",
        "contact": "contact@example.com"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "关于我们配置不存在"
}
```