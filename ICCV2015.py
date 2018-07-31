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

url = 'http://openaccess.thecvf.com//ICCV2015.py'
web_context = get_context(url)

#find paper files

'''
(?<=href=\"): 寻找开头，匹配此句之后的内容
.+: 匹配多个字符（除了换行符）
?pdf: 匹配零次或一次pdf
(?=\">pdf): 以">pdf" 结尾
|: 或
'''
#link pattern: href="***_ICCV_2015_paper.pdf">pdf
link_list = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)",web_context)
#name pattern: <a href="***_ICCV_2015_paper.html">***</a>
name_list = re.findall(r"(?<=2015_paper.html\">).+(?=</a>)",web_context)
import csv
csvfile = open('ICCV15.csv', 'w')
writer = csv.writer(csvfile)
writer.writerow(['id', 'keywords'])
data = []
for x in range(len(link_list)):
    data.append((x, name_list[x]))
    print(data[x])

writer.writerows(data)
csvfile.close()
#download
# create local filefolder
local_dir = 'D:\\ICCV15\\'
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

import threading
import time

def getpdf(arg):
    time.sleep(1)
    file_name = name_list[arg]
    download_url = link_list[arg]
    file_name = re.sub('[:\?/]+',"_",file_name).replace(' ','_')
    file_path = local_dir + file_name + '.pdf'
    print( '['+str(arg)+'/'+str(len(link_list))+'] Downloading' + file_path)
    try:
        urllib.request.urlretrieve("http://openaccess.thecvf.com/" + download_url, file_path)
    except Exception as e:
        time.sleep(12)
        urllib.request.urlretrieve("http://openaccess.thecvf.com/" + download_url, file_path)
        # none123.append(arg)
        # print(none123)

for num in range(len(link_list)):
    t = threading.Thread(target=getpdf,args=(num,))
    t.start()
print('Finished')