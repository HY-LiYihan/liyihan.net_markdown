---
title: GNU Screen 速查手册
slug: gnu-screen-cheatsheet
description: Linux 下 GNU Screen 终端复用器的快速参考指南，包含基本用法和常用命令
excerpt: Screen 是一款强大的终端复用工具，本文提供快速参考指南
categories:
  - Linux
  - 终端工具
tags:
  - screen
  - 终端
  - 速查手册
  - CLI
---

# GNU Screen 速查手册

## 安装
- Ubuntu/Debian: `sudo apt install screen`
- CentOS/RHEL: `sudo yum install screen`
- macOS: `brew install screen`

## 基本概念
- Screen 是一个终端复用器，可以在单个终端窗口中创建多个会话
- 支持会话持久化，SSH 断开后会话仍然运行
- 可以在不同窗口间切换

## 常用命令速查

### 会话管理
| 命令 | 说明 |
|------|------|
| `screen` | 创建新会话 |
| `screen -S name` | 创建命名会话 |
| `screen -ls` | 列出所有会话 |
| `screen -r` | 恢复最近会话 |
| `screen -r name` | 恢复指定会话 |
| `screen -d -r name` | 分离并恢复会话 |
| `screen -X -S name quit` | 关闭指定会话 |

### 快捷键（Ctrl+a 前缀）
| 快捷键 | 说明 |
|--------|------|
| `Ctrl+a c` | 创建新窗口 |
| `Ctrl+a n` | 切换到下一个窗口 |
| `Ctrl+a p` | 切换到上一个窗口 |
| `Ctrl+a 0-9` | 切换到指定窗口 |
| `Ctrl+a d` | 分离当前会话 |
| `Ctrl+a k` | 关闭当前窗口 |
| `Ctrl+a A` | 重命名当前窗口 |
| `Ctrl+a [` | 进入复制模式 |
| `Ctrl+a ]` | 粘贴内容 |

## 实用示例

### 创建持久化任务
```bash
# 创建命名会话
screen -S work

# 在会话中运行长时间任务
./long-running-script.sh

# 分离会话（Ctrl+a d）
# 任务会继续在后台运行
```

### 恢复会话
```bash
# 查看所有会话
screen -ls

# 恢复会话
screen -r work
```

### 多窗口操作
```bash
# 创建新窗口
Ctrl+a c

# 在窗口1运行服务
python server.py

# 创建新窗口2
Ctrl+a c

# 在窗口2运行测试
pytest tests/

# 切换窗口
Ctrl+a n  # 下一个
Ctrl+a p  # 上一个
Ctrl+a 0  # 窗口0
```
