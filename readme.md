# 为Ueeshop一键生产blog
## 0. python 版本： 3.10.14
## 1. 复制config.json.template改名为config.json，并填写相关信息
## 2. 安装conda, ollama(非必须)
## 3. 创建urls.txt文件，内容为网店所有的url
    > 文件格式为url列表， 每行一个url,例子如下： 
    ```
        /products/df005
        /products/306
        /products/618a
    ```
## 3. 执行 start_create_blog.ps1