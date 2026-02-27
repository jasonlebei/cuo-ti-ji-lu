import os
import urllib.parse

def generate_exam_nav():
    # 排除不需要扫描的文件夹和文件
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode'}
    exclude_files = {'README.md', 'index.md', 'generate_nav.py', '_config.yml', '.nojekyll'}
    
    content_lines = [
        "# 📚 错题集导航\n\n",
        "> 💡 **提示**：本页面由 GitHub Actions 自动构建更新。点击下方链接即可查看详情。\n\n",
        "--- \n\n"
    ]

    # 定义图标映射（可根据需要增加）
    icon_map = {
        "math": "🔢",
        "english": "🔤",
        "physics": "🧪",
        "code": "💻",
        "exam": "📝"
    }

    # 遍历当前目录
    for root, dirs, files in os.walk('.'):
        # 过滤掉排除目录
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        # 仅处理 .md 文件
        files = sorted([f for f in files if f not in exclude_files and f.endswith('.md')])

        # 计算目录深度
        depth = 0 if root == "." else root.count(os.sep) + 1
        
        if files:
            folder_name = os.path.basename(root)
            if root != ".":
                # 使用不同的标题等级和图标美化文件夹
                header_level = "#" * (min(depth + 1, 4)) 
                content_lines.append(f"{header_level} 📂 {folder_name}\n")

            for file in files:
                # 1. 获取不带后缀的文件名
                display_name = os.path.splitext(file)[0]
                
                # 2. 匹配图标（根据文件名匹配，默认使用 📄）
                icon = "📄"
                for key, val in icon_map.items():
                    if key in display_name.lower():
                        icon = val
                        break

                # 3. 核心修改：处理路径（去掉 .md 后缀）
                # 获取文件的相对路径并去掉 .md
                raw_path_no_ext = os.path.join(root, display_name).replace("\\", "/")
                if raw_path_no_ext.startswith("./"):
                    raw_path_no_ext = raw_path_no_ext[2:]
                
                # 4. URL 编码处理
                safe_path = urllib.parse.quote(raw_path_no_ext, safe='/')
                
                # 5. 生成美化后的列表项
                content_lines.append(f"  * {icon} [{display_name}](./{safe_path})\n")
            
            content_lines.append("\n---\n\n") # 文件夹间增加分割线

    # 移除最后一个多余的分割线
    if content_lines[-1] == "\n---\n\n":
        content_lines.pop()

    # 页脚美化
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    content_lines.append(f"\n\n---\n> 🕒 最近更新时间：{now}")

    # --- 双写逻辑 ---
    for filename in ["README.md", "index.md"]:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("".join(content_lines))
        print(f"✅ 已美化并同步: {filename}")

if __name__ == "__main__":
    generate_exam_nav()
