import os
import urllib.parse
import datetime

def generate_exam_nav():
    # 1. 排除配置（请确保“2级”文件夹不在这个列表里）
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode', 'assets', 'static'}
    exclude_files = {'README.md', 'index.md', 'generate_nav.py', '_config.yml', '.nojekyll'}
    
    # 2. 头部信息
    content_lines = [
        "# 📚 错题集导航\n\n",
        "**当前位置：[🏠 首页](https://jasonlebei.github.io/cuo-ti-ji-lu/) / 📂 全部记录**\n\n",
        "---\n\n"
    ]

    # 3. 图标映射
    icon_map = {
        "math": "🔢", "english": "🔤", "physics": "🧪", 
        "code": "💻", "exam": "📝", "note": "📒", "python": "🐍"
    }

    # 4. 遍历目录
    # 使用 topdown=True 配合 dirs[:] 修改可以有效过滤
    for root, dirs, files in os.walk('.'):
        # 原地修改 dirs 以排除不需要的目录
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        
        # 筛选当前目录下的 md 文件
        md_files = sorted([f for f in files if f not in exclude_files and f.endswith('.md')])

        # 只要当前目录有 md 文件，就生成该目录的标题
        if md_files:
            # 更加健壮的深度计算
            relative_path = os.path.relpath(root, '.')
            if relative_path == '.':
                depth = 0
            else:
                depth = relative_path.replace("\\", "/").count("/") + 1
            
            # 文件夹标题处理
            if root != ".":
                folder_name = os.path.basename(root)
                # 根据深度决定标题等级：1级深度对应 ##，2级对应 ###
                header_level = "#" * min(depth + 1, 4)
                content_lines.append(f"{header_level} 📂 {folder_name}\n\n")
            else:
                content_lines.append(f"## 📌 根目录记录\n\n")

            # 遍历并添加文件链接
            for file in md_files:
                display_name = os.path.splitext(file)[0]
                
                # 自动匹配图标
                icon = "📄"
                for key, val in icon_map.items():
                    if key in display_name.lower():
                        icon = val
                        break

                # 构造路径
                path_parts = relative_path.split(os.sep) if relative_path != '.' else []
                path_parts.append(display_name)
                url_path = "/".join(path_parts)
                
                # 编码 URL 并指向 .html
                safe_url = urllib.parse.quote(url_path, safe='/') + ".html"
                
                content_lines.append(f"* {icon} [{display_name}](./{safe_url})\n")
            
            # 区块结束换行
            content_lines.append("\n")

    # 5. 页脚时间（北京时间）
    now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    content_lines.append("---\n")
    content_lines.append(f"> 🕒 最近更新时间：{now} (北京时间)\n")

    # 6. 写入文件
    for filename in ["README.md", "index.md"]:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("".join(content_lines))
            print(f"✅ 成功同步: {filename}")
        except Exception as e:
            print(f"❌ 写入 {filename} 失败: {e}")

if __name__ == "__main__":
    generate_exam_nav()
