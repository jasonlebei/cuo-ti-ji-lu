import os
import urllib.parse
import datetime

def generate_exam_nav():
    # 1. 排除配置
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode'}
    exclude_files = {'README.md', 'index.md', 'generate_nav.py', '_config.yml', '.nojekyll'}
    
    # 2. 头部信息（正文顶部的面包屑导航）
    content_lines = [
        "# 📚 错题集导航\n\n",
        "**当前位置：[🏠 首页](https://jasonlebei.github.io/cuo-ti-ji-lu/) / 📂 全部记录**\n\n",
        "--- \n\n"
    ]

    # 3. 图标映射
    icon_map = {
        "math": "🔢", "english": "🔤", "physics": "🧪", 
        "code": "💻", "exam": "📝", "note": "📒"
    }

    # 4. 遍历目录
    for root, dirs, files in os.walk('.'):
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        md_files = sorted([f for f in files if f not in exclude_files and f.endswith('.md')])

        if md_files:
            depth = 0 if root == "." else root.count(os.sep) + 1
            folder_name = os.path.basename(root)
            
            if root != ".":
                header_level = "#" * (min(depth + 1, 4))
                content_lines.append(f"{header_level} 📂 {folder_name}\n")

            for file in md_files:
                display_name = os.path.splitext(file)[0]
                
                icon = "📄"
                for key, val in icon_map.items():
                    if key in display_name.lower():
                        icon = val
                        break

                # 构造路径
                raw_path_no_ext = os.path.join(root, display_name).replace("\\", "/")
                if raw_path_no_ext.startswith("./"):
                    raw_path_no_ext = raw_path_no_ext[2:]
                
                # 【关键点】强制指向 .html 后缀，并处理 URL 编码
                # 这样 GitHub Pages 才会用 Minimal 主题渲染该页面
                safe_url = urllib.parse.quote(raw_path_no_ext, safe='/') + ".html"
                
                content_lines.append(f"  * {icon} [{display_name}](./{safe_url})\n")
            
            content_lines.append("\n---\n\n")

    # 5. 页脚时间
    now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    content_lines.append(f"\n> 🕒 最近更新时间：{now} (北京时间)")

    # 6. 写入文件
    for filename in ["README.md", "index.md"]:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("".join(content_lines))
        print(f"✅ 成功同步并美化: {filename}")

if __name__ == "__main__":
    generate_exam_nav()
