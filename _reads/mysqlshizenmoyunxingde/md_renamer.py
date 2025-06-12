import os
import re
from pypinyin import lazy_pinyin

def convert_to_pinyin_initials(text):
    """将中文字符转换为拼音首字母缩写"""
    # 提取中文字符部分
    chinese_part = re.sub(r'[\d\-_]', '', text)
    # 转换拼音首字母
    initials = ''.join([lazy_pinyin(c)[0][0] for c in chinese_part if '\u4e00' <= c <= '\u9fff'])
    return initials

def process_directory(directory):
    index_file = os.path.join(directory, 'index.md')
    rename_mapping = {}
    
    # 第一阶段：收集重命名信息并重命名文件
    for filename in os.listdir(directory):
        if filename.endswith('.md') and filename != 'index.md':
            # 拆分文件名组成部分
            parts = re.split(r'-(\d{2}-)', filename)
            if len(parts) > 1:
                prefix = parts[1]
                chinese_part = '-'.join(parts[2:]).rsplit('.', 1)[0]
                initials = convert_to_pinyin_initials(chinese_part)
                
                # 构建新文件名
                new_filename = f"{prefix}{initials}.md"
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                
                # 执行重命名并记录映射关系
                os.rename(old_path, new_path)
                rename_mapping[filename.replace('.md', '.html')] = new_filename.replace('.md', '.html')

    # 第二阶段：更新index.md中的链接
    if os.path.exists(index_file):
        with open(index_file, 'r+', encoding='utf-8') as f:
            content = f.read()
            for old_link, new_link in rename_mapping.items():
                content = content.replace(old_link, new_link)
            f.seek(0)
            f.write(content)
            f.truncate()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    process_directory(current_dir)
