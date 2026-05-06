# CodeSearchProject 代码搜索平台

基于Sanic后端 + Vue3移动端的代码搜索与内容分享平台。

## 技术栈

### 后端
- Python 3.12.13 / Sanic 25.12.0
- SQLAlchemy 2.0.49 / PyMySQL 1.1.2
- Sanic-Cors / sanic-ext / sanic-openapi
- 阿里云OSS存储

### 前端（App）
- Vue 3.5.32 / Vite 8.0.10
- Vant 4.9.24（移动端UI框架）
- Vue Router 4.6.4

### 管理后台
- Layui / EasyMDE / ECharts

## 项目结构

```
CodeSearchProject/
├── App/                    # Vue3移动端应用
│   ├── src/
│   │   ├── assets/         # 静态资源（API封装等）
│   │   ├── router/         # 路由配置
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 公共组件（RankingItem/UserListItem/PostCard/PageNavBar）
│   │   ├── main.js         # 入口文件
│   │   ├── App.vue         # 根组件
│   │   └── style.css       # 全局样式
│   ├── package.json
│   └── vite.config.js
├── router/                 # Sanic路由模块
│   ├── admin_router/       # 管理后台API（17个路由文件）
│   ├── app_router/         # 移动端API（12个路由文件）
│   ├── upload_router.py    # 文件上传路由
│   └── log_router.py       # 前端日志路由
├── models/                 # SQLAlchemy数据模型
├── template/               # HTML模板
│   ├── admin/              # 管理后台页面（含dialogs子目录）
│   └── index.html          # 首页
├── static/                 # 静态资源
│   ├── webs/               # 前端库（Layui/ECharts/EasyMDE/Vanta等）
│   ├── mds/                # 项目文档
│   └── uploads/            # 上传文件
├── utils/                  # 工具类（oss_option/password_analysis）
├── test/                   # 测试模块
├── config.py               # 配置文件
└── app.py                  # 应用入口
```

## 数据库模型

| 模型 | 说明 |
|------|------|
| User | 用户表 |
| Post | 文章表 |
| Category | 分类表 |
| Tag | 标签表 |
| PostTag | 文章标签关联表 |
| Comment | 评论表 |
| Favorite | 收藏表 |
| Like | 点赞表 |
| Follow | 关注表 |
| Message | 私信表 |
| SystemMessage | 系统消息表 |
| SystemMessageTarget | 系统消息目标表 |
| Report | 举报表 |
| File | 文件表 |
| SearchHistory | 搜索历史表 |
| SystemSetting | 系统设置表 |
| Notification | 通知表 |

## 快速开始

### 环境要求
- Python 3.12.13
- Node.js 18+
- MySQL 8.0+

### 后端启动
```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
后端服务运行在 `http://localhost:8848`

### 前端启动
```bash
cd App
npm install
npm run dev
```
前端开发服务器运行在 `http://localhost:5173`

## API文档

通过 `/docs` 路径访问Sanic OpenAPI文档。

## 许可证

MIT
