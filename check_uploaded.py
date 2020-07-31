import hashlib
import os


# 文件必须都有下划线 不能有空格！！

check_url="https://library.bz/main/uploads/{}"

book_dir=r"D:\AllDowns\newbooks"

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


def get_check_url(file_path):
    # print(check_url.format(get_file_md5(file_path)))
    return check_url.format(get_file_md5(file_path))

def main():
    books=sorted(os.listdir(book_dir),key=lambda x: os.path.getmtime(os.path.join(book_dir, x)),reverse=True)
    for each_book in books:
        print(get_check_url(book_dir+os.sep+each_book))
        print("")

if __name__ == '__main__':
    main()
'''
['https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F25987241%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=0',
 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F1166307%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=1',
 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F1048872%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=2',
 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F6139564%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=3', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F27045347%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=4', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F26921129%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=5', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F1363132%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=6', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F1379842%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=7', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F3151074%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=8', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F3635743%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=9', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F27094982%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=10', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F27094986%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=11', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F30514505%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=12', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F30369995%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=13', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F31184437%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=14', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F30648087%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=15', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F30612799%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=16', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F30574809%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=17', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F30573647%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=18', 'https://www.douban.com/link2/?url=https%3A%2F%2Fbook.douban.com%2Fsubject%2F30778164%2F&query=%E9%98%85%E8%AF%BB%E4%BD%A0%E7%9A%84%E7%97%87%E7%8A%B6_%E4%B8%8B%E7%AF%87&cat_id=1001&type=search&pos=19']
'''