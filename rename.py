import os
import re

root_path = r"D:\obsidian\src\知识笔记"  # 修改为你的 Obsidian 根目录路径

image_pattern = re.compile(r'!\[\[(.*?)\]\]')

# 建立图片路径映射
image_map = {}
for dirpath, _, filenames in os.walk(root_path):
    for f in filenames:
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            image_map[f] = os.path.join(dirpath, f)

# 处理 Markdown 文件
for dirpath, _, filenames in os.walk(root_path):
    for filename in filenames:
        if filename.endswith(".md"):
            md_path = os.path.join(dirpath, filename)
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            changed = False
            matches = image_pattern.findall(content)

            for match in matches:
                img_name = os.path.basename(match)
                if img_name in image_map:
                    correct_path = os.path.relpath(image_map[img_name], start=dirpath).replace("\\", "/")
                    if match != correct_path:
                        print(f"[✓] 修复: {match} → {correct_path}")
                        content = content.replace(f"[[{match}]]", f"[[{correct_path}]]")
                        changed = True

            if changed:
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(content)
