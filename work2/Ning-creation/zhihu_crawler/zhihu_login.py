from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time

# ========= 1. 启动浏览器 =========
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# ========= 2. 打开知乎登录页 =========
driver.get("https://www.zhihu.com/signin")

input("请扫码登录知乎，看到头像后，按【回车】继续...")

# ========= 3. 保存 cookies =========
with open("zhihu_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ cookies 已保存")

# ========= 4. 进入话题页 =========
driver.get("https://www.zhihu.com/topic/19563107")
time.sleep(5)

input("如果你已经看到话题页面内容，按【回车】退出")
driver.quit()
