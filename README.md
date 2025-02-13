# 实验室知识管理系统

本课题旨在为科研实验室开发一套Web端知识管理系统，主要包括以下模块：
[1]实验室成果展示板块：展示实验室的科研成果，便于查看和管理。
[2]实验室技术总结帖：供实验室成员发布技术总结和经验分享，促进技术交流。
[3]实验室项目进度管理：帮助管理科研项目进度，任务分配和进度更新。
[4]实验室人员管理：管理实验室成员信息，配置角色与权限。
[5]实验室会议研讨管理：记录会议内容，管理会议安排和议题讨论
一个用于管理实验室知识资产的综合平台，包括成果展示、技术总结等功能。

## 功能特点

- 🔐 用户认证与授权
  - 用户注册、登录
  - JWT token认证
  - 基于角色的权限控制

- 📊 成果管理
  - 成果展示列表
  - 详细信息展示
  - 文件上传与下载
  - 分类筛选与搜索
  - 数据统计

- 💡 技术总结
  - 技术文档管理
  - 标签分类
  - 版本控制

- 🎨 用户界面
  - 响应式设计
  - 现代化UI
  - 良好的用户体验

## 技术栈

### 后端
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Login
- Flask-Migrate
- Flask-CORS

### 前端
- Vue 3
- Vite
- Element Plus
- Pinia
- Vue Router
- Axios

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 8+

### 后端设置
1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 初始化数据库
```bash
flask db upgrade
```

4. 运行开发服务器
```bash
python run.py
```

### 前端设置
1. 安装依赖
```bash
cd frontend
npm install
```

2. 运行开发服务器
```bash
npm run dev
```

## 项目结构
```
.
├── app/                    # 后端应用
│   ├── api/               # API接口
│   ├── models/            # 数据模型
│   ├── routes/            # 路由控制
│   ├── static/            # 静态文件
│   └── templates/         # 模板文件
├── frontend/              # 前端应用
│   ├── src/              
│   │   ├── api/          # API请求
│   │   ├── components/   # 组件
│   │   ├── router/       # 路由配置
│   │   ├── stores/       # 状态管理
│   │   └── views/        # 页面视图
│   └── public/           # 公共资源
└── requirements.txt       # Python依赖
```

## API文档

### 认证接口
- POST `/api/v1/auth/login` - 用户登录
- POST `/api/v1/auth/register` - 用户注册
- POST `/api/v1/auth/refresh` - 刷新token
- GET `/api/v1/auth/me` - 获取当前用户信息

### 成果接口
- GET `/api/v1/achievements` - 获取成果列表
- GET `/api/v1/achievements/<id>` - 获取成果详情
- POST `/api/v1/achievements` - 创建新成果
- PUT `/api/v1/achievements/<id>` - 更新成果
- DELETE `/api/v1/achievements/<id>` - 删除成果

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

项目维护者 - [@yourgithub](https://github.com/yourgithub)

项目链接: [https://github.com/yourusername/your-repo-name](https://github.com/yourusername/your-repo-name)