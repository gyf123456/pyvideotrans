# pyVideoTrans Web 前端

Vue3 + Element Plus + TypeScript 构建的 Web 前端，完整复刻桌面版 GUI 功能。

## 环境要求

- Node.js >= 18
- Python >= 3.10（后端）
- uv（Python 包管理）

## 安装依赖

```bash
# 前端依赖
cd web
npm install

# 后端依赖（项目根目录）
cd ..
uv sync
```

## 开发模式

需要同时启动前端开发服务器和后端 API 服务器。

### 1. 启动后端

```bash
# 在项目根目录
uv run python web_api.py
```

后端运行在 http://localhost:9011

### 2. 启动前端开发服务器

```bash
# 在 web/ 目录
cd web
npm run dev
```

前端运行在 http://localhost:5173，API 请求自动代理到后端 9011 端口。

打开浏览器访问 **http://localhost:5173**

## 生产模式

构建前端静态文件后，由后端 FastAPI 统一托管，只需启动一个服务。

### 1. 构建前端

```bash
cd web
npm run build
```

构建产物输出到 `web/dist/`。

### 2. 启动服务

```bash
# 在项目根目录
uv run python web_api.py
```

打开浏览器访问 **http://localhost:9011**

### 自定义主机和端口

```bash
uv run python web_api.py --host 0.0.0.0 --port 8080
```

## 目录结构

```
web/
├── src/
│   ├── api/          # Axios 请求封装
│   ├── stores/       # Pinia 状态管理
│   ├── composables/  # 组合式函数（WebSocket 等）
│   ├── types/        # TypeScript 类型定义
│   ├── i18n/         # 中英文国际化
│   ├── data/         # 服务商字段定义（数据驱动）
│   ├── layouts/      # 页面布局
│   ├── views/        # 页面视图（工作区/任务列表/设置）
│   └── components/   # UI 组件
│       ├── workspace/  # 工作区组件
│       ├── settings/   # 设置组件
│       ├── tasks/      # 任务组件
│       └── common/     # 通用组件
└── dist/             # 构建产物（git 忽略）
```
