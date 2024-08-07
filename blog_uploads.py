# 加载环境变量
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from config import Config
config = Config()

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
            # 重新打开编辑页面
            driver.get(f"{config.UEESHOP_URL}/manage/plugins/blog/blog-v2-edit?id=0")
            
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
    print("所有文件上传完成")
if __name__ == '__main__':
    # 设置Chrome浏览器的选项
    upload_file()