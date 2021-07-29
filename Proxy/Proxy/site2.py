from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import fake_useragent
from bs4 import BeautifulSoup
from create_db import add_to_db
# proxylist = []
# portlist = []

user_agent = fake_useragent.UserAgent().random
url = 'https://geonode.com/free-proxy-list'
driver = webdriver.Chrome()
# options
options = webdriver.ChromeOptions()
# adding user-agent
options.add_argument(f'user-agent={user_agent}')
driver.maximize_window()

def help_parse():
    soup = BeautifulSoup(driver.page_source, 'lxml')
    rows = soup.find_all('tr', class_='freeProxyTable_freeProxyTableItem__3R6OM')

    for i in range(len(rows)):
        row = rows[i].find_all('td', class_='freeProxyTable_freeProxyTableRow__2dzS1')
        # proxylist.append(row[0].text)
        # portlist.append(row[1].text)
        add_to_db(row[0].text,row[1].text)
    button = driver.find_element_by_css_selector(
        '#__next > div > div > main > div > div.MuiGrid-root.freeProxy_container__'
        '1pksc.MuiGrid-container.MuiGrid-wrap-xs-nowrap.MuiGrid-align-items-xs-center.MuiGrid-justify-xs-space-between'
        ' > div.freeProxyTable_freeProxyBlock__1_HQh > div > div.freeProxyTable_tableFooterWrapper__2xtW0'
        ' > div:nth-child(2) > div:nth-child(3) > svg > path')
    # нажатие стрелки мышкой
    ActionChains(driver).move_to_element(button).click(button).perform()
    time.sleep(3)

def parse2():
    try:
        driver.get(url)
        time.sleep(5)

        pages = driver.find_element_by_xpath('/html/body/div[1]/div/div/main/div/div[2]/div[2]/div/div[2]/div[2]/label/select')
        buf = pages.text.split('\n')
        max_page = int(buf[-1])

        for i in range(max_page):
            help_parse()
        # print(proxylist)
        # print(portlist)
    except Exception:
        print(Exception)
    finally:
        driver.close()
        driver.quit()
