#-*- codeing = utf-8 -*-
#@Time  : 2024-01-30 11:41
#@Author: boo 
#@File  : renamxhtml.py

# 使用方法：调用convert_extension函数并传入目录路径
# 例如： convert_extension('/path/to/directory')

import os
import sys

def convert_extension(directory):
    for filename in os.listdir(directory):
        # print(f"filename: {directory}/{filename}")
        if filename.endswith('.xhtml'):
            base = os.path.splitext(filename)[0]
            new_filename = base + '.html'
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"--> 将filename:{directory}/{filename}, 重命名为new_filename：{directory}/{new_filename} 成功！")

if __name__ == "__main__":
    dir = "."
    if len(sys.argv) > 1:
        dir = sys.argv[1]
    convert_extension(dir)