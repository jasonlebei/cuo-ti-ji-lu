import os
import urllib.parse

def generate_exam_nav():
    # --- 配置区 ---
    exclude_dirs = {'.git', '.github', 'node_modules'}
    exclude_files = {'README.md', 'generate_nav.py'}
    target_file = "README.md"
    
    # 导航头部
    content_lines = [
        "# 📚 错题集导航\n",
        "> 本导航由 GitHub Actions 自动更新。点击下方链接可查看详情。\n\n",
        "--- \n\n"
    ]

    # os.walk 会递归遍历所有子文件夹
    # 我们按名称排序以保证导航的整齐
    for root, dirs, files in os.walk('.'):
        # 排除隐藏或无关目录
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        files = sorted([f for f in files if f not in exclude_files and f.endswith('.md')])

        # 计算当前目录的深度
        # root 为 "." 时 depth 为 0
        depth = 0 if root == "." else root.count(os.sep) + (1 if os.sep in root else 1)
        
        # 如果当前文件夹下有 md 文件，则生成标题
        if files:
            folder_name = os.path.basename(root)
            if root != ".":
                # 根据深度决定标题级别 (如 2 级文件夹显示为 ###)
                header_level = "#" * (depth + 1)
                content_lines.append(f"{header_level} 📁 {folder_name}\n")

            for file in files:
                # 1. 组合完整路径并统一为 Linux 斜杠
                raw_path = os.path.join(root, file).replace("\\", "/")
                # 去掉路径开头的 ./ (如果是从根目录开始)
                if raw_path.startswith("./"):
                    raw_path = raw_path[2:]

                # 2. 核心修复：对路径进行编码，处理空格和括号冲突
                # quote 默认保留 '/'，但会把空格变 %20，括号变 %28 %29
                safe_path = urllib.parse.quote(raw_path)

                # 3. 提取文件名作为链接标题（去掉 .md 后缀）
                display_name = os.path.splitext(file)[0]

                # 4. 生成 Markdown 链接行
                content_lines.append(f"* [{display_name}](./{safe_path})\n")
            
            content_lines.append("\n")

    # 写入 README.md
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("".join(content_lines))
    print("✅ 导航更新成功！")

if __name__ == "__main__":
    generate_exam_nav()
