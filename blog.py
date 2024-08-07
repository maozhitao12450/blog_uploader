
import re
import requests
# from WindowProxyInfo import ProxyServer
# ProxyServer().setEnv()

# 读取images.txt
import datetime
import os
import re
import json

from config import Config
config = Config()

os.makedirs("output", exist_ok=True)
urls = None
with open('urls.txt', 'r') as f:
    urls = f.readlines()

def get_url_desc(index,url):
    url = url.strip()
    url_file = f'tmp/urls/{url.replace("/","-").replace("?","-")}.json'
    if os.path.exists(url_file):
        with open(url_file, 'r') as f:
            objstr = f.read()
            return (str(index) + ": "+objstr) , json.loads(objstr)
    else:
        # 说明没有下载到文件，那么触发生产
        import loadUrlTitle
        if loadUrlTitle.load_url_title(url):
            return get_url_desc(index,url)
        else :
            # 删除urls.txt中的这一行
            with open('urls.txt', 'r') as f:
                lines = f.readlines()
            with open('urls.txt', 'w') as f:
                for line in lines:
                    if line.strip() != url:
                        f.write(line)
            print("error url: " + url)
            return None,None

def getUrlDescribe(urls):
    # 读取urls
    result = []
    result_obj = []
    for index,url in enumerate(urls):
        url = url.strip()
        url_file = f'tmp/urls/{url.replace("/","-").replace("?","-")}.json'
        if os.path.exists(url_file):
            with open(url_file, 'r') as f:
                objstr = f.read()
                result.append(str(index) + ": "+objstr)
                result_obj.append(json.loads(objstr))
        else:
            result_temp , result_obj_temp =  get_url_desc(index,url)
            if result_temp is None:
                continue
            result.append(result_temp)
            result_obj.append(result_obj_temp)
    return result,result_obj


def getImagesDescribe(images):
    # 读取images
    result = []
    for image in images:
        url = image.strip()
        url_file = url.replace("https://ueeshop.ly200-cdn.com/u_file/UPAZ/UPAZ166/","").replace("/","-").replace("?","-").replace("\n","")
        url_file = f'tmp/images-description/{url_file}'.split(".")[0] + ".json"
        if os.path.exists(url_file):
            with open(url_file, 'r') as f:
                result.append(f.read()) 
    return result


nowdate = datetime.datetime.now().strftime('%Y-%m-%d')

BLOG_PORMOT = f'''
i have give you urls infos.
you must write a Furniture html Advertisement blog use First person view that includes all 5 urls.url,just return the div block
and chose all 5 images from urls.img_urls, every images url only use once.
you cant change any url or image.
image can jump back the url when click.
now date is : {nowdate}
'''

# 随机读取 5条图片和5条url
import random

def get_blog_prompts():
    # 输出5条图片和5条url,到随机名称.txt
    random.shuffle(urls)
    urldescribe,urldescribe_obj = getUrlDescribe(urls[:5])
    # 整理prompt
    response_text = f'''
{BLOG_PORMOT}
the urls infos: 
{json.dumps(urldescribe, ensure_ascii=False)}'''
    return {
        "response_text": response_text,
        "urldescribe": urldescribe,
        "urldescribe_obj": urldescribe_obj,
    }

from openai import OpenAI

def generate_blog(prompt:str,urldescribe,client:OpenAI,model:str):
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content":"you are a Senior Frontend javascript Developer, you will return javascript code result, you will only return the div block. At least 3000 words.dont change picture size"},
            {"role": "user", "content": f"the urls info is: " + json.dumps(urldescribe, ensure_ascii=False)},
            {"role": "user", "content": BLOG_PORMOT},
        ],
        max_tokens=30000,
        stream=True,
    )
    return stream

def get_blog_SEO_info(client:OpenAI,model:str,context:str):
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role":"user","content": "a html blog is:  ```html \n" + context + "\n```"},
            {"role": "system", "content":f"you are an SEO professional,you will return result like this: {{title: 'the seo title', description: 'the seo description', keywords: 'the seo keywords',url: 'the seo url'}}"},
            {"role": "user", "content": "i have give you a html blog about Furniture, you will return SEO-related attributes: title, description,keywords,url in json format,just return the json only, Do not let me replace any words."},
        ],
        stream=True,
    )
    return stream

def load_json_str_from_str(str_message:str):
    # 正则表达式抽取文本中的json数据, 例如：{"title": "the seo title", "description": "the seo description", "keywords": "the seo keywords", "url": "the seo url"}
    str_message = str_message.replace('\n', '')
    json_str = re.findall(r'\{.*?\}', str_message)
    if len(json_str) > 0:
        try:
            return json.loads(json_str[0])
        except:
            return None
    else:
        return None

def create_blog(i):
    prompt = get_blog_prompts()
    urldescribe = prompt.get("urldescribe")
    urldescribe_obj = prompt.get("urldescribe_obj")
    # 遍历 urldescribe , 
    image_urls = []
    urls_bak = []
    for obj in urldescribe_obj:
        image_urls = image_urls + obj.get("img_urls")
        urls_bak.append(obj.get("url"))
    prompt = prompt.get("response_text")
    
    # 当前时间
    print(f'正在生成第{i+1}篇博客')
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d%H%M%S")
    # 本地生成看看 gemma2:27b   mistral-nemo
    response_text = None
    client = None
    while True:
        # 本地生产
        # client = OpenAI(base_url= "http://localhost:11434/v1" ,api_key= "ollama")
        # temp_model = model
        # 使用chatgpt生成
        client = OpenAI(base_url= config.BLOG_GENERATE_API_BASE ,api_key= config.BLOG_GENERATE_API_KEY)
        temp_model = config.BLOG_GENERATE_API_MODEL
        print("---------------------------------------------------------------------")
        # qwen2:7b 效果还不错
        # mistral:latest X
        # qwen2:0.5b X
        # gemma2:27b X 
        # mistral-nemo:latest X
        # llama3.1:latest X
        # gemma2:latest 还行
        # llava:7b X
        stream = generate_blog(prompt=prompt,urldescribe=urldescribe,client = client,model=temp_model)
        response_text = ""
        sign = True
        url_temp = ""
        count= 0
        try:
            for chunk in stream:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    response_text += chunk_content
                    if len(response_text) > 200 and ("<div" not in response_text and "<html" not in response_text):
                        stream.close()
                        sign = False
                        print("返回结果不完整，重新生成")
                        break
                    # 如果出现换行符
                    if "\n" in chunk_content:
                        url_temp = ""
                    else:
                        url_temp += chunk_content
                    if "www.example" in response_text or "example.com" in response_text:
                        stream.close()
                        sign = False
                        print("出现了没用的东西")
                        break
          
                    # 查找image和urls,如果找到且不能访问则中断生产
                    if url_temp and ("<img" in url_temp and "src" in url_temp):
                        images = re.findall(r'<img src="(.*?)"', url_temp)
                        if len(images) > 0:
                            url_temp = ""
                        try:
                            # 如果图片不能访问则中断生产
                            for image in images:
                                if "/" not in image:
                                    stream.close()
                                    sign = False
                                    print("图片异常")
                                    break
                                if "http" not in image:
                                    image = "http:" + image
                                if not requests.get(image).ok:
                                    # 从 image_urls 随机取一条
                                    random_image_url = random.choice(image_urls)
                                    # 替换 response_text 中的 image_url
                                    response_text = response_text.replace(image, random_image_url)
                            if not sign:
                                break
                        except :
                            # 从 image_urls 随机取一条
                            random_image_url = random.choice(image_urls)
                            # 替换 response_text 中的 image_url
                            response_text = response_text.replace(image, random_image_url)
                            
                    if url_temp and ("<a" in url_temp and "href" in url_temp):
                        urls = re.findall(r'<a href="(.*?)"', url_temp)
                        if len(urls) > 0:
                            url_temp = ""
                        try:
                            # 如果图片不能访问则中断生产
                            for url in urls:
                                if "/" not in url:
                                    stream.close()
                                    sign = False
                                    print("url异常")
                                    break
                                if not requests.get(f"{config.UEESHOP_URL}/{url}").ok:
                                    response_text = response_text.replace(url, random.choice(urls_bak))
                            if not sign:
                                break
                        except:                                    
                            response_text = response_text.replace(url, random.choice(urls_bak))

                    print(chunk_content,end="")
            if not re.findall(r'<img', response_text) or not re.findall(r'<a', response_text):
                sign = False
            # 正则表达式读取第一个<div和最后一个</div> 之间的内容
            search_result = re.search(r'<div(.*?)>(.*?)</div>', response_text, re.S)
            if search_result:
                response_text = search_result.group(0)
                break
            else:
                print("未找到匹配的div")
                sign = False
            # 如果没有图片或者没有url则中断生产
            if sign:
                break
        finally:
            stream.close()
            client.close()
    
    response_json = ""
    while True:
        client = OpenAI(base_url= config.SEO_GENERATE_API_BASE ,api_key= config.SEO_GENERATE_API_KEY)
        stream = get_blog_SEO_info(client, config.SEO_GENERATE_API_MODEL, response_text)
        seo_info = ""
        sign = True
        try:
            for chunk in stream:
                chunk_content = chunk.choices[0].delta.content
                seo_info += chunk_content
                print(chunk_content,end="")
            # 正则表达式抽取文本中的json数据
            response_json = load_json_str_from_str(seo_info)
            if response_json:
                # 校验字段是否存在
                check_words = ["title", "description","keywords","url"]
                if all(word in response_json for word in check_words):
                    # url仅取最后一个/后的
                    response_json["url"] = response_json["url"].split("/")[-1]
                    break
        finally:
            stream.close()
            client.close()

                
    # 打印生产耗时
    cost_time = datetime.datetime.now() - now
    print(f'第{i+1}篇博客生成耗时：{cost_time}')
    if len(response_text) > 1000:
        with open(f'output/blog-{date}.json', 'w' ,encoding="utf8") as f:
                f.write(json.dumps({
                        "html": response_text,
                        "seo": response_json,
                    }, ensure_ascii=False))
                f.write('\n')

if __name__ == '__main__':
    # python blog.py 3
    import sys
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    else:
        num = 1
    for i in range(num):
        create_blog(i)