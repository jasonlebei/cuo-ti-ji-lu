import os
import urllib.parse

def generate_exam_nav():
    # 排除不需要扫描的文件夹和文件
    exclude_dirs = {'.git', '.github', 'node_modules'}
    exclude_files = {'README.md', 'index.md', 'generate_nav.py', '_config.yml', '.nojekyll'}
    
    content_lines = [
        "# 📚 错题集导航\n",
        "> 本导航由 GitHub Actions 自动更新。若页面显示 404，请尝试刷新。\n\n",
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
                # 拼接相对路径
                raw_path = os.path.join(root, file).replace("\\", "/")
                if raw_path.startswith("./"):
                    raw_path = raw_path[2:]
                
                # 关键：手动处理 URL 编码，避免 GitHub Pages 对特殊符号二次转义导致 404
                # 我们只编码空格和反引号，保留中文原样（GitHub Pages 支持中文路径）
                safe_path = raw_path.replace(" ", "%20").replace("`", "%60").replace("%", "%25")
                
                display_name = os.path.splitext(file)[0]
                content_lines.append(f"* [{display_name}](./{safe_path})\n")
            
            content_lines.append("\n")

    # --- 核心改进：同时写入两个文件 ---
    # README.md 用于仓库主页显示，index.md 用于 GitHub Pages 渲染首页
    for filename in ["README.md", "index.md"]:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("".join(content_lines))
        print(f"成功更新: {filename}")

if __name__ == "__main__":
    generate_exam_nav()
