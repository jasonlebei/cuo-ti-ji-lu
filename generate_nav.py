import os
import urllib.parse
import datetime

def generate_exam_nav():
    # 1. 排除配置
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode'}
    exclude_files = {'README.md', 'index.md', 'generate_nav.py', '_config.yml', '.nojekyll'}
    
    # 2. 头部信息（确保 H1 标题前后有空行，保证渲染）
    content_lines = [
        "# 📚 错题集导航\n\n",
        "**当前位置：[🏠 首页](https://jasonlebei.github.io/cuo-ti-ji-lu/) / 📂 全部记录**\n\n",
        "---\n\n"
    ]

    # 3. 图标映射
    icon_map = {
        "math": "🔢", "english": "🔤", "physics": "🧪", 
        "code": "💻", "exam": "📝", "note": "📒"
    }

    # 4. 遍历目录
    # 使用 sorted 确保文件夹按名称排序
    for root, dirs, files in os.walk('.'):
        # 过滤并排序目录
        dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
        
        # 过滤并排序 Markdown 文件
        md_files = sorted([f for f in files if f not in exclude_files and f.endswith('.md')])

        if md_files:
            # 计算深度：根目录为 0，子目录为 1, 2...
            depth = 0 if root == "." else root.replace("\\", "/").strip("./").count("/") + 1
            
            # 文件夹标题处理
            if root != ".":
                folder_name = os.path.basename(root)
                # 确保子文件夹从 ## (二级标题) 开始
                header_level = "#" * min(depth + 1, 4)
                content_lines.append(f"{header_level} 📂 {folder_name}\n\n")
            else:
                # 根目录下的文件放在一个统一的二级标题下
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

                # 构造符合 GitHub Pages 的 HTML 路径
                raw_path_no_ext = os.path.join(root, display_name).replace("\\", "/")
                if raw_path_no_ext.startswith("./"):
                    raw_path_no_ext = raw_path_no_ext[2:]
                
                # 编码 URL 并强制指向 .html
                safe_url = urllib.parse.quote(raw_path_no_ext, safe='/') + ".html"
                
                # 每一行列表后确保换行
                content_lines.append(f"* {icon} [{display_name}](./{safe_url})\n")
            
            # 每个文件夹区块结束后增加空行和分割线
            content_lines.append("\n---\n\n")

    # 5. 页脚时间
    now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    content_lines.append(f"> 🕒 最近更新时间：{now} (北京时间)\n")

    # 6. 写入文件
    target_files = ["README.md", "index.md"]
    full_content = "".join(content_lines)
    
    for filename in target_files:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(full_content)
            print(f"✅ 成功同步并美化: {filename}")
        except Exception as e:
            print(f"❌ 写入 {filename} 失败: {e}")

if __name__ == "__main__":
    generate_exam_nav()
