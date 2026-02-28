import os
import urllib.parse
import datetime

def generate_exam_nav():
    # 1. 排除配置
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode', 'assets', 'static'}
    # 注意：不要在这里排除你想在导航里显示的 md 文件
    exclude_files = {'generate_nav.py', '_config.yml'}
    # 导航生成目标文件本身也要排除，防止递归扫描
    target_files = {'README.md', 'index.md'}
    
    content_lines = [
        "# 📚 错题集导航\n\n",
        "**当前位置：[🏠 首页](https://jasonlebei.github.io/cuo-ti-ji-lu/) / 📂 全部记录**\n\n",
        "---\n\n"
    ]

    icon_map = {
        "math": "🔢", "english": "🔤", "physics": "🧪", 
        "code": "💻", "exam": "📝", "note": "📒", "python": "🐍"
    }

    # 4. 遍历目录
    for root, dirs, files in os.walk('.'):
        # 排除目录
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        
        # 筛选 md 文件，同时排除 README.md 和 index.md 本身
        md_files = sorted([f for f in files if f.endswith('.md') 
                          and f not in exclude_files 
                          and f not in target_files])

        if md_files:
            relative_path = os.path.relpath(root, '.')
            
            # 文件夹标题处理
            if root == ".":
                content_lines.append(f"## 📌 根目录记录\n\n")
            else:
                # 计算深度，并将 Windows 路径分隔符替换为 /
                depth = relative_path.replace("\\", "/").count("/") + 1
                header_level = "#" * min(depth + 1, 4)
                content_lines.append(f"{header_level} 📂 {relative_path}\n\n")

            for file in md_files:
                display_name = os.path.splitext(file)[0]
                
                # 图标逻辑
                icon = "📄"
                for key, val in icon_map.items():
                    if key in display_name.lower():
                        icon = val
                        break

                # 构造相对于根目录的路径
                # 如果文件在根目录，路径就是 file；如果在子目录，就是 relative_path/file
                if relative_path == ".":
                    full_path = file
                else:
                    full_path = os.path.join(relative_path, file).replace("\\", "/")
                
                # 转换后缀为 .html (用于部署后的页面)
                url_path = os.path.splitext(full_path)[0] + ".html"
                safe_url = urllib.parse.quote(url_path, safe='/')
                
                content_lines.append(f"* {icon} [{display_name}](./{safe_url})\n")
            
            content_lines.append("\n")

    # 5. 页脚
    now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    content_lines.append("---\n")
    content_lines.append(f"> 🕒 最近更新时间：{now} (北京时间)\n")

    # 6. 写入文件
    for filename in target_files:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("".join(content_lines))
            print(f"✅ 成功同步: {filename}")
        except Exception as e:
            print(f"❌ 写入 {filename} 失败: {e}")

if __name__ == "__main__":
    generate_exam_nav()
