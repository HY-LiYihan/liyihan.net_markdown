#!/usr/bin/env python3
import os
import frontmatter
from pathlib import Path

CATEGORIES = {
    'Linux': 'Linux',
    '工具': '工具',
    '开发': '开发'
}

def parse_markdown_file(filepath):
    try:
        post = frontmatter.load(filepath)
        return {
            'title': post.get('title', Path(filepath).stem),
            'path': filepath,
            'categories': post.get('categories', []),
            'tags': post.get('tags', [])
        }
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

def scan_directory(category_name, dir_path):
    files = []
    if not os.path.exists(dir_path):
        return files
    
    for root, dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, '.')
                post_info = parse_markdown_file(filepath)
                if post_info:
                    post_info['path'] = rel_path
                    files.append(post_info)
    
    return files

def generate_readme():
    readme_content = "# 个人知识库\n\n"
    
    for category_name, dir_name in CATEGORIES.items():
        category_path = dir_name
        files = scan_directory(category_name, category_path)
        
        readme_content += f"## {category_name}\n"
        
        if files:
            for file_info in files:
                readme_content += f"- [{file_info['title']}]({file_info['path']})\n"
        else:
            readme_content += "*暂无内容*\n"
        
        readme_content += "\n"
    
    readme_content += "---\n\n*本 README 由 scripts/generate_readme.py 自动生成*"
    
    return readme_content

def main():
    readme_content = generate_readme()
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("[OK] README.md generated")
    
    import subprocess
    try:
        subprocess.run(['git', 'add', 'README.md'], check=True)
        subprocess.run(['git', 'commit', '-m', 'docs: update README auto-generated'], check=True)
        print("[OK] Committed to git")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git commit failed: {e}")

if __name__ == '__main__':
    main()
