from io import BytesIO
import json
import os
import sys
import ebooklib
from bs4 import BeautifulSoup
from PIL import Image
from ebooklib import epub, utils

args = sys.argv
if len(args) < 2:
    print("第一个参数为epub的路径，如 python epub2html.py path/mybook.epub")
    exit(1)
path = args[1]
book_name = ((path.split("/")[-1]).split('.')[0]).lower().replace(" ", "_")

if len(args) > 2:
    book_name = args[2]

print(f"path:{path}, book_name:{book_name}")

# http://docs.sourcefabric.org/projects/ebooklib/en/latest/tutorial.html#introduction
book = epub.read_epub(path)
title = book.title


def fetch_toc_list(tocs):
    toc_array = [];
    for toc in tocs:
        if (type(toc) is tuple) or (type(toc) is list):
            # print(toc)
            v = fetch_toc_list(toc)
            toc_array.extend(v)
        else:
            toc_href = toc.href
            # toc_title = toc.title
            toc_array.append({"href":toc_href.split("#")[0], "title":toc.title})

    return toc_array;

def gen_item_toc(toc_item):
    return f'<li><a href="{toc_item.href}">{toc_item.title}</a></li>'

def gen_toc(toc_list):
    toc_array = [];
    toc_array.append('<lu>')
    for toc in toc_list:
        # print(type(toc))
        if (type(toc) is tuple) or (type(toc) is list):
            toc_array.append(gen_toc(toc))
        else:
            toc_array.append(gen_item_toc(toc))
    toc_array.append('</lu>')
    return "".join(toc_array);

def item_out_test(items):
    # 解析
    for item in items:
        print(f'名称：{item.title},type:{item.get_type()}')

def check_dir(out_file_name):
    # 获取目录路径
    directory = os.path.dirname(out_file_name)
    # 如果目录不存在，则创建目录
    if not os.path.exists(directory):
        os.makedirs(directory)

# 输出目录
def out_index():
    toc_layout_str = f"""---
layout: post
title: {book.title}
category: book
---
"""
    toc_str = gen_toc(book.toc)
    out_file_name = book_name+'/index.html'
    check_dir(out_file_name)
    with open(out_file_name, 'w') as f:
        f.write(toc_layout_str)
        f.write(toc_str)

# 输出css
def out_resources_css():
    styles = []
    # 输出资源 css
    for item in book.get_items_of_type(ebooklib.ITEM_STYLE):
        file_name = item.file_name
        out_file_name = book_name+"/"+file_name
        check_dir(out_file_name)
        with open(out_file_name, 'w') as f:
            f.write(item.get_content().decode('utf-8'))
        styles.append(item.file_name)
    return styles

# 输出图片
def out_resources_image():
    # 输出 图片
    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        file_name = item.file_name
        out_file_name = book_name+"/"+file_name
        check_dir(out_file_name)
        with Image.open(BytesIO(item.get_content())) as image:
            # 保存图片
            image.save(out_file_name)
       

# 输出图片 css等资源数据
def out_resources():
    # 解析
    doc_list = []
    styles = []
    for item in book.get_items():
        file_name = item.file_name
        out_file_name = book_name+"/"+file_name
        check_dir(out_file_name)
        type = item.get_type()
        # 提取书中的文本内容
        if type == ebooklib.ITEM_DOCUMENT:
            print(f"【html】，文件：{file_name}, 类型：{type}")
            doc_list.append(item)
        elif type == ebooklib.ITEM_IMAGE:
            print(f"输出【图片】，文件：{file_name}, 类型：{type}")
            with Image.open(BytesIO(item.get_content())) as image:
                # 保存图片
                image.save(out_file_name)
        elif type == ebooklib.ITEM_STYLE:
            print(f"输出【style】，文件：{file_name}, 类型：{type}")
            with open(out_file_name, 'w') as f:
                f.write(item.get_content().decode('utf-8'))
            styles.append(file_name)
        else:
            print(f"找不到输出，名称：{file_name}, 类型：{type}")
    return [doc_list, styles]


def build_style(file_name:str):
    name = file_name.split("#")[0]
    flag = len(name.split("/")) - 1
    vv = []
    for v in styles:
        if flag > 0:
            vv.append("\""+(str("../" * flag) + v) +"\"")
        else:
            vv.append("\""+ v +"\"")

    return ",".join(vv) 


def build_index(file_name:str):
    name = file_name.split("#")[0]
    flag = len(name.split("/")) - 1
    if flag > 0:
        return str("../"*flag) + "index.html"
    else:
        return  "index.html"
    
def item_out_with_toc():
    idx:int = 0
    for item in doc_list:
        file_name = item.file_name
        styles_str = build_style(file_name)
        index_url = build_index(file_name);
        out_file_name = book_name+"/"+file_name
        check_dir(out_file_name)
        pre_url = index_url
        if idx > 0:
            pre_item = doc_list[idx - 1]
            pre_url = pre_item.file_name.split("/")[-1]
        next_url = index_url
        if len(doc_list) > idx + 1:
            next_item = doc_list[idx + 1]
            next_url = next_item.file_name.split("/")[-1]
        layout = f"""---
layout: book
page_previous: {pre_url}
index_page: {index_url}
page_next: {next_url}
styles: [{styles_str}]
---
"""
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        with open(out_file_name, 'w') as f:
            f.write(layout)
            f.write(str(soup.body).replace("<body>","").replace("</body>",""))
        
        idx = idx + 1



def item_out(items):
    # 解析
    for item in items:
        file_name = item.file_name
        out_file_name = book_name+"/"+file_name
        # 获取目录路径
        directory = os.path.dirname(out_file_name)
        # 如果目录不存在，则创建目录
        if not os.path.exists(directory):
            os.makedirs(directory)
        type = item.get_type()
        # 提取书中的文本内容
        if type == ebooklib.ITEM_DOCUMENT :
            
            # epub中的内容是html格式，使用BeautifulSoup可以完美解析
            # 将BeautifulSoup对象转换为字符串
            # body = soup.body.find_all()
            # 将字符串写入文件
            print(f"输出【html】，文件：{file_name}, 类型：{type}")
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            with open(out_file_name, 'w') as f:
                f.write(str(soup.body).replace("<body>","").replace("</body>",""))
                # for ctx in soup.body.contents:
                #     et = str(ctx)
                #     if et != '\n\r' and et != '\n' :
                #         f.write(et)
                
        elif type == ebooklib.ITEM_IMAGE:
            print(f"输出【图片】，文件：{file_name}, 类型：{type}")
            #with open('html/'+file_name, 'w') as f:
            #    f.write(item.get_content())
            # 将图片数据转换为PIL图像对象
            with Image.open(BytesIO(item.get_content())) as image:
                # 保存图片
                image.save(out_file_name)
        elif type == ebooklib.ITEM_STYLE:
            # epub中的内容是html格式，使用BeautifulSoup可以完美解析
            #soup = BeautifulSoup(item.get_content(), )
            # 将BeautifulSoup对象转换为字符串
            #soup_str = str(soup)
            # 将字符串写入文件
            print(f"输出【html】，文件：{file_name}, 类型：{type}")
            with open(out_file_name, 'w') as f:
                f.write(item.get_content().decode('utf-8'))
        else:
            print(f"找不到输出，名称：{file_name}, 类型：{type}")

def gen_single_toc(toc_list):
    toc_array = [];
    toc_array.append('<lu>')
    for toc in toc_list:
        # print(type(toc))
        if (type(toc) is tuple) or (type(toc) is list):
            toc_array.append(gen_toc(toc))
        else:
            v = toc.href.split("#")[0]

            toc_array.append(f'<li><a href="#{v.replace(".", "_").replace("/", "_")}">{toc.title}</a></li>')
    toc_array.append('</lu>')
    return "".join(toc_array);


def item_out_single():
    first_item = doc_list[0]
    first_file_name = first_item.file_name
    ffs = first_file_name.split("/")
    pf = ""
    if len(ffs) > 1:
        pf = str("../" * (len(ffs) - 1))
    styles_list = []
    for style in styles:
        styles_list.append(f'<link rel="stylesheet" href="{pf}{style}">')
    styles_str = "\r\n".join(styles_list)   
    html_pre = f"""<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title> {book.title} </title>
        {styles_str}

    </head>
    <body>
"""
    html_end = """
    </body>
</html>
"""
    
    ffs[-1] = 'single.html'
    single_name = "/".join(ffs)

    html = open(book_name+"/"+single_name, 'w')
    html.write(html_pre)

    toc_str = gen_single_toc(book.toc)
    html.write(toc_str)
    # 解析
    for item in doc_list:
        mp = item.file_name.replace(".", "_").replace("/", "_")
        html.write(f'<a name="{mp}"></a>')
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        html.write(str(soup.body).replace("<body>","").replace("</body>",""))

    html.write(html_end)
    html.flush()   
    html.close()


# toc_list = fetch_toc_list(book.toc)
# out_index()
res = out_resources()
doc_list = res[0]
styles = res[1]
#item_out_with_toc()
item_out_single()
    