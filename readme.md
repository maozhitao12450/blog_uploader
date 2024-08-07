## 生成blog一般流程
1. 准备以下文件
    1.1 urls.txt 下载url列表，举例： /products/618a
2. 执行url信息解析代码
``` shell
python loadUrlTitle.py
```
3. 执行blog.py调用大模型生产blog
``` shell
python blog.py
```
4. 执行blog_uploads.py上传
``` shell
python blog_uploads.py
```
### 完整脚本
``` shell 
python loadUrlTitle.py
python blog.py
python blog_uploads.py
```
