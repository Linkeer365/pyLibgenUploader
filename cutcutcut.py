import os
import pandas as pd
import re

# 灵机一动，发现可以直接parse这个markdown然后用pandas写到excel里头去...

lines=[]

desktop_path=r"C:\Users\linsi\Desktop"

xlsx_path=r"C:\Users\linsi\Desktop\books-for-free.xlsx"

with open("./【长期更新】每日传书计划.md","r",encoding="utf-8") as f:
	lines=f.readlines()[13:]

# start_line="# 2020-07-03 12:02:27\n"
# start_line=""
ignores=["#",">","----","书名"]
# start_idx=None

cut_lines=[]

for line in lines:
    flag=0
    for ignore in ignores:
    	if ignore in line:
    		flag=1
    if flag==0:
    	cut_lines.append(line)

# for idx,line in enumerate(lines):
# 	if line == start_line:
# 		print("cut!")
# 		start_idx=idx
# 		break

# cut_lines=lines[start_idx:]
# cut_lines=[each for each in cut_lines if each != ignore_line]

print("END AT:",cut_lines[-1])

cut_lines_s="".join(cut_lines)

head_s="| 书名 | 作者 | ISBN号 | 图书链接 |\n| ---- | ---- | ---- | ---- |\n"

cut_lines_s=head_s+cut_lines_s

with open("{}/free-book-Chinese-CN.md".format(desktop_path),"w",encoding="utf-8") as f:
	f.write(cut_lines_s)

css_path=r"C:\Users\linsi\AppData\Roaming\Typora\themes\lavender.css"
command="D:/Anaconda3/Scripts/pandoc.exe \"C:/Users/linsi/Desktop/free-book-Chinese-CN.md\" --css \"C:/Users/linsi/AppData/Roaming/Typora/themes/lavender.css\" -o \"C:/Users/linsi/Desktop/free-book-Chinese-CN.html\" "

os.system(command)

with open("{}/free-book-Chinese-CN.md".format(desktop_path),"r",encoding="utf-8") as f:
	lines=[l.strip("\n") for l in f.readlines() if l!='\n']

packs=[[],[],[],[]]

fiction_link_len=len("http://libgen.rs/fiction/E7C5FAF75F18FDEE7EBBA0A62C2E91BA")
main_link_len=len("http://libgen.is/book/index.php?md5=D400E1D9EB9ED3F50D5AF35406D78A0C")

for line in lines:
    if "----" in line:
        continue
    title,author,isbn,link=line.split(" | ")
    title=title.lstrip("| ")
    link=link.rstrip(" |")
    link_head=link.find("http")
    if link_head!=-1:
        if "fiction" in link:
            link=link[link_head:link_head+fiction_link_len]
        elif "index.php" in link:
            link=link[link_head:link_head+main_link_len]
    packs[0].append(title)
    packs[1].append(author)
    packs[2].append(isbn)
    packs[3].append(link)

some_dict=dict()

for pack in packs:
    fieldname=pack[0]
    items=pack[1:]
    some_dict[fieldname]=items

df=pd.DataFrame(some_dict)



# df1=pd.DataFrame({'Data1':packs[0]})
# df2=pd.DataFrame({'Data2':packs[1]})
# df3=pd.DataFrame({'Data3':packs[2]})
# df4=pd.DataFrame({'Data4':packs[3]})

wt=pd.ExcelWriter(xlsx_path)

df.to_excel(wt,index=False)

# df1.to_excel(wt,sheet_name=packs[0][0],startcol=0,index=False)
# df2.to_excel(wt,sheet_name=packs[1][0],startcol=1,index=False)
# df3.to_excel(wt,sheet_name=packs[2][0],startcol=2,index=False)
# df4.to_excel(wt,sheet_name=packs[3][0],startcol=3,index=False)

# for t in packs:
#     print(t)

wt.save()

print("done.")
