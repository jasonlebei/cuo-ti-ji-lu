import os
import urllib.parse
import datetime

def generate_exam_nav():
    # 1. 排除配置
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode', 'assets', 'static'}
    exclude_files = {'generate_nav.py', '_config.yml', '.nojekyll'}
    target_files = {'README.md', 'index.md'}
    
    content_lines = [
        "# 📚 错题集导航\n\n",
        "**当前位置：[🏠 首页](https://jasonlebei.github.io/cuo-ti-ji-lu/) / 📂 全部记录**\n\n",
        "---\n\n"
    ]

    icon_map = {"math": "🔢", "english": "🔤", "physics": "🧪", "code": "💻", "exam": "📝", "note": "📒", "python": "🐍"}

    # 4. 遍历目录
    for root, dirs, files in os.walk('.'):
        # 过滤并排序目录
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        
        # 过滤 md 文件
        md_files = sorted([f for f in files if f.endswith('.md') and f not in exclude_files and f not in target_files])
        
        relative_path = os.path.relpath(root, '.')
        
        # --- 核心修复：只要不是根目录，就显示文件夹标题 ---
        if root != ".":
            folder_name = os.path.basename(root)
            # 计算深度：'2级' 深度为 0，'2级/2025.12' 深度为 1
            depth = relative_path.replace("\\", "/").count("/")
            
            # 这里的规则：深度0 (2级) -> #， 深度1 (2025.12) -> ##
            header_level = "#" * (depth + 1)
            content_lines.append(f"{header_level} 📂 {folder_name}\n\n")

        # 如果当前目录下有 md 文件，则列出
        if md_files:
            for file in md_files:
                display_name = os.path.splitext(file)[0]
                icon = "📄"
                for key, val in icon_map.items():
                    if key in display_name.lower():
                        icon = val
                        break

                # 构造路径
                clean_rel_path = relative_path.replace("\\", "/")
                if relative_path == ".":
                    url_path = f"{display_name}.html"
                else:
                    url_path = f"{clean_rel_path}/{display_name}.html"
                
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
