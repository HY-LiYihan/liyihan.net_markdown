#!/usr/bin/env python3
import os
import shutil
import frontmatter
import csv
from pathlib import Path
from datetime import datetime

VERSION_FILE = 'VERSION'
ARTICLES_DIR = 'articles'
VERSIONS_CSV = 'versions.csv'
VERSIONS_MD = 'versions.md'

def read_current_version():
    """读取当前版本号"""
    if not os.path.exists(VERSION_FILE):
        return "v0.0"
    with open(VERSION_FILE, 'r') as f:
        return f.read().strip()

def increment_version(version):
    """递增版本号"""
    if not version:
        return "v1.0"

    parts = version.split('.')
    if len(parts) != 2:
        return version

    major = int(parts[0][1:])
    minor = int(parts[1])
    return f"v{major}.{minor+1}"

def get_file_info(filepath):
    """获取文件信息"""
    try:
        post = frontmatter.load(filepath)
        stat = os.stat(filepath)
        return {
            'filename': os.path.basename(filepath),
            'title': post.get('title', Path(filepath).stem),
            'description': post.get('description', ''),
            'excerpt': post.get('excerpt', ''),
            'categories': '|'.join(post.get('categories', [])),
            'tags': '|'.join(post.get('tags', [])),
            'slug': post.get('slug', ''),
            'size': stat.st_size
        }
    except Exception as e:
        print(f"[WARNING] Failed to parse {filepath}: {e}")
        return None

def scan_articles():
    """扫描 articles/ 中的所有文章"""
    articles = []
    if not os.path.exists(ARTICLES_DIR):
        return articles

    for file in os.listdir(ARTICLES_DIR):
        if file.endswith('.md'):
            filepath = os.path.join(ARTICLES_DIR, file)
            info = get_file_info(filepath)
            if info:
                articles.append(info)

    return sorted(articles, key=lambda x: x['filename'])

def read_versions_csv():
    """读取 versions.csv"""
    if not os.path.exists(VERSIONS_CSV):
        return {}

    versions = {}
    with open(VERSIONS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            versions[row['article_path']] = row

    return versions

def write_versions_csv(records):
    """写入 versions.csv"""
    fieldnames = ['article_path', 'version', 'published_at', 'is_deployed', 'title', 'description', 'excerpt', 'category', 'tags', 'slug']

    with open(VERSIONS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def generate_versions_md(new_articles, version, published_at):
    """生成 versions.md"""
    from collections import defaultdict
    articles_by_category = defaultdict(list)

    for article in new_articles:
        categories = article.get('categories', '').split('|')
        if categories:
            articles_by_category[categories[0]].append(article)

    md_content = "# 版本信息\n\n"
    md_content += "本文档记录每篇文章的版本信息和发布历史。\n\n"
    md_content += f"## {version} ({published_at.strftime('%Y-%m-%d')})\n\n"

    # 按分类分组显示
    for category, articles in sorted(articles_by_category.items()):
        md_content += f"### {category}\n"
        for article in sorted(articles, key=lambda x: x['filename']):
            md_content += f"- [{article['filename']}]({ARTICLES_DIR}/{article['filename']}) - {article['title']}\n"
        md_content += "\n"

    md_content += "---\n"
    md_content += f"总文章数：{len(new_articles)} 篇\n"

    # 读取并追加之前的版本
    if os.path.exists(VERSIONS_MD):
        with open(VERSIONS_MD, 'r', encoding='utf-8') as f:
            old_content = f.read()

        # 提取旧内容（跳过标题部分）
        lines = old_content.split('\n')
        start_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('## ') and start_idx == 0:
                start_idx = i

        if start_idx > 0:
            md_content += "\n" + '\n'.join(lines[start_idx:])

    return md_content

def create_version(version=None):
    """创建新版本"""

    # 1. 确定版本号
    current_version = read_current_version()
    new_version = version or increment_version(current_version)

    print(f"[INFO] Creating version {new_version}...")

    # 2. 扫描文章
    articles = scan_articles()
    if not articles:
        print("[INFO] No articles found in articles/")
        return False

    # 3. 读取现有版本信息
    versions_dict = read_versions_csv()
    published_at = datetime.now()

    # 4. 确定新文章
    new_articles = []
    for article in articles:
        filename = article['filename']
        if filename not in versions_dict or versions_dict[filename].get('version') != new_version:
            new_articles.append(article)

    if not new_articles:
        print(f"[INFO] No new articles for version {new_version}")
        return False

    # 5. 更新版本信息
    new_records = []
    for article in new_articles:
        record = {
            'article_path': article['filename'],
            'version': new_version,
            'published_at': published_at.strftime('%Y-%m-%d'),
            'is_deployed': 'False',
            'title': article['title'],
            'description': article['description'],
            'excerpt': article['excerpt'],
            'category': article['categories'],
            'tags': article['tags'],
            'slug': article['slug']
        }
        new_records.append(record)

    # 更新 CSV
    updated_records = []
    for filename, record in versions_dict.items():
        if record['version'] != new_version:
            updated_records.append(record)
    updated_records.extend(new_records)
    write_versions_csv(updated_records)

    # 6. 生成 Markdown
    md_content = generate_versions_md(new_articles, new_version, published_at)
    with open(VERSIONS_MD, 'w', encoding='utf-8') as f:
        f.write(md_content)

    # 7. 更新 VERSION 文件
    with open(VERSION_FILE, 'w') as f:
        f.write(new_version)

    # 8. 完成
    print(f"\n[OK] Version {new_version} created successfully")
    print(f"[INFO] Total articles: {len(articles)}")
    print(f"[INFO] New articles: {len(new_articles)}")
    print(f"[INFO] Run 'python scripts/prepare_deploy.py' to prepare deployment")

    return True

def main():
    import sys

    version = None
    if len(sys.argv) > 1:
        version = sys.argv[1]

    try:
        success = create_version(version)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Failed to create version: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
