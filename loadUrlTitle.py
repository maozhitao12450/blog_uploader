# 读取urls.txt
import requests
import json
import os
import re

url_prefix = os.getenv('UEESHOP_URL')

def load_url_title(url):
    print(f"开始获取{url}的标题,描述和相关图片信息")
    url = url.strip()
    url_file = f'tmp/urls/{url.replace("/","-").replace("?","-")}.json'
    # 判断url是否已经存在
    if os.path.exists(url_file):
        return 

    response = requests.get(url_prefix+url)
    if response.status_code == 200:
        # 根据html中的 meta  og:title 获取标题
        # 根据html中的 meta  og:description 获取描述
        html = response.text
        title = html.split('<meta property="og:title" content="')[1].split('" />')[0]
        description = html.split('<meta property="og:description" content="')[1].split('" />')[0]
        # 通过正则表达式读取所有的图片Url
        img_urls = re.findall('<img src="(.*?)"',html)
        # 移除?x-oss-process之后的
        img_urls = [re.sub('\?x-oss-process.*','',img_url) for img_url in img_urls]
        
        os.makedirs('tmp/urls',exist_ok=True)
        with open(url_file,'w') as f:
            url_info = {
                "url": url,
                "title": title,
                "description": description,
                "img_urls":img_urls
            }
            f.write(json.dumps(url_info))
            print(f"完成获取{url}的标题,描述和相关图片信息")
            return url_info
    else:
        print(url+" is error")

if __name__ == "__main__":
    with open('urls.txt','r') as f:
        urls = f.readlines()
        for url in urls:
            load_url_title(url)
