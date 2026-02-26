import os

def generate_tree_nav():
    exclude_dirs = {'.git', '.github', 'node_modules'}
    exclude_files = {'README.md', 'generate_nav.py'}
    target_file = "README.md"
    
    content_lines = ["# 📚 错题集导航\n", "> 本导航由 GitHub Actions 自动更新\n\n"]

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # 排序确保顺序稳定
        dirs.sort()
        files.sort()

        depth = root.count(os.sep)
        if depth > 0:
            folder_name = os.path.basename(root)
            # 2级目录显示为 ###，以此类推
            content_lines.append(f"{'#' * (depth + 1)} 📁 {folder_name}\n")

        for file in files:
            if file.endswith('.md') and file not in exclude_files:
                # 1. 获取相对路径并统一斜杠
                raw_path = os.path.join(root, file).replace("\\", "/")
                if raw_path.startswith("./"):
                    raw_path = raw_path[2:]
                
                # 2. 关键：只替换空格，保留中文
                # Markdown 链接中，空格必须转义为 %20
                safe_path = raw_path.replace(" ", "%20")
                
                # 3. 提取文件名作为显示标题（不含后缀）
                display_name = os.path.splitext(file)[0]
                
                # 4. 写入行
                content_lines.append(f"* [{display_name}](./{safe_path})\n")
        
        if depth > 0:
            content_lines.append("\n")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write("".join(content_lines))

if __name__ == "__main__":
    generate_tree_nav()
