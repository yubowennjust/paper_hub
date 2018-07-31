import os
import re
import urllib

import requests
import csv



#get web context
def get_context(url):
    """
    params:
        url: link
    return:
        web_context
    """
    web_context = requests.get(url)
    return web_context.text

url = 'http://openaccess.thecvf.com//ICCV2017.py'
web_context = get_context(url)

#find paper files

'''
(?<=href=\"): 寻找开头，匹配此句之后的内容
.+: 匹配多个字符（除了换行符）
?pdf: 匹配零次或一次pdf
(?=\">pdf): 以">pdf" 结尾
|: 或
'''
#link pattern: href="***_ICCV_2017_paper.pdf">pdf
link_list = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)",web_context)
#name pattern: <a href="***_ICCV_2017_paper.html">***</a>
name_list = re.findall(r"(?<=2017_paper.html\">).+(?=</a>)",web_context)

#download
# create local filefolder
local_dir = 'D:\\ICCV17\\'
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

cnt = 0
while cnt < len(link_list):
    file_name = name_list[cnt]
    download_url = link_list[cnt]
    #为了可以保存为文件名，将标点符号和空格替换为'_'
    file_name = re.sub('[:\?/]+',"_",file_name).replace(' ','_')
    file_path = local_dir + file_name + '.pdf'
    #download
    print( '['+str(cnt)+'/'+str(len(link_list))+'] Downloading' + file_path)
    try:
        urllib.request.urlretrieve("http://openaccess.thecvf.com/" + download_url, file_path)
    except Exception as e:
        print("GG")
    cnt += 1
print('Finished')