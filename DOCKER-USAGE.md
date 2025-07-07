# Docker 使用说明

## 📦 概述

这个项目已经优化了 Docker 配置，去掉了不必要的 VNC/noVNC 功能，专注于提供一个简洁的 Web UI 服务。

## 🚀 快速开始

### 1. 使用 Docker Compose 启动（推荐）

```bash
# 克隆项目
git clone https://github.com/yourkin666/my-browser-use-webui.git
cd my-browser-use-webui

# 配置环境变量（复制示例文件）
cp .env.example .env

# 编辑 .env 文件，添加您的 API 密钥
nano .env

# 启动服务
docker-compose up -d
```

### 2. 使用 Docker 直接构建

```bash
# 构建镜像
docker build -t browser-use-webui .

# 运行容器
docker run -d \
  -p 7788:7788 \
  -e SILICONFLOW_API_KEY=your_api_key_here \
  -e SILICONFLOW_ENDPOINT=https://api.siliconflow.cn/v1/ \
  -v $(pwd)/tmp:/app/tmp \
  -v $(pwd)/data:/app/data \
  --name browser-use-webui \
  browser-use-webui
```

## 🔧 配置

### 环境变量

在 `.env` 文件中配置以下变量：

```bash
# 硅基流动 API 配置
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
SILICONFLOW_ENDPOINT=https://api.siliconflow.cn/v1/

# 其他LLM提供商（可选）
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 端口

- **7788**: Web UI 访问端口

### 数据持久化

```bash
# 自动创建的数据目录
./tmp/     # 临时文件和下载
./data/    # 持久化数据
```

## 🌐 访问

启动后，在浏览器中访问：

- Web UI: http://localhost:7788

## 📋 功能特性

- ✅ **简化配置**: 去掉复杂的 VNC 设置
- ✅ **Web UI**: 基于 Gradio 的现代界面
- ✅ **多 LLM 支持**: 支持硅基流动、OpenAI、Anthropic 等
- ✅ **浏览器代理**: 内置 Playwright 浏览器
- ✅ **数据持久化**: 自动保存代理历史和下载文件
- ✅ **健康检查**: 自动监控服务状态

## 🛠️ 故障排除

### 1. 容器启动失败

```bash
# 查看日志
docker-compose logs -f browser-use-webui

# 或者
docker logs browser-use-webui
```

### 2. API 密钥错误

确保在 `.env` 文件中正确配置了 API 密钥：

```bash
# 检查环境变量
docker-compose exec browser-use-webui env | grep API_KEY
```

### 3. 端口冲突

如果 7788 端口被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8080:7788" # 改为其他端口
```

## 🔄 更新

```bash
# 停止服务
docker-compose down

# 拉取最新代码
git pull origin main

# 重新构建并启动
docker-compose up -d --build
```

## 💡 优化建议

1. **资源限制**: 根据需要调整 `shm_size` 和内存限制
2. **网络配置**: 在生产环境中配置适当的网络安全策略
3. **日志管理**: 配置日志轮转以避免磁盘空间问题
4. **监控**: 使用健康检查功能监控服务状态
