# 调试模式打开google1浏览器访问 UEESHOP_URL/manage/plugins/blog/blog-v2?start_upload_auto=true
import time
# 加载环境变量
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select

from config import Config
config = Config()

import win32clipboard
def install_monkey(driver:webdriver.Chrome = None):
    # chrome_options.add_extension(r'tampermonkey_stable.crx')
    # 加载Tampermonkey脚本
    # 打开设置页
    driver.get("chrome-extension://dhdgffkkebhmkfjojejmpbldmpobfkfo/options.html")
    
    print(driver.current_url)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#select_TW4hD19jb25maWdNb2Rl_dd')))
    
    # 设置select值为100
    select_element = driver.find_element(By.CSS_SELECTOR,'#select_TW4hD19jb25maWdNb2Rl_dd')
    select = Select(select_element)
    select.select_by_value('100')
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#select_QbgaLLuLDCH9l9zY3JpcHRfZmlsZV9hY2Nlc3M_dd')))
    
    time.sleep(1)
    
    # 设置启用可以访问本地文件
    select_element = driver.find_element(By.CSS_SELECTOR,'#select_QbgaLLuLDCH9l9zY3JpcHRfZmlsZV9hY2Nlc3M_dd')
    select = Select(select_element)
    select.select_by_value('all')
    
    time.sleep(1)
    
    # 点击保存
    driver.find_element(By.CSS_SELECTOR, '#input_dW5kZWZpbmVkX3RhYmxlX2lXaGZjMlZqZFhKcGRIa19jb250ZW50_Save').click()
    # 等待1秒
    time.sleep(1)
    
    # 载入脚本
    paste_text_to_editor(driver)
    
    time.sleep(1)

def paste_text_to_editor(driver:webdriver.Chrome = None,paths = ["monkey.js","monkey_2.js"]):
    for path in paths:
        # 点击 新增脚本
        driver.find_element(By.CSS_SELECTOR, '#div_dGFiX25ldy11c2VyLXNjcmlwdF9jb250ZW50bWFpbg').click()
        
        # 将文本存入剪贴板
        script = open(path, 'r', encoding='utf-8').read()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, script)
        win32clipboard.CloseClipboard()
        
        # 等待编辑页面加载
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#div_bmV3LXVzZXItc2NyaXB0X2VkaXQ')))
        time.sleep(1)
        
        first_row = driver.find_element(By.XPATH,'//*[@id="div_bmV3LXVzZXItc2NyaXB0X2VkaXQ"]/div/div/div[6]/div[1]/div/div/div/div[5]/div/pre')
        first_row.click()
        time.sleep(1)
        # 使用ActionChains模拟按下Ctrl+A , Ctrl+V
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        # save 
        actions.key_down(Keys.CONTROL).send_keys("s").key_up(Keys.CONTROL).perform()
        
def to_bmp(s):
    return ''.join(c if ord(c) < 0xFFFF else '' for c in s)

def upload_file():
    # 设置Chrome浏览器的选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无界面模式
    chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_extension(r'tampermonkey_stable.crx')
    
    # 启动Chrome浏览器
    driver = webdriver.Chrome(options=chrome_options)
    # 输出当前地址栏
    print(driver.current_url)
    # 打开网页
    # driver.get(f"{config.UEESHOP_URL}/manage/plugins/blog/blog-v2-edit?id=0&start_upload_auto=true")
    driver.get(f"{config.UEESHOP_URL}/manage/plugins/blog/blog-v2-edit?id=0")

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.submit')))
    
    # 如果页面是登录页面则执行登录
    if "login" in driver.current_url:
        # 输入用户名和密码
        username = driver.find_element(By.CSS_SELECTOR, 'input[name="MobilePhone"]')
        password = driver.find_element(By.CSS_SELECTOR, 'input[name="Password"]')
        
        username.send_keys(config.UEESHOP_LOGIN_USER)
        password.send_keys(config.UEESHOP_LOGIN_PASSWORD)

        # 点击登录按钮
        login_button = driver.find_element(By.CSS_SELECTOR, 'input.submit')
        login_button.click()
    
    
    # 读取output下的所有json文件，除了blog_connect.json
    os.makedirs("output", exist_ok=True)
    for filename in os.listdir("output"):
        if filename != "blog_connect.json" and filename.endswith(".json"):
            # 打开json文件
            blog_info = json.load(open(os.path.join("output", filename), "r", encoding="utf-8"))
            seo = blog_info.get("seo")
            print("正在上传：", filename)
            form_prefix = "#edit_form > div.left_container > div > div > div:nth-child"
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, form_prefix +"(2) input")))
            driver.find_element(By.CSS_SELECTOR, form_prefix +"(2) input").send_keys(seo.get("title"))
            driver.find_element(By.CSS_SELECTOR, ".unit_input .box_input").send_keys(seo.get("title"))
            driver.find_element(By.CSS_SELECTOR, form_prefix +"(3) textarea").send_keys(seo.get("description"))
            driver.find_element(By.CSS_SELECTOR, ".unit_input .box_textarea").send_keys(seo.get("description"))
            driver.find_element(By.CSS_SELECTOR, form_prefix +"(4) input").send_keys("Alice")
            driver.find_element(By.CSS_SELECTOR, form_prefix +'(5) button[title="源代码"][aria-label="源代码"]').click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="保存"].tox-button')))
            driver.find_element(By.CSS_SELECTOR, '.tox-dialog__content-js .tox-textarea').send_keys(to_bmp(blog_info.get("html")))
            driver.find_element(By.CSS_SELECTOR, 'button[title="保存"].tox-button').click()
            input = driver.find_element(By.CSS_SELECTOR, 'div[data-name="keyword"] .option_selected input')
            # 触发div的点击事件
            driver.execute_script('arguments[0].click();', input)
            input_real = driver.find_element(By.CSS_SELECTOR, '#edit_form > div.right_container > div.global_container.global_seo_box > div:nth-child(4) > div > div > div > div.option_selected.option_focus > input')
            input_real.send_keys(seo.get("keywords") + ",")
            # 发布按钮
            driver.find_element(By.CSS_SELECTOR, "#blog_inside > div.rows.fixed_btn_submit > div > div > input.btn_global.btn_submit.btn_save_publish").click()
            # 等待发布完成
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#blog > div.inside_table.pt0.radius > div.list_menu > ul > li > a")))
            print("上传完成：", filename)
            # 删除文件
            os.remove(os.path.join("output", filename))
            # 重新打开编辑页面
            driver.get(f"{config.UEESHOP_URL}/manage/plugins/blog/blog-v2-edit?id=0")
    print("所有文件上传完成")
if __name__ == '__main__':
    # 设置Chrome浏览器的选项
    upload_file()