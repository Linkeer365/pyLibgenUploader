import os
# ss_len=8+4
ss_len2=5
for each in os.listdir("."):
    if each.endswith(".pdf"):
        # os.rename(each,each[0:len(each)-ss_len]+".pdf")
        # os.rename(each,each[0:len(each)-ss_len2]+".pdf")
        # os.rename(each,each.replace(".pdf.pdf",".pdf"))
        os.rename(each,each.replace(" ","_"))
        # new_name=each.split("_")[1]+".pdf"
        # new_name=each.rsplit("＝",maxsplit=1)[0]+".pdf"
        # os.rename(each,new_name)

for each in os.listdir("."):
    if each.endswith(".pdf"):
        # os.rename(each,each[0:len(each)-ss_len]+".pdf")
        # os.rename(each,each[0:len(each)-ss_len2]+".pdf")
        # os.rename(each,each.replace(".pdf.pdf",".pdf"))
        os.rename(each,each.replace("__","_"))

print("done.")