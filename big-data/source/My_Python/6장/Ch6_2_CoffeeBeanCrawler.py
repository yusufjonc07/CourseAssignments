from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

from selenium import webdriver
import time

#[CODE 1]
def CoffeeBean_store(result):
    CoffeeBean_URL = "https://www.coffeebeankorea.com/store/store.asp"
    wd = webdriver.Chrome()
    
    wd.get(CoffeeBean_URL)
    time.sleep(2)

    for i in range(1, 400):   # iterate possible store IDs
        try:
            wd.execute_script(f"storeView({i});")
            time.sleep(1)

            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')

            store_name_tag = soup.select_one("div.store_txt > h2")
            if not store_name_tag:
                continue

            store_name = store_name_tag.get_text(strip=True)

            store_info = soup.select("div.store_txt table.store_table td")

            if len(store_info) < 4:
                continue

            store_address = store_info[2].get_text(strip=True)
            store_phone = store_info[3].get_text(strip=True)

            print(store_name)

            result.append([store_name, store_address, store_phone])

        except:
            continue

    wd.quit()
    
#[CODE 0]
def main():
    result = []
    print('CoffeeBean store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    CoffeeBean_store(result)  #[CODE 1]
    
    CB_tbl = pd.DataFrame(result, columns=('store', 'address','phone'))
    CB_tbl.to_csv('CoffeeBean.csv', encoding='cp949', mode='w', index=True)
    print('CoffeeBean.csv  파일저장 완료 >>>>>>>>>>>>>>>>>')

if __name__ == '__main__':
     main()
