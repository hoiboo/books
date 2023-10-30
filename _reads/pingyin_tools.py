from pypinyin import pinyin, Style
import sys
args = sys.argv

pinyin_list = pinyin(args[1], style=Style.NORMAL)
bb = []
for pt in pinyin_list:
    bb.append(pt[0])
book_name = "".join(bb)

print(book_name)