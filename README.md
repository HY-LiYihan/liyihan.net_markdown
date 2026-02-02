# LiYiHan Knowledge Base

本知识库汇集个人技术笔记与速查手册，访问完整版请至 [liyihan.net](https://liyihan.net)

**作者说明**：文章作者显示为 `HYL` 表示该文章由 AI (OpenCode) 与我协作完成。

---

## 📚 项目简介

这是一个基于版本管理的知识库系统，用于管理和部署 Markdown 格式的技术文章。

**核心特性**：
- ✅ 扁平化文章存储，便于查找和管理
- ✅ 完整版本追踪（CSV + Markdown 双格式）
- ✅ 增量式发布流程
- ✅ 完全自定义分类（通过 Front Matter）
- ✅ Git 友好（staging/ 和 deploy/ 已忽略）

**重要说明**：
- ⚠️ 仅支持增量式发布新文章
- ⚠️ 无法修改已发布的文章
- ⚠️ 如需修改文章，请在 HALO 上删除后重新发布

---

## 📚 快速开始

### 1. 创建新文章

将新文章放到 `staging/` 目录中：

```
staging/
├── your-new-article.md
└── another-article.md
```

**重要**：每个文章必须包含 Front Matter，至少包含以下字段：

```yaml
---
title: 文章标题
slug: article-slug
description: 文章描述
excerpt: 文章摘要
categories:
  - Linux
  - 工具
tags:
  - tag1
  - tag2
---

# 文章内容
```

### 2. 发布文章

```bash
# 方式一：发布所有文章
python scripts/sync_to_articles.py

# 方式二：交互式选择文章
python scripts/sync_to_articles.py --select

# 方式三：从配置文件读取
python scripts/sync_to_articles.py --file staging/publish.txt
```

**交互式选择示例**：
```
Found 3 articles in staging/:

[ ] 1. new-article.md - 新文章标题
[ ] 2. another-article.md - 另一篇文章
[ ] 3. third-article.md - 第三篇文章

Select articles to publish (1-3, separate with spaces): 1 2

Selected: new-article.md, another-article.md
```

### 3. 创建版本

```bash
# 创建版本（自动递增版本号）
python scripts/create_version.py

# 指定版本号
python scripts/create_version.py v2.0
```

### 4. 准备部署

```bash
python scripts/prepare_deploy.py
```

### 5. 上传到 HALO

打开 `deploy/` 文件夹，上传所有文件。

### 6. 提交到 Git

```bash
git add .
git commit -m "version: v1.1 - add X new articles"
```

---

## 📂 目录结构

```
liyihan.net_markdown/
├── README.md                    # 项目说明（本文件）
├── articles/                   # 所有文章（扁平化）
├── versions.csv                # 版本信息（CSV 格式）
├── versions.md                 # 版本信息（Markdown 格式）
├── staging/                   # 新文章暂存区
├── deploy/                    # 部署包
└── scripts/                   # 脚本工具
```

---

## 🔧 脚本使用指南

### sync_to_articles.py

**功能**：将 staging/ 中的文章同步到 articles/

```bash
# 发布所有文章
python scripts/sync_to_articles.py

# 交互式选择文章
python scripts/sync_to_articles.py --select

# 从配置文件读取
python scripts/sync_to_articles.py --file staging/publish.txt
```

**交互式选择示例**：
```
Found 3 articles in staging/:

[ ] 1. new-article.md - 新文章标题
[ ] 2. another-article.md - 另一篇文章
[ ] 3. third-article.md - 第三篇文章

Select articles to publish (1-3, separate with spaces): 1 2

Published: new-article.md, another-article.md
[OK] 2 articles synced to articles/
```

### create_version.py

**功能**：创建新版本，更新版本信息

```bash
# 创建版本（自动递增版本号）
python scripts/create_version.py

# 指定版本号
python scripts/create_version.py v2.0
```

**输出示例**：
```
[INFO] Creating version v1.1...
[INFO] Reading articles from articles/...
[INFO] Found 2 new articles
[INFO] Updating versions.csv...
[INFO] Updating versions.md...
[OK] Version v1.1 created successfully
[INFO] Total articles: 12
[INFO] New articles: 2
[INFO] Run 'python scripts/prepare_deploy.py' to prepare deployment
```

### prepare_deploy.py

**功能**：准备部署包

```bash
python scripts/prepare_deploy.py
```

**输出示例**：
```
[INFO] Preparing deployment for v1.1...
[INFO] Found 12 articles in articles/
  [+] compression-cheatsheet.md
  [+] new-article.md
  [+] another-article.md
  ...

[OK] Deployment package prepared at deploy/
[INFO] Total files: 12
[INFO] Upload all files from deploy/ to HALO
```

---

## 📝 Front Matter 格式

每个文章必须包含 Front Matter，字段说明：

```yaml
---
title: 文章标题          # 必需：显示在列表中的标题
slug: article-slug       # 可选：URL 友好的 slug（默认使用文件名）
description: 文章描述   # 可选：SEO 描述（默认使用 excerpt）
excerpt: 文章摘要        # 可选：简短摘要
categories:              # 必需：分类列表（用于筛选）
  - Linux
  - 工具
tags:                    # 可选：标签列表
  - tag1
  - tag2
---

# 文章内容
```

**注意事项**：
- `categories` 至少需要一个分类
- 分类名称自定义，不限于 Linux、工具、开发
- 文件名建议使用 kebab-case（如 `article-name.md`）

---

## 📦 版本管理

### 查看版本信息

- **CSV 格式**（Excel 可编辑）：[versions.csv](versions.csv)
- **Markdown 格式**（GitHub 可预览）：[versions.md](versions.md)

### 版本命名规则

- 格式：`v{major}.{minor}`
- 例如：v1.0, v1.1, v2.0
- major：重大更新
- minor：小版本更新

### 查找文章历史

在 `versions.csv` 中搜索文章名，查看其版本历史：
- 最初发布的版本
- 最后更新的版本
- 发布日期

---

## 🎯 工作流程总结

```
1. 在 staging/ 中创建新文章
   ↓
2. 运行 sync_to_articles.py（同步到 articles/）
   ↓
3. 运行 create_version.py（创建版本，更新版本信息）
   ↓
4. 运行 prepare_deploy.py（准备部署包）
   ↓
5. 上传 deploy/ 到 HALO
   ↓
6. 提交到 Git
```

---

## ❓ 常见问题

### Q: 为什么只能增量发布新文章？

**A**: 因为 HALO 的限制，无法直接更新已发布的文章。如果需要修改文章，必须在 HALO 上删除后重新发布。

### Q: 如何修改已发布的文章？

**A**: 
1. 在 HALO 上删除原文章
2. 在 staging/ 中创建修改后的文章
3. 按照正常流程发布

### Q: staging/ 和 articles/ 的区别？

**A**:
- **staging/**：新文章的暂存区，不参与版本追踪
- **articles/**：所有已发布文章的最终位置，会被版本追踪

### Q: 如何批量发布文章？

编辑 `staging/publish.txt` 文件：
```
new-article-1.md
new-article-2.md
new-article-3.md
```

然后运行：
```bash
python scripts/sync_to_articles.py --file staging/publish.txt
```

### Q: 如何自定义分类？

在 Front Matter 的 `categories` 字段中定义：
```yaml
---
categories:
  - 数据科学
  - Web 开发
  - 自动化
---
```

---

## 📊 统计信息

查看完整统计请访问 [liyihan.net](https://liyihan.net)

---

## 🔒 安全说明

- `staging/` 和 `deploy/` 已添加到 `.gitignore`
- 只提交 `articles/`、`scripts/`、版本文件
- 避免重复上传和版本混乱

---

## ⚠️ 重要提醒

1. **增量式发布**：本系统仅支持新增文章，不支持修改已发布的文章
2. **文章修改**：如需修改文章，请在 HALO 上删除后重新发布
3. **版本追踪**：每次发布都会记录版本信息，便于追溯
4. **作者标识**：文章作者显示为 `HYL` 表示由 AI (OpenCode) 协作完成

---

*本项目使用版本管理系统，便于文章追踪和部署*
