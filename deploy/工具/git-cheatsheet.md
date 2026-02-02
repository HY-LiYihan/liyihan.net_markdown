---
title: Git 速查手册
slug: git-cheatsheet
description: Git 版本控制系统的快速参考指南，包含基本命令、分支管理和常用工作流
excerpt: 掌握 Git 版本控制的核心命令
categories:
  - 工具
  - 版本控制
tags:
  - git
  - version-control
  - 速查手册
---

## Git 基础配置

### 初始化和配置
```bash
# 初始化仓库
git init

# 克隆仓库
git clone <repository-url>

# 克隆特定分支
git clone -b <branch-name> <repository-url>

# 配置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 配置编辑器
git config --global core.editor "vim"

# 查看配置
git config --list
```

---

## 基本操作

### 工作区、暂存区、仓库
```
工作区 (Working Directory) → 暂存区 (Staging Area) → 仓库 (Repository)
```

### 查看状态
```bash
# 查看当前状态
git status

# 查看简洁状态
git status -s
```

### 添加和提交
```bash
# 添加文件到暂存区
git add <filename>

# 添加所有修改
git add .

# 添加所有修改（包括删除的文件）
git add -A

# 提交更改
git commit -m "commit message"

# 添加并提交
git commit -am "commit message"

# 修改最后一次提交
git commit --amend
git commit --amend -m "new message"
```

### 查看历史
```bash
# 查看提交历史
git log

# 查看简洁历史
git log --oneline

# 查看图表历史
git log --graph --oneline --all

# 查看文件历史
git log -p <filename>

# 查看最近 n 次提交
git log -n 3
```

---

## 分支管理

### 分支操作
```bash
# 查看所有分支
git branch

# 查看远程分支
git branch -r

# 查看所有分支（本地和远程）
git branch -a

# 创建新分支
git branch <branch-name>

# 切换分支
git checkout <branch-name>
git switch <branch-name>

# 创建并切换分支
git checkout -b <branch-name>
git switch -c <branch-name>

# 删除分支
git branch -d <branch-name>

# 强制删除分支
git branch -D <branch-name>

# 重命名分支
git branch -m <old-name> <new-name>
```

### 分支合并
```bash
# 合并分支到当前分支
git merge <branch-name>

# 变基分支到当前分支
git rebase <branch-name>

# 终止变基
git rebase --abort

# 继续变基
git rebase --continue
```

---

## 远程操作

### 远程仓库
```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add <name> <url>

# 删除远程仓库
git remote remove <name>

# 更改远程仓库 URL
git remote set-url <name> <new-url>
```

### 推送和拉取
```bash
# 推送到远程仓库
git push

# 推送到特定远程和分支
git push <remote> <branch>

# 推送所有分支
git push --all

# 删除远程分支
git push <remote> --delete <branch>

# 拉取远程更新
git pull

# 拉取远程更新（不合并）
git fetch

# 拉取并变基
git pull --rebase
```

---

## 撤销操作

### 撤销工作区修改
```bash
# 撤销文件修改
git checkout -- <filename>
git restore <filename>

# 撤销所有修改
git checkout .
git restore .
```

### 撤销暂存区
```bash
# 取消暂存文件
git reset <filename>
git restore --staged <filename>

# 取消所有暂存
git reset
```

### 撤销提交
```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最后一次提交（取消暂存）
git reset HEAD~1

# 撤销最后一次提交（丢弃修改）
git reset --hard HEAD~1

# 撤销到指定提交
git reset --hard <commit-hash>

# 创建反向提交
git revert HEAD
```

---

## 文件操作

### 文件追踪
```bash
# 删除文件
git rm <filename>

# 删除暂存区文件（保留工作区文件）
git rm --cached <filename>

# 移动/重命名文件
git mv <old-name> <new-name>
```

### 忽略文件 (.gitignore)
```bash
# 创建 .gitignore 文件
touch .gitignore

# 常用规则
node_modules/
*.log
.DS_Store
.env
build/
dist/

# 例外规则
*.log
!important.log
```

---

## 标签管理

### 标签操作
```bash
# 创建轻量标签
git tag <tag-name>

# 创建附注标签
git tag -a <tag-name> -m "tag message"

# 删除标签
git tag -d <tag-name>

# 推送标签到远程
git push <remote> <tag-name>

# 推送所有标签
git push <remote> --tags

# 查看标签
git tag
git show <tag-name>
```

---

## 差异比较

### 查看差异
```bash
# 查看工作区与暂存区的差异
git diff

# 查看暂存区与仓库的差异
git diff --staged
git diff --cached

# 查看工作区与仓库的差异
git diff HEAD

# 查看两次提交的差异
git diff <commit1> <commit2>

# 查看文件的差异
git diff <filename>

# 查看特定提交的更改
git show <commit-hash>
```

---

## 储藏操作

### 储藏和恢复
```bash
# 储藏当前工作
git stash

# 储藏并添加消息
git stash save "message"

# 查看储藏列表
git stash list

# 应用最新储藏
git stash apply
git stash pop

# 应用特定储藏
git stash apply stash@{0}

# 删除储藏
git stash drop stash@{0}

# 删除所有储藏
git stash clear
```

---

## 常用工作流

### Feature Branch 工作流
```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发和提交
git add .
git commit -m "Add new feature"

# 3. 推送功能分支
git push -u origin feature/new-feature

# 4. 创建 Pull Request

# 5. 合并后删除分支
git checkout main
git pull
git branch -d feature/new-feature
```

### Git Flow 工作流
```bash
# 安装 git-flow
# macOS: brew install git-flow-avh
# Ubuntu: apt install git-flow

# 初始化
git flow init

# 开始新功能
git flow feature start my-feature

# 完成功能
git flow feature finish my-feature

# 开始发布
git flow release start v1.0.0

# 完成发布
git flow release finish v1.0.0
```

---

## 实用技巧

### 查找提交
```bash
# 查找包含特定文本的提交
git log --grep="keyword"

# 查找修改特定文件的提交
git log -- <filename>

# 查找特定作者的提交
git log --author="name"

# 查找特定日期范围的提交
git log --since="2024-01-01" --until="2024-12-31"
```

### 变基技巧
```bash
# 交互式变基（修改历史）
git rebase -i HEAD~3

# 选择操作：
# pick: 保留提交
# reword: 修改提交信息
# edit: 编辑提交
# squash: 合并提交
# drop: 删除提交
```

### 子模块
```bash
# 添加子模块
git submodule add <repository-url>

# 更新子模块
git submodule update --init --recursive

# 拉取子模块
git submodule foreach git pull origin main
```

---

## 故障排查

### 常见问题
```bash
# 解决合并冲突
git status
# 编辑冲突文件
git add <conflicted-file>
git commit

# 放弃合并
git merge --abort

# 清理未追踪文件
git clean -fd

# 查看远程跟踪状态
git branch -vv

# 同步远程分支
git fetch --prune
```
