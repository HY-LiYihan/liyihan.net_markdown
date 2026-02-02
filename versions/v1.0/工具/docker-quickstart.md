---
title: Docker 快速入门
slug: docker-quickstart
description: Docker 容器技术的快速入门指南，包含基本概念、常用命令和 Dockerfile 示例
excerpt: 快速掌握 Docker 容器化技术
categories:
  - 工具
  - 容器化
tags:
  - docker
  - container
  - devops
  - 速查手册
---

## Docker 基本概念

### 核心概念
- **镜像 (Image)**: 只读的模板，包含运行应用所需的所有内容
- **容器 (Container)**: 镜像的运行实例，可以启动、停止、删除
- **仓库 (Registry)**: 存储和分发镜像的服务（如 Docker Hub）
- **Dockerfile**: 用于构建 Docker 镜像的文本文件

### Docker 架构
```
客户端 (Client) ←→ 守护进程 (Daemon) ←→ 镜像/容器
```

---

## 安装 Docker

### Ubuntu/Debian
```bash
# 更新包索引
sudo apt update

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 添加用户到 docker 组
sudo usermod -aG docker $USER

# 重启或重新登录
newgrp docker

# 验证安装
docker --version
docker run hello-world
```

### CentOS/RHEL
```bash
# 安装 Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
docker run hello-world
```

### macOS
```bash
# 使用 Homebrew
brew install --cask docker

# 或下载 Docker Desktop for Mac
# https://www.docker.com/products/docker-desktop
```

---

## 镜像操作

### 搜索和下载镜像
```bash
# 搜索镜像
docker search nginx
docker search python

# 下载镜像
docker pull nginx:latest
docker pull python:3.9

# 查看本地镜像
docker images
docker image ls

# 删除镜像
docker rmi nginx
docker image rm python:3.9
```

### 构建镜像
```bash
# 构建镜像
docker build -t myapp:1.0 .

# 构建时指定 Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# 查看镜像详情
docker inspect nginx

# 导出/导入镜像
docker save -o nginx.tar nginx:latest
docker load -i nginx.tar
```

---

## 容器操作

### 运行容器
```bash
# 基本运行
docker run nginx

# 后台运行
docker run -d nginx

# 指定端口映射
docker run -p 8080:80 nginx

# 指定名称
docker run --name mynginx nginx

# 指定环境变量
docker run -e ENV=production nginx

# 挂载卷
docker run -v /host/path:/container/path nginx

# 交互式运行
docker run -it ubuntu bash
docker run -it --rm alpine sh
```

### 管理容器
```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 查看容器日志
docker logs mynginx
docker logs -f mynginx

# 查看容器详细信息
docker inspect mynginx

# 进入运行中的容器
docker exec -it mynginx bash

# 停止容器
docker stop mynginx

# 启动容器
docker start mynginx

# 重启容器
docker restart mynginx

# 删除容器
docker rm mynginx

# 强制删除运行中的容器
docker rm -f mynginx
```

### 容器资源管理
```bash
# 限制内存
docker run -m 512m nginx

# 限制 CPU
docker run --cpus=2 nginx

# 查看容器资源使用
docker stats

# 查看容器进程
docker top mynginx
```

---

## Dockerfile 编写

### 基础 Dockerfile
```dockerfile
# 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "app.py"]
```

### 常用指令
```dockerfile
# FROM: 指定基础镜像
FROM ubuntu:20.04

# WORKDIR: 设置工作目录
WORKDIR /app

# COPY: 复制文件到容器
COPY . /app
COPY --from=builder /app/dist /app

# ADD: 复制文件（支持 URL 和解压）
ADD https://example.com/file.tar.gz /app/

# RUN: 执行命令
RUN apt-get update && apt-get install -y python3
RUN pip install -r requirements.txt

# CMD: 容器启动时执行的命令
CMD ["python", "app.py"]
CMD python app.py

# ENTRYPOINT: 容器启动时执行的命令（可被 CMD 覆盖）
ENTRYPOINT ["python"]
CMD ["app.py"]

# ENV: 设置环境变量
ENV APP_ENV=production
ENV PORT=8000

# ARG: 构建时的变量
ARG VERSION=1.0
ENV VERSION=$ARG

# EXPOSE: 暴露端口
EXPOSE 8000

# VOLUME: 声明挂载点
VOLUME /data
```

### 多阶段构建
```dockerfile
# 构建阶段
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 运行阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Docker Compose

### 基础使用
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=true
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 常用命令
```bash
# 启动所有服务
docker-compose up

# 后台启动
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看日志
docker-compose logs

# 查看特定服务的日志
docker-compose logs -f web

# 重启服务
docker-compose restart web

# 构建服务
docker-compose build

# 构建并启动
docker-compose up -d --build

# 进入容器
docker-compose exec web bash

# 执行命令
docker-compose exec web python manage.py migrate
```

---

## 网络管理

### 查看和管理网络
```bash
# 查看网络
docker network ls

# 创建网络
docker network create mynetwork

# 连接容器到网络
docker network connect mynetwork mycontainer

# 断开容器连接
docker network disconnect mynetwork mycontainer

# 删除网络
docker network rm mynetwork
```

### 创建自定义网络
```bash
# 创建桥接网络
docker network create --driver bridge mynetwork

# 创建 overlay 网络（用于 Swarm）
docker network create --driver overlay mynetwork

# 指定子网
docker network create --subnet 192.168.0.0/16 mynetwork
```

---

## 实用示例

### Python Web 应用
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Node.js 应用
```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### Nginx 反向代理
```dockerfile
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## 数据管理

### 数据卷
```bash
# 创建数据卷
docker volume create mydata

# 查看数据卷
docker volume ls

# 查看数据卷详情
docker volume inspect mydata

# 删除数据卷
docker volume rm mydata

# 删除未使用的数据卷
docker volume prune
```

### 绑定挂载
```bash
# 挂载主机目录
docker run -v /host/path:/container/path nginx

# 只读挂载
docker run -v /host/path:/container/path:ro nginx

# 挂载数据卷
docker run -v mydata:/data nginx
```

---

## 最佳实践

### 1. 镜像优化
```dockerfile
# 使用多阶段构建减小镜像大小
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --production
EXPOSE 3000
CMD ["npm", "start"]
```

### 2. 缓存优化
```dockerfile
# 先复制依赖文件，再复制代码
FROM python:3.9
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

### 3. 安全实践
```bash
# 使用非 root 用户
FROM python:3.9
RUN useradd -m myuser
USER myuser

# 使用最小的基础镜像
FROM alpine:3.14

# 定期更新基础镜像
docker pull python:3.9
```

---

## 故障排查

### 常见问题
```bash
# 查看容器日志
docker logs <container_id>

# 查看容器详细信息
docker inspect <container_id>

# 进入容器调试
docker exec -it <container_id> sh

# 查看容器资源使用
docker stats <container_id>

# 重新构建镜像
docker build --no-cache -t myapp .
```

### 清理系统
```bash
# 清理停止的容器
docker container prune

# 清理未使用的镜像
docker image prune

# 清理未使用的网络
docker network prune

# 清理所有未使用的资源
docker system prune -a
```
