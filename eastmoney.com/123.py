from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import time
import json
import os

# 初始化 WebDriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)

def fetch_data(page_number):
    url = f'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery11230576826202197892_1722667992409&sortColumns=REPORT_DATE&sortTypes=-1&pageSize=10&pageNumber={page_number}&reportName=RPT_INDUSTRY_INDEX&columns=REPORT_DATE%2CINDICATOR_VALUE%2CCHANGE_RATE%2CCHANGERATE_3M%2CCHANGERATE_6M%2CCHANGERATE_1Y%2CCHANGERATE_2Y%2CCHANGERATE_3Y&filter=(INDICATOR_ID%3D%22EMI00662539%22)&source=WEB&client=WEB'
    driver.get(url)
    time.sleep(2)  # 等待页面加载
    response_text = driver.page_source
    json_data = response_text[response_text.find("{"):response_text.rfind("}")+1]
    return json_data

def parse_data(json_data):
    data = json.loads(json_data)
    result_data = data['result']['data']
    df = pd.DataFrame(result_data)
    return df

def save_to_excel(df, filename='energy_data.xlsx'):
    if not os.path.isfile(filename):
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Energy Data')
    else:
        existing_df = pd.read_excel(filename, sheet_name='Energy Data', engine='openpyxl')
        combined_df = pd.concat([existing_df, df]).drop_duplicates().reset_index(drop=True)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            combined_df.to_excel(writer, index=False, sheet_name='Energy Data')

def main():
    total_pages = 764  # 这是从响应中获取的总页数，可以动态获取
    for page_number in range(1, total_pages + 1):
        json_data = fetch_data(page_number)
        df = parse_data(json_data)
        save_to_excel(df)
        print(f"Page {page_number} saved.")
    
    driver.quit()

if __name__ == '__main__':
    main()
