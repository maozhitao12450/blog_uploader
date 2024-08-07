# pip install pywin32
# pip install selenium
import win32clipboard
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
        