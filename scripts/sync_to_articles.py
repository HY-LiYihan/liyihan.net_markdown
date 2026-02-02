#!/usr/bin/env python3
import os
import shutil
import frontmatter
from pathlib import Path

STAGING_DIR = 'staging'
ARTICLES_DIR = 'articles'
PUBLISH_FILE = os.path.join(STAGING_DIR, 'publish.txt')
CATEGORIES = ['Linux', '工具', '开发']

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
        'filename': os.path.basename(filepath),
        'title': title,
        'size': stat.st_size,
        'modified': stat.st_mtime
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
    return sorted(articles, key=lambda x: x['path'])

def interactive_select(articles):
    """交互式选择文章"""
    if not articles:
        print("[INFO] No articles found in staging/")
        return []

    print(f"\nFound {len(articles)} articles in staging/:\n")
    for i, article in enumerate(articles, 1):
        from datetime import datetime
        modified = datetime.fromtimestamp(article['modified']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"[ ] {i}. {article['path']} - {article['title']}")
        print(f"       Size: {article['size']} bytes | Modified: {modified}")

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

def sync_to_articles(mode='all', publish_file=None):
    """同步文章到 articles/"""

    # 1. 确保目标目录存在
    if not os.path.exists(ARTICLES_DIR):
        os.makedirs(ARTICLES_DIR)

    # 2. 获取要发布的文章
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

        all_articles = list_staging_articles()
        selected_articles = [a for a in all_articles if a['path'] in selected_paths]
    else:
        selected_articles = list_staging_articles()

    # 3. 复制到 articles/
    print(f"\n[INFO] Syncing {len(selected_articles)} articles to articles/...")
    for article in selected_articles:
        src = os.path.join(STAGING_DIR, article['path'])
        dst = os.path.join(ARTICLES_DIR, article['filename'])
        shutil.copy2(src, dst)
        print(f"  [+] {article['filename']}")

    # 4. 清空 staging/
    print(f"\n[INFO] Clearing staging/...")
    for article in selected_articles:
        filepath = os.path.join(STAGING_DIR, article['path'])
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"  [-] {article['path']}")

    # 5. 完成
    print(f"\n[OK] {len(selected_articles)} articles synced to articles/")
    print(f"[INFO] Run 'python scripts/create_version.py' to create a new version")

    return True

def main():
    import sys

    mode = 'all'
    publish_file = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == '--select':
            mode = 'select'
        elif arg == '--file':
            if i + 1 < len(sys.argv):
                publish_file = sys.argv[i + 1]
                mode = 'file'
                i += 1

        i += 1

    try:
        success = sync_to_articles(mode, publish_file)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Failed to sync articles: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
