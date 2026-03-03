from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

input("如果看到百度页面，说明成功，按回车退出")
driver.quit()
