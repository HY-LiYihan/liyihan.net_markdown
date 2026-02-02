#!/usr/bin/env python3
import os
import frontmatter
from pathlib import Path

STAGING_DIR = 'staging'
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

def read_publish_list():
    """读取发布列表"""
    if not os.path.exists(PUBLISH_FILE):
        return []

    selected_paths = []
    with open(PUBLISH_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                selected_paths.append(line)

    return selected_paths

def write_publish_list(paths):
    """写入发布列表"""
    with open(PUBLISH_FILE, 'w', encoding='utf-8') as f:
        f.write("# Publish List\n")
        f.write("# 以 # 开头的行会被忽略\n")
        f.write("# 每行一个文件路径\n\n")
        for path in paths:
            f.write(f"{path}\n")

def list_command():
    """列出命令"""
    articles = list_staging_articles()

    if not articles:
        print("[INFO] No articles found in staging/")
        return

    selected_paths = read_publish_list()

    print(f"\nFound {len(articles)} articles in staging/:\n")
    for i, article in enumerate(articles, 1):
        marker = "✓" if article['path'] in selected_paths else " "
        print(f"{marker} {i}. {article['path']} - {article['title']}")
        print(f"       Size: {article['size']} bytes | Modified: {datetime.fromtimestamp(article['modified']).strftime('%Y-%m-%d %H:%M:%S')}")

    if selected_paths:
        print(f"\n[INFO] {len(selected_paths)} articles in publish list")
    else:
        print("\n[INFO] Publish list is empty")

def add_command(file_path):
    """添加命令"""
    if not file_path:
        print("[ERROR] File path required")
        return

    # 检查文件是否存在
    full_path = os.path.join(STAGING_DIR, file_path)
    if not os.path.exists(full_path):
        print(f"[ERROR] File not found: {file_path}")
        return

    # 读取当前列表
    selected_paths = read_publish_list()

    # 添加文件
    if file_path not in selected_paths:
        selected_paths.append(file_path)
        write_publish_list(selected_paths)
        print(f"[OK] Added to publish list: {file_path}")
    else:
        print(f"[INFO] Already in publish list: {file_path}")

def remove_command(file_path):
    """移除命令"""
    if not file_path:
        print("[ERROR] File path required")
        return

    # 读取当前列表
    selected_paths = read_publish_list()

    # 移除文件
    if file_path in selected_paths:
        selected_paths.remove(file_path)
        write_publish_list(selected_paths)
        print(f"[OK] Removed from publish list: {file_path}")
    else:
        print(f"[INFO] Not in publish list: {file_path}")

def clear_command():
    """清空命令"""
    if not os.path.exists(PUBLISH_FILE):
        print("[INFO] Publish list is already empty")
        return

    choice = input("Are you sure you want to clear the publish list? (yes/no): ")
    if choice.lower() in ['yes', 'y']:
        write_publish_list([])
        print("[OK] Publish list cleared")
    else:
        print("[INFO] Operation cancelled")

def view_command():
    """查看命令"""
    selected_paths = read_publish_list()

    if not selected_paths:
        print("[INFO] Publish list is empty")
        return

    print("\nPublish List:\n")
    for i, path in enumerate(selected_paths, 1):
        full_path = os.path.join(STAGING_DIR, path)
        if os.path.exists(full_path):
            title = get_file_title(full_path)
            print(f"  {i}. {path}")
            print(f"     Title: {title}")
        else:
            print(f"  {i}. {path} (FILE NOT FOUND)")
    print()

def interactive_command():
    """交互式命令"""
    articles = list_staging_articles()
    if not articles:
        print("[INFO] No articles found in staging/")
        return

    selected_paths = read_publish_list()
    selected_set = set(selected_paths)

    while True:
        print("\n" + "=" * 60)
        print("Publish List Manager")
        print("=" * 60)

        print("\nCurrent list:")
        for i, path in enumerate(selected_paths, 1):
            print(f"  {i}. {path}")

        print("\nAvailable articles in staging:")
        for i, article in enumerate(articles, 1):
            marker = "[✓]" if article['path'] in selected_set else "[ ]"
            print(f"  {marker} {i}. {article['path']} - {article['title']}")

        print("\nActions:")
        print("  [1] Add articles (enter numbers, separate with spaces)")
        print("  [2] Remove articles (enter numbers)")
        print("  [3] Clear list")
        print("  [4] View list")
        print("  [5] Save and exit")
        print("  [0] Exit without saving")

        try:
            choice = input("\nYour choice: ").strip()

            if choice == '0':
                print("[INFO] Exited without saving")
                break
            elif choice == '1':
                input_str = input("Enter numbers to add (separate with spaces): ").strip()
                if not input_str:
                    continue

                indices = [int(x.strip()) - 1 for x in input_str.split()]
                for idx in indices:
                    if 0 <= idx < len(articles):
                        article = articles[idx]
                        if article['path'] not in selected_set:
                            selected_paths.append(article['path'])
                            selected_set.add(article['path'])
                            print(f"  [+] {article['path']}")

            elif choice == '2':
                if not selected_paths:
                    print("[INFO] List is empty")
                    continue

                input_str = input("Enter numbers to remove (separate with spaces): ").strip()
                if not input_str:
                    continue

                indices = [int(x.strip()) - 1 for x in input_str.split()]
                to_remove = []

                for idx in indices:
                    if 0 <= idx < len(selected_paths):
                        path = selected_paths[idx]
                        to_remove.append(path)

                for path in to_remove:
                    selected_paths.remove(path)
                    selected_set.remove(path)
                    print(f"  [-] {path}")

            elif choice == '3':
                if not selected_paths:
                    print("[INFO] List is already empty")
                    continue

                choice_confirm = input("Are you sure? (yes/no): ").strip().lower()
                if choice_confirm in ['yes', 'y']:
                    selected_paths.clear()
                    selected_set.clear()
                    print("[OK] List cleared")

            elif choice == '4':
                view_command()

            elif choice == '5':
                write_publish_list(selected_paths)
                print(f"[OK] List saved to {PUBLISH_FILE}")
                break

        except (ValueError, KeyboardInterrupt):
            print("\n[INFO] Invalid input")

def main():
    import sys
    from datetime import datetime

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python select_articles.py --list")
        print("  python select_articles.py --add <file_path>")
        print("  python select_articles.py --remove <file_path>")
        print("  python select_articles.py --clear")
        print("  python select_articles.py --view")
        print("  python select_articles.py --interactive")
        sys.exit(1)

    action = sys.argv[1]

    if action == '--list':
        list_command()
    elif action == '--add':
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        add_command(file_path)
    elif action == '--remove':
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        remove_command(file_path)
    elif action == '--clear':
        clear_command()
    elif action == '--view':
        view_command()
    elif action == '--interactive':
        interactive_command()
    else:
        print(f"[ERROR] Unknown action: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()
