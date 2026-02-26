import os
import urllib.parse

def generate_exam_nav():
    # 排除不需要扫描的文件夹和文件
    exclude_dirs = {'.git', '.github', 'node_modules'}
    exclude_files = {'README.md', 'index.md', 'generate_nav.py', '_config.yml', '.nojekyll'}
    
    content_lines = [
        "# 📚 错题集导航\n",
        "> 本导航由 GitHub Actions 自动更新。若页面显示 404，请强制刷新浏览器。\n\n",
        "--- \n\n"
    ]

    # 遍历当前目录
    for root, dirs, files in os.walk('.'):
        # 过滤掉排除目录
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        # 仅处理 .md 文件
        files = sorted([f for f in files if f not in exclude_files and f.endswith('.md')])

        # 计算目录深度（用于生成标题等级）
        depth = 0 if root == "." else root.count(os.sep) + 1
        
        if files:
            folder_name = os.path.basename(root)
            if root != ".":
                header_level = "#" * (min(depth + 1, 6)) 
                content_lines.append(f"{header_level} 📁 {folder_name}\n")

            for file in files:
                # 拼接相对路径并统一使用正斜杠
                raw_path = os.path.join(root, file).replace("\\", "/")
                if raw_path.startswith("./"):
                    raw_path = raw_path[2:]
                
                # --- 核心改进：使用标准 URL 编码 ---
                # urllib.parse.quote 会把空格转为 %20，把中文转为编码
                # safe='/' 表示不对斜杠进行编码，保留路径结构
                safe_path = urllib.parse.quote(raw_path, safe='/')
                
                display_name = os.path.splitext(file)[0]
                # 在导航中显示原名，但链接使用 safe_path
                content_lines.append(f"* [{display_name}](./{safe_path})\n")
            
            content_lines.append("\n")

    # --- 双写逻辑：同时更新 README 和 index ---
    for filename in ["README.md", "index.md"]:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("".join(content_lines))
        print(f"✅ 已成功同步内容至: {filename}")

if __name__ == "__main__":
    generate_exam_nav()
