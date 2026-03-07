import os
import urllib.parse
import datetime

def generate_exam_nav():
    # 1. 排除配置
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode', 'assets', 'static'}
    exclude_files = {'generate_nav.py', '_config.yml', '.nojekyll'}
    target_files = {'README.md', 'index.md'}
    
    icon_map = {"math": "🔢", "english": "🔤", "physics": "🧪", "code": "💻", "exam": "📝", "note": "📒", "python": "🐍"}

    # 遍历并生成内容逻辑
    def get_content(target_extension):
        """
        target_extension: 生成链接的后缀 ('.md' 或 '.html')
        """
        content_lines = [
            "# 📚 错题集导航\n\n",
            "**当前位置：[🏠 首页](https://jasonlebei.github.io/cuo-ti-ji-lu/) / 📂 全部记录**\n\n",
            "---\n\n"
        ]

        for root, dirs, files in os.walk('.'):
            # 过滤并排序目录
            dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
            
            # 过滤 md 文件
            md_files = sorted([f for f in files if f.endswith('.md') and f not in exclude_files and f not in target_files])
            
            relative_path = os.path.relpath(root, '.')
            
            if root != ".":
                folder_name = os.path.basename(root)
                depth = relative_path.replace("\\", "/").count("/")
                header_level = "#" * (depth + 1)
                content_lines.append(f"{header_level} 📂 {folder_name}\n\n")

            if md_files:
                for file in md_files:
                    display_name = os.path.splitext(file)[0]
                    icon = "📄"
                    for key, val in icon_map.items():
                        if key in display_name.lower():
                            icon = val
                            break

                    # 核心逻辑：根据 target_extension 决定后缀
                    clean_rel_path = relative_path.replace("\\", "/")
                    if relative_path == ".":
                        url_path = f"{display_name}{target_extension}"
                    else:
                        url_path = f"{clean_rel_path}/{display_name}{target_extension}"
                    
                    safe_url = urllib.parse.quote(url_path, safe='/')
                    content_lines.append(f"* {icon} [{display_name}](./{safe_url})\n")
                
                content_lines.append("\n")

        now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
        content_lines.append("---\n")
        content_lines.append(f"> 🕒 最近更新时间：{now} (北京时间)\n")
        return "".join(content_lines)

    # 6. 分别写入
    for filename in target_files:
        try:
            # README.md 指向 .md | index.md 指向 .html
            ext = ".md" if filename == "README.md" else ".html"
            content = get_content(ext)
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 成功同步: {filename} (链接后缀: {ext})")
        except Exception as e:
            print(f"❌ 写入 {filename} 失败: {e}")

if __name__ == "__main__":
    generate_exam_nav()
