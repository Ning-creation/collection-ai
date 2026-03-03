from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException


# ========= 1. 启动浏览器 =========
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# ========= 2. 先访问知乎首页 =========
driver.get("https://www.zhihu.com")
time.sleep(3)

# ========= 3. 加载 cookies =========
with open("zhihu_cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# ========= 4. 刷新页面，让登录生效 =========
driver.refresh()
time.sleep(3)

# ========= 5. 进入话题页 =========
driver.get("https://www.zhihu.com/topic/19563107")
time.sleep(5)

# 滚动加载
for i in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# 抓链接
question_links = set()
elements = driver.find_elements("css selector", "a")

for e in elements:
    href = e.get_attribute("href")
    if href and "/question/" in href:
        question_links.add(href)

# 只保留前20个链接
question_links = list(question_links)[:20]

for link in question_links:
    print(link)

# 抓“回答”的函数
def get_answers_from_question(driver, max_answers=10):
    wait = WebDriverWait(driver, 10)
    answers = []

    # ========= 1. 尝试等待回答区 =========
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".QuestionAnswers-answers, .List")
            )
        )
    except TimeoutException:
        print("⚠️ 未检测到回答区，可能该问题暂无回答，跳过")
        return answers

    # ========= 2. 尝试点击「更多回答」 =========
    try:
        more_btn = driver.find_element(
            By.XPATH, "//button[.//span[contains(text(),'更多回答')]]"
        )
        driver.execute_script("arguments[0].click();", more_btn)
        time.sleep(2)
    except:
        pass

    # ========= 3. 找回答容器（兼容两种结构） =========
    try:
        answers_container = driver.find_element(
            By.CSS_SELECTOR, ".QuestionAnswers-answers"
        )
    except:
        answers_container = driver.find_element(
            By.CSS_SELECTOR, ".List"
        )

    scroll_count = 0
    while len(answers) < max_answers and scroll_count < 20:
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight",
            answers_container
        )
        time.sleep(2)
        scroll_count += 1

        # ========= 4. 展开阅读全文 =========
        expand_buttons = driver.find_elements(
            By.XPATH, "//button[.//span[contains(text(),'展开')]]"
        )
        for btn in expand_buttons:
            try:
                driver.execute_script("arguments[0].click();", btn)
            except:
                pass

        time.sleep(1)

        # ========= 5. 抓回答正文 =========
        answer_elements = driver.find_elements(
            By.CSS_SELECTOR, ".RichContent-inner"
        )

        for elem in answer_elements:
            text = elem.text.strip()
            if text and text not in answers:
                answers.append(text)

        print(f"已抓到回答数：{len(answers)}")

    return answers[:max_answers]

all_data = []   # 用来保存最终数据

for idx, q_url in enumerate(question_links, start=1):
    print(f"\n========== 正在处理第 {idx} 个问题 ==========")
    driver.get(q_url)
    time.sleep(3)

    # 抓问题标题
    title = driver.find_element("css selector", "h1").text

    # 抓问题描述
    try:
        detail = driver.find_element(
            "css selector", ".QuestionRichText"
        ).text
    except:
        detail = ""

    print("问题：", title)

    # 抓回答
    answers = get_answers_from_question(driver, max_answers=10)

    print(f"该问题共抓到 {len(answers)} 条回答")

    for ans in answers:
        all_data.append({
            "问题名": title,
            "问题具体内容": detail,
            "回答信息": ans
        })

# ========= 保存为 CSV =========
df = pd.DataFrame(all_data)

df.to_csv(
    "zhihu_topic_answers.csv",
    index=False,
    encoding="utf-8-sig"
)

print("✅ CSV 文件已保存：zhihu_topic_answers.csv")

