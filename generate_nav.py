import os
import urllib.parse
import datetime

def generate_exam_nav():
    # 1. 排除不需要扫描的目录和文件
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode', 'assets', 'static'}
    # 仅排除脚本和配置文件，不要排除 README.md，否则根目录会被跳过
    exclude_files = {'generate_nav.py', '_config.yml', '.nojekyll'}
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

    # 4. 遍历目录 (按字母顺序排序确保目录层级正确)
    for root, dirs, files in os.walk('.'):
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        
        # 筛选有效 md 文件（排除自身生成的目标文件）
        md_files = sorted([f for f in files if f.endswith('.md') 
                          and f not in exclude_files 
                          and f not in target_files])

        if md_files:
            relative_path = os.path.relpath(root, '.')
            
            # --- 标题层级逻辑修正 ---
            if root == ".":
                content_lines.append(f"## 📌 根目录记录\n\n")
            else:
                # 取得当前文件夹名称
                folder_name = os.path.basename(root)
                # 计算路径深度：1级子目录(如'2级')深度为0，2级子目录(如'2025.12')深度为1
                depth = 0 if relative_path == "." else relative_path.replace("\\", "/").count("/")
                
                # 根据深度决定 # 数量：深度0 -> # (一级), 深度1 -> ## (二级)
                header_level = "#" * (depth + 1)
                content_lines.append(f"{header_level} {folder_name}\n\n")

            # --- 文件链接生成 ---
            for file in md_files:
                display_name = os.path.splitext(file)[0]
                icon = "📄"
                for key, val in icon_map.items():
                    if key in display_name.lower():
                        icon = val
                        break

                # 构造 URL 路径
                if relative_path == ".":
                    url_path = display_name + ".html"
                else:
                    # 将路径中的 \ 换成 / 以兼容 web
                    clean_rel_path = relative_path.replace("\\", "/")
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
