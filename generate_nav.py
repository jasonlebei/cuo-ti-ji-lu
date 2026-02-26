import os

def generate_tree_nav():
    # 配置
    exclude_dirs = {'.git', '.github', 'node_modules'}
    exclude_files = {'README.md', 'generate_nav.py'}
    target_file = "README.md"
    
    content_lines = ["# 📚 错题集导航\n", "> 本导航由 GitHub Actions 自动更新\n\n"]

    # 递归遍历
    for root, dirs, files in os.walk('.'):
        # 过滤隐藏目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # 计算当前深度 (根目录为 0)
        depth = root.count(os.sep)
        if depth > 0:
            indent = "  " * (depth - 1)
            folder_name = os.path.basename(root)
            # 根据深度决定标题级别，2级文件夹用 ###，以此类推
            content_lines.append(f"{'#' * (depth + 1)} 📁 {folder_name}\n")

        # 排序文件以保持导航整齐
        for file in sorted(files):
            if file.endswith('.md') and file not in exclude_files:
                file_path = os.path.join(root, file)
                # 移除 .md 后缀作为显示名称
                display_name = os.path.splitext(file)[0]
                # 生成相对路径链接
                content_lines.append(f"* [{display_name}]({file_path})\n")
        
        content_lines.append("\n")

    # 写入文件
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("".join(content_lines))

if __name__ == "__main__":
    generate_tree_nav()
