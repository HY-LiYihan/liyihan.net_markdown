#!/usr/bin/env python3
import os
import shutil
import yaml
from datetime import datetime
import frontmatter
from pathlib import Path

VERSION_FILE = 'VERSION'
STAGING_DIR = 'staging'
VERSIONS_DIR = 'versions'
CHANGELOG_FILE = 'changelog.md'
CATEGORIES = ['Linux', '工具', '开发']

def read_current_version():
    """读取当前版本号"""
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE, 'r') as f:
        return f.read().strip()

def get_previous_version(version):
    """获取上一个版本号"""
    parts = version.split('.')
    if len(parts) != 2:
        return None
    major, minor = int(parts[0][1:]), int(parts[1])
    if minor == 0:
        return None
    return f"v{major}.{minor-1}"

def get_file_title(filepath):
    """从 Markdown 文件读取标题"""
    try:
        post = frontmatter.load(filepath)
        return post.get('title', Path(filepath).stem)
    except:
        return Path(filepath).stem

def get_file_info(filepath):
    """获取文件信息"""
    stat = os.stat(filepath)
    title = get_file_title(filepath)
    rel_path = os.path.relpath(filepath, STAGING_DIR)
    return {
        'path': rel_path,
        'title': title,
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    }

def list_staging_articles():
    """列出 staging 中的所有文章"""
    articles = []
    for category in CATEGORIES:
        category_dir = os.path.join(STAGING_DIR, category)
        if os.path.exists(category_dir):
            for file in os.listdir(category_dir):
                if file.endswith('.md'):
                    filepath = os.path.join(category_dir, file)
                    articles.append(get_file_info(filepath))
    return articles

def interactive_select(articles):
    """交互式选择文章"""
    if not articles:
        print("[INFO] No articles found in staging/")
        return []

    print(f"\nFound {len(articles)} articles in staging/:\n")
    for i, article in enumerate(articles, 1):
        print(f"[ ] {i}. {article['path']} - {article['title']}")
        print(f"       Size: {article['size']} bytes | Modified: {article['modified']}")

    print("\nSelect articles to publish (1-{}, separate with spaces):".format(len(articles)), end=" ")
    try:
        input_str = input()
        if not input_str.strip():
            print("[INFO] No articles selected")
            return []

        indices = [int(x.strip()) - 1 for x in input_str.split()]
        indices = [i for i in indices if 0 <= i < len(articles)]

        if not indices:
            print("[INFO] Invalid selection")
            return []

        selected = [articles[i] for i in indices]
        print(f"\nSelected:")
        for article in selected:
            print(f"  - {article['path']}")

        return selected
    except (ValueError, KeyboardInterrupt):
        print("\n[INFO] Selection cancelled")
        return []

def read_publish_list(publish_file):
    """从配置文件读取发布列表"""
    if not os.path.exists(publish_file):
        return []

    selected_paths = []
    with open(publish_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                selected_paths.append(line)

    return selected_paths

def create_version(version=None, mode='all', publish_file=None):
    """创建新版本"""

    # 1. 确定版本号
    if version is None:
        current_version = read_current_version()
        if current_version:
            parts = current_version.split('.')
            major, minor = int(parts[0][1:]), int(parts[1])
            version = f"v{major}.{minor+1}"
        else:
            version = "v1.0"

    print(f"[INFO] Creating version {version}...")

    # 2. 检查版本是否已存在
    version_dir = os.path.join(VERSIONS_DIR, version)
    if os.path.exists(version_dir):
        print(f"[ERROR] Version {version} already exists")
        return False

    # 3. 获取要发布的文章
    selected_articles = None

    if mode == 'select':
        articles = list_staging_articles()
        selected_articles = interactive_select(articles)
        if not selected_articles:
            return False
    elif mode == 'file' and publish_file:
        selected_paths = read_publish_list(publish_file)
        if not selected_paths:
            print("[INFO] No articles in publish list")
            return False

        # 根据 publish.txt 获取文章信息
        all_articles = list_staging_articles()
        selected_articles = [a for a in all_articles if a['path'] in selected_paths]
    else:
        # 默认：所有文章
        selected_articles = list_staging_articles()

    # 4. 创建版本目录
    os.makedirs(version_dir, exist_ok=True)

    # 5. 复制上一个版本的内容
    previous_version = get_previous_version(version)
    if previous_version and os.path.exists(os.path.join(VERSIONS_DIR, previous_version)):
        print(f"[INFO] Copying from {previous_version}...")
        for category in CATEGORIES:
            src_dir = os.path.join(VERSIONS_DIR, previous_version, category)
            dst_dir = os.path.join(version_dir, category)
            if os.path.exists(src_dir):
                shutil.copytree(src_dir, dst_dir)

    # 6. 合并选中的文章
    print(f"[INFO] Merging selected articles from staging/...")
    for article in selected_articles:
        src = os.path.join(STAGING_DIR, article['path'])
        dst = os.path.join(version_dir, article['path'])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  [+] {article['path']}")

    # 7. 统计文章数量
    total_articles = 0
    for category in CATEGORIES:
        category_dir = os.path.join(version_dir, category)
        if os.path.exists(category_dir):
            total_articles += len([f for f in os.listdir(category_dir) if f.endswith('.md')])

    # 8. 生成版本信息
    version_info = {
        'version': version,
        'created_at': datetime.now().isoformat(),
        'total_articles': total_articles,
        'previous_version': previous_version
    }

    version_info_path = os.path.join(version_dir, 'version_info.yaml')
    with open(version_info_path, 'w', encoding='utf-8') as f:
        yaml.dump(version_info, f, allow_unicode=True)

    # 9. 更新 VERSION 文件
    with open(VERSION_FILE, 'w') as f:
        f.write(version)

    # 10. 清空 staging/ 中的已发布文章
    print(f"[INFO] Clearing published articles from staging/...")
    remaining_count = 0
    for article in selected_articles:
        filepath = os.path.join(STAGING_DIR, article['path'])
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"  [-] {article['path']}")

    # 统计剩余文章
    for category in CATEGORIES:
        category_dir = os.path.join(STAGING_DIR, category)
        if os.path.exists(category_dir):
            remaining_count += len([f for f in os.listdir(category_dir) if f.endswith('.md')])

    # 11. 更新 changelog
    changelog_entry = f"\n## {version} ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    changelog_entry += f"### 新增文章 ({len(selected_articles)} 篇)\n"
    for article in selected_articles:
        changelog_entry += f"- [{article['path']}] - {article['title']}\n"
    changelog_entry += f"\n### 统计\n"
    changelog_entry += f"- 总文章数: {total_articles} 篇\n"
    if remaining_count > 0:
        changelog_entry += f"- Staging 中剩余: {remaining_count} 篇\n"

    with open(CHANGELOG_FILE, 'a', encoding='utf-8') as f:
        f.write(changelog_entry)

    # 12. 完成
    print(f"\n[OK] Version {version} created successfully")
    print(f"[INFO] Total articles: {total_articles}")
    print(f"[INFO] Published: {len(selected_articles)} articles")
    if remaining_count > 0:
        print(f"[INFO] Staging 中剩余: {remaining_count} articles")
        print(f"[INFO] Run 'python scripts/select_articles.py --list' to view remaining articles")
    print(f"[INFO] Run 'python scripts/prepare_deploy.py' to prepare deployment")

    return True

def main():
    import sys

    # 解析命令行参数
    version = None
    mode = 'all'
    publish_file = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if not arg.startswith('--'):
            # 版本号
            if not version:
                version = arg
        elif arg == '--select':
            mode = 'select'
        elif arg == '--file':
            if i + 1 < len(sys.argv):
                publish_file = sys.argv[i + 1]
                mode = 'file'
                i += 1

        i += 1

    try:
        success = create_version(version, mode, publish_file)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Failed to create version: {e}")
        print("[INFO] Staging directory remains unchanged")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
