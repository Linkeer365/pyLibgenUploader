import os
lines=[]

desktop_path=r"C:\Users\linsi\Desktop"

with open("./【长期更新】每日传书计划.md","r",encoding="utf-8") as f:
	lines=f.readlines()

start_line="# 2020-07-03 12:02:27\n"
ignore_line="> 垃圾脚本（能用就行）: https://github.com/Linkeer365/pyLibgenUploader\n"
start_idx=None

for idx,line in enumerate(lines):
	if line == start_line:
		start_idx=idx
		break

cut_lines=lines[start_idx:]
cut_lines=[each for each in cut_lines if each != ignore_line]
cut_lines_s="".join(cut_lines)

with open("{}/ripper.md".format(desktop_path),"w",encoding="utf-8") as f:
	f.write(cut_lines_s)

css_path=r"C:\Users\linsi\AppData\Roaming\Typora\themes\lavender.css"
command="D:/Anaconda3/Scripts/pandoc.exe \"C:/Users/linsi/Desktop/ripper.md\" --css \"C:/Users/linsi/AppData/Roaming/Typora/themes/lavender.css\" -o \"C:/Users/linsi/Desktop/ripper.html\" "

os.system(command)

print("done.")
