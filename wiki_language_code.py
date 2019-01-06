# encoding: utf-8
"""
@author: pkusp
@contact: pkusp@outlook.com

@version: 1.0
@file: wiki_language_code.py
@time: 2019/1/6 下午8:16

这一行开始写关于本文件的说明与解释
"""

import requests

from bs4 import BeautifulSoup


url = "https://zh.wikipedia.org/wiki/ISO_639-1%E4%BB%A3%E7%A0%81%E8%A1%A8"

headers = {
':authority': 'zh.wikipedia.org',
':method': 'GET',
':path': '/w/api.php?page=Template%3AAdvancedSiteNotices%2Fajax&variant=zh-cn&prop=text&action=parse&format=json&maxage=3600&smaxage=3600',
':scheme': 'https',
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
'cookie': 'WMF-Last-Access-Global=06-Jan-2019; GeoIP=CN:BJ:Beijing:39.93:116.39:v4; WMF-Last-Access=06-Jan-2019; TBLkisOn=0',
'referer': 'https://zh.wikipedia.org/wiki/ISO_639-1%E4%BB%A3%E7%A0%81%E8%A1%A8',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'x-requested-with': 'XMLHttpRequest',
}
# url = "http://www.baidu.com"
res = requests.get(url)
res_html = res.content
res_content = res_html.decode('utf-8')

# print(res_content)
print("soup start")
soup = BeautifulSoup(res_content)

trs = soup.find_all('tr')
# print(trs)
mp = {}
for tr in trs:
    tr_list = tr.text.split('\n')
    if len(tr_list) >= 6:
        mp[tr_list[1]]=(tr_list[5],tr_list[6])
    else:
        print(tr_list)

for k,v in mp.items():
    print(k,":",v)

with open("language_codes.txt",mode='w') as f:
    for k,v in mp.items():
        f.write(k+"-"+v[0]+"-"+v[1]+"\n")


print(len(mp))