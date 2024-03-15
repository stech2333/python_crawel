import datetime
import time, json, re
from time import sleep
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

DEBUG = False

def get_html(url):
    driver = get_driver(url)
    # 隐式等待
    driver.implicitly_wait(10)
    # 浏览器最大化
    driver.maximize_window()
    driver.get(url)
    if not DEBUG: time.sleep(random.uniform(3, 4))
    # 定位登录界面关闭按钮
    close_btn = driver.find_element(By.XPATH, "//button[@class='Button Modal-closeButton Button--plain']")
    # 点击登录界面关闭按钮
    close_btn.click()
    scroll_to_bottom(driver)
    answerElementList = driver.find_elements(By.CSS_SELECTOR, "#QuestionAnswers-answers .List-item .ContentItem")
    return answerElementList, driver


def get_driver(url):
    driver = webdriver.Edge(service=Service('msedgedriver.exe'))
    return driver


def scroll_to_bottom(driver):
    # 获取当前窗口的总高度
    js = 'return action=document.body.scrollHeight'
    # 初始化滚动条所在的高度
    height = 0
    # 当前窗口总高度
    currHeight = driver.execute_script(js)
    while height < currHeight:
        # 将滚动条调整至页面底端
        for i in range(height, currHeight, 100):
            driver.execute_script("window.scrollTo(0, {})".format(i))
            if not DEBUG: time.sleep(0.02)
        height = currHeight
        currHeight = driver.execute_script(js)
        if not DEBUG: time.sleep(3)


def get_answers(answerElementList, url):
    # 定义一个存储回答中的信息的数据表格
    answerData = pd.DataFrame(
        columns=(
            'question_title', 'answer_url', 'question_url', 'author_name', 'fans_count', 'created_time', 'updated_time',
            'comment_count',
            'voteup_count', 'content'))
    numAnswer = 0
    # 遍历每一个回答并获取回答中的信息
    for answer in answerElementList:
        dictText = json.loads(answer.get_attribute('data-zop'))
        question_title = dictText['title']  # 问题名称
        answer_url = answer.find_element(By.XPATH,
                                         "meta[@itemprop='url' and contains(@content, 'answer')]").get_attribute(
            'content')  # 获取回答的链接
        
        author_name = dictText['authorName']  # 回答作者名称
        fans_count = answer.find_element(By.XPATH, "*//meta[contains(@itemprop, 'followerCount')]").get_attribute(
            'content')  # 获取粉丝数量
        created_time = answer.find_element(By.XPATH, "meta[@itemprop='dateCreated']").get_attribute(
            'content')  # 获取回答的创建时间
        updated_time = answer.find_element(By.XPATH, "meta[@itemprop='dateModified']").get_attribute(
            'content')  # 获取回答最近的编辑时间
        comment_count = answer.find_element(By.XPATH, "meta[@itemprop='commentCount']").get_attribute(
            'content')  # 获取该回答的评论数量
        voteup_count = answer.find_element(By.XPATH, "meta[@itemprop='upvoteCount']").get_attribute(
            'content')  # 获取回答的赞同数量
        contents = answer.find_elements(By.TAG_NAME, "p")
        
        content = ''.join([content.text for content in contents])
        if not DEBUG: time.sleep(0.001)
        row = {'question_title': [question_title],
               'author_name': [author_name],
               'question_url': [url],
               'answer_url': [answer_url],
               'fans_count': [fans_count],
               'created_time': [created_time],
               'updated_time': [updated_time],
               'comment_count': [comment_count],
               'voteup_count': [voteup_count],
               'content': [content]
               }
        answerData = answerData.append(pd.DataFrame(row), ignore_index=True)
        numAnswer += 1
        print(f"[NORMAL] 问题：【{question_title}】 的第 {numAnswer} 个回答抓取完成...")
        if not DEBUG: time.sleep(0.2)
    answerData.to_csv('filename.csv', encoding='utf_8_sig')

    return answerData, question_title


if __name__ == '__main__':

    try:
        df_tmp = pd.read_csv('zhihu_result.csv')
        question_url_contained = set(df_tmp['question_url'].to_list())
        del df_tmp
        
    except Exception as e:
        print('no breakpoint:', e)
        question_url_contained = set()
        # 创建表头
        answerData_init = pd.DataFrame(
            columns=(
                'question_title', 'answer_url', 'question_url', 'author_name', 'fans_count', 'created_time', 'updated_time',
                'comment_count',
                'voteup_count', 'content'))
        answerData_init.to_csv(f'zhihu_result.csv', mode='a', encoding='utf_8_sig', index=False, header = True)


    url = input("输入问题的链接:")
    print('----------------------------------------')
    print('url:', url)

    url_num = int(url.split('/')[-1])
    try:
        if not DEBUG: time.sleep(random.uniform(60, 120))
        answerElementList, driver = get_html(url)
        print("[NORMAL] 开始抓取该问题的回答...")
        answerData, question_title = get_answers(answerElementList, url)
        print(f"[NORMAL] 问题：【{question_title}】 的回答全部抓取完成...")
        if not DEBUG: time.sleep(random.uniform(1, 3))
        question_title = re.sub(r'[\W]', '', question_title)
        filename = str(f"result-{datetime.datetime.now().strftime('%Y-%m-%d')}-{question_title}")

        answerData.to_csv(f'zhihu_result.csv', mode='a', encoding='utf_8_sig', index=False, header = False)
        print(f"[NORMAL] 问题：【{question_title}】 的回答已经保存至 {filename}.xlsx...")
        driver.close()
            
    except Exception as e:
        if not DEBUG: time.sleep(random.uniform(300, 400))
        print(e)
        print(f"[ERROR] 抓取失败...")
    

