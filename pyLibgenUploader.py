import requests
from lxml import etree
import os
from time import sleep
import multiprocessing
import sys


# 中文文档要改一下fields.py下面的几个函数才行...
# https://www.cnblogs.com/liaofeifight/p/5807901.html

# 学了下fiddler才知道大致要怎么搞，文件上传其实就是要处理不同类型的几个post请求而已
# https://blog.csdn.net/Enderman_xiaohei/article/details/89421773
from requests_toolbelt.multipart.encoder import MultipartEncoder


# 子进程不支持input我艹啊...


glo_comm="1"

book_dir=r"D:\AllDowns\newbooks"
result_dir=r"D:\AllDowns\upload_results"

main_url="https://library.bz/main/upload/"

upload_new_url="https://library.bz/main/uploads/new/"

check_url="https://library.bz/main/uploads/{}"

# headers 一个UA足够了，libgen不限制headers的！
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

# auth必须要有！
auth = ('genesis', 'upload')

import hashlib

def get_file_md5(file_path):
    """
    获取文件md5值
    :param file_path: 文件路径名
    :return: 文件md5值
    """
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()

def get_upload_url(file_path):
    return upload_new_url+get_file_md5(file_path)

def get_check_url(file_path):
    # print(check_url.format(get_file_md5(file_path)))
    return check_url.format(get_file_md5(file_path))


def get_title_from_path(some_path: str) -> str:
    assert some_path[-4:]
    last=some_path.rsplit(os.sep, maxsplit=1)[-1]
    return last[:-4]

def is_isbn(some_num_str: str, num_str_len=11) -> bool:
    return some_num_str.isdigit() and len(some_num_str) == num_str_len

def is_douban_id(some_num_str,num_str_len=6):
    return some_num_str.isdigit() and len(some_num_str) == num_str_len

def get_field_from_pattern(some_html, some_field_pattern: str, comm=None,is_douban=0) -> str:
    fields = some_html.xpath(some_field_pattern)
    if fields==[]:
        print("Fields Not Found")
        return None
    # 打印的漂亮一点
    if is_douban==1:
        for each_idx,each_field in enumerate(fields,1):
            print(each_field,"\t"*3,each_idx)
    print("\n")
    if comm==None:
        comm=input("Your comm:>>")
        if is_douban_id(comm) or is_isbn(comm):
            return comm
        if is_douban==1:
            glo_comm=comm
    if comm.isdigit():
        order_idx=int(comm)-1
        return fields[order_idx]
    elif comm == "j":
        # join list
        return "".join(fields)
    elif comm == "ph":
        # pick head
        return fields[0]
    elif comm == "pt":
        # pick tail
        return fields[-1]
    elif comm == "d":
        # drop list
        return "NIL"
    elif comm == "r":
        # remain the same
        return fields

def get_page_text(some_url: str, auth_flag=0) -> str:
    if auth_flag == 0:
        return requests.get(some_url, headers=headers).text
    elif auth_flag == 1:
        return requests.get(some_url, headers=headers, auth=auth).text

def fetch_douban_isbn_or_id(some_title:str, old_titles, old_ids):
    print("Book Title:{}".format(some_title))
    for some_old_idx,some_old_title in enumerate(old_titles):
        if some_title in some_old_title:
            print("already")
            some_old_id=old_ids[some_old_idx].replace("\n","")
            return some_old_id
    last_bit=some_title.rsplit(maxsplit=1)[-1]
    if is_isbn(last_bit):
        douban_isbn=last_bit
        with open(result_dir + os.sep + "Book And IDs.txt", "a", encoding="utf-8") as f:
            f.write("{}\t{}\n".format(some_title, douban_isbn))
        return douban_isbn
    else:
        base1="https://www.douban.com/search?cat=1001&q="
        base2="https://www.douban.com/search?q="
        # douban_url=base1+some_title
        douban_url=base2+some_title
        many_titles_html=etree.HTML(get_page_text(douban_url))
        assert many_titles_html!=None
        bookinfo_pattern="//span[@class='subject-cast']//text()"
        bookinfo=get_field_from_pattern(many_titles_html,bookinfo_pattern,is_douban=1)
        if is_isbn(bookinfo) or is_douban_id(bookinfo):
            douban_id=bookinfo
            with open(result_dir+os.sep+"Book And IDs.txt","a",encoding="utf-8") as f:
                f.write("{}\t{}\n".format(some_title,douban_id))
            return douban_id
        booklink_pattern="//a[contains(@href,'%2Fbook.douban.com%2F') and @class='nbg'][position()={}]//@href".format(glo_comm)
        booklink=get_field_from_pattern(many_titles_html,booklink_pattern,comm="1",is_douban=2)

        # 可见是4个%2F和5个%2F
        # len(base_str)=76,
        bare_str="https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F"
        booklink_cut1=booklink[76:]
        first_idx=booklink.find("%2F")
        douban_id=booklink_cut1[0:first_idx]

        # bookid_slice=slice(len(bare_str),len(full_str))
        # len(base_str)=76,len(full_str)=76+7=83

        # 有些douban_id长度是8...

        # douban_id=booklink[76:83]
        print(douban_id)
        with open(result_dir + os.sep + "Book And IDs.txt", "a", encoding="utf-8") as f:
            f.write("{}\t{}\n".format(some_title, douban_id))

        return douban_id

def check_if_uploaded(check_url_with_md5):
    check_pattern="//div[@class='error']//text()"
    page_text=get_page_text(check_url_with_md5,auth_flag=1)
    checker=get_field_from_pattern(etree.HTML(page_text),check_pattern,comm="1")
    print("Checker:\t",checker)
    return not checker


def upload_one_book(some_path, some_id):

    print("Some Path:{}".format(some_path))

    bool2=check_if_uploaded(get_check_url(some_path))
    print(bool2)

    if bool2:
        print("Earlier uploaded.")
        return None

    # 填写 multipart/form-data的表单，
    # 详见 https://blog.csdn.net/j_akill/article/details/43560293
    # print(get_title_from_path(some_path))
    book_with_pdf=get_title_from_path(some_path)+".pdf"
    book_without_pdf=get_title_from_path(some_path)
    print(book_with_pdf)

    headers2=headers.copy()
    m = MultipartEncoder(fields={'file': (book_with_pdf,open(some_path, 'rb'),"application/pdf")})
    headers2['Content-Type']=m.content_type

    r1=requests.post(main_url,data=m,headers=headers2,auth=auth)


    upload_url=get_upload_url(some_path)



    print("Upload Url:",upload_url)

    toc_text=get_page_text(upload_url,auth_flag=1)

    ori_toc=get_field_from_pattern(etree.HTML(toc_text),"//textarea[@name='toc']//text()",comm="1")
    #
    mywords = "\n\n书签已装载，\n书签制作方法请找 yjyouaremysunshine@163.com\n完全免费\n\n"
    #
    payload={  "metadata_source": "douban",
            "metadata_query": "{}".format(some_id),
            "fetch_metadata": "Fetch",
            "toc":ori_toc,
            "language":"中文"}

    r2=requests.post(upload_url,data=payload,auth=auth)

    info_html=etree.HTML(r2.text)

    field_name_pattern1="//input[@type='text' and @name and @value]//@name"
    field_value_pattern1="//input[@type='text' and @name and @value]//@value"
    field_name_pattern2="//textarea[@name]//@name"
    field_value_pattern2="//textarea[@name]//text()"
    fields_name1=get_field_from_pattern(info_html,field_name_pattern1,comm="r")
    fields_value1=get_field_from_pattern(info_html,field_value_pattern1,comm="r")
    fields_name2=get_field_from_pattern(info_html,field_name_pattern2,comm="r")
    fields_value2=get_field_from_pattern(info_html,field_value_pattern2,comm="r")

    print(fields_name1)
    print(fields_value1)
    print(fields_name2)
    print(fields_value2)


    fields1=dict(zip(fields_name1,fields_value1))
    fields2=dict(zip(fields_name2,fields_value2))

    # 补上mywords

    for k,v in fields2.items():
        if k=="description":
            new_v=mywords+v
            fields2[k]=new_v

    # update过程，无返回值r

    fields=fields1.copy()
    fields.update(fields2)

    if "上" in book_without_pdf:
        fields["volume"]="1"
    elif "下" in book_without_pdf:
        fields["volume"]="2"
    else:
        pass

    must_display_name={"year","fetch_metadata"}


    for k,v in fields.items():
        if (not k in must_display_name) and bool(v)==0:
            continue
        print("{}:\t{}".format(k,v))

    form_data=fields.copy()

    for k,v in fields.items():
        v_tup=(None,v)
        form_data[k]=v_tup

    r3=requests.post(upload_url,files=form_data,headers=headers,auth=auth,params=fields)

    print(r3.headers)
    # if r3.status_code==200:
    #     print("One book uploaded yet.")

    with open(result_dir+os.sep+get_title_from_path(some_path)+"-"+some_id+".txt","w",encoding="utf-8") as f:
        f.write(r3.text)


def single(some_book):
    # assert all([each.endswith(".pdf") for each in os.listdir(book_dir)])
    book_path=book_dir+os.sep+some_book
    book_title=get_title_from_path(book_path)
    book_id=fetch_douban_isbn_or_id(book_title)
    upload_one_book(book_path,book_id)

def main():
    # IO密集型
    # pool=multiprocessing.Pool(processes=1)

    # 按照修改时间排序，最早的最先出现
    books=sorted(os.listdir(book_dir),key=lambda x: os.path.getmtime(os.path.join(book_dir, x)),reverse=True)
    with open(result_dir + os.sep + "Book And IDs.txt", "r", encoding="utf-8") as f:
        lines=f.readlines()
    old_titles=[each_line.split("\t")[0] for each_line in lines]
    old_ids=[each_line.split("\t")[1] for each_line in lines]
    bookids=[fetch_douban_isbn_or_id(book[:-4],old_titles,old_ids) for book in books]
    # books_bookids=[book[:-4]+"\t"+bookid+"\n" for book,bookid in zip(books,bookids)]
    # books_bookids_str="".join(books_bookids)
    # with open(result_dir+os.sep+"Book And IDs.txt","a",encoding="utf-8") as f:
    #     f.write(books_bookids_str)
    for each_idx,each_book in enumerate(books):
        bookid=bookids[each_idx]
        book_path=book_dir+os.sep+each_book
        upload_one_book(book_path,bookid)
        # pool.apply_async(single,args=(each_book,))

    # print("Pool: Wait for all done.")
    # pool.close()
    # pool.join()

    print("all done.")



if __name__ == '__main__':
    main()



# upload_one_book(r"C:\Users\linsi\Desktop\中文测试文档.pdf","9781580173728")

def tt(some_title,some_path):
    headers2=headers.copy()
    m = MultipartEncoder(fields={'file': (some_title,open(some_path, 'rb'),"application/pdf")})
    headers2['Content-Type']=m.content_type
    # headers2["Host"]="library.bz"
    # headers2["Referer"]="https://library.bz/main/upload/"


    response = requests.post(url=main_url,
                             data=m,
                             headers=headers2,
                             auth=auth)
    ul_link=get_upload_url(some_path)
    print("1: ", ul_link)
    print("3: ", response.headers)

# tt("中文测试文档.pdf",r"C:\Users\linsi\Desktop\中文测试文档.pdf")

