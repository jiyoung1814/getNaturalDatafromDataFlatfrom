from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
eng_mons = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# url = 'https://gml.noaa.gov/grad/solcalc/'
# driver = webdriver.Chrome("chromedriver.exe")
# driver.get(url)

class crawling_Az_El:
    def __init__(self, d, t):
        self.date = d.split('-')
        self.y = self.date[0]
        self.m = self.date[1]
        self.d = self.date[2]

        self.time = t.split(':')
        self.H = self.time[0]
        self.M = self.time[1]
        self.S = self.time[2]



        # 위도 경도 입력
        self.input_write('latbox', "36.851221")
        self.input_write('lngbox', "127.152924")
        self.input_write('tz', "Asia/Seoul", True)

        # 년
        self.input_write('yearbox', self.y)
        # 월
        self.input_write('mosbox', eng_mons[int(self.m)-1])
        # 일
        self.select_write('daybox', str(int(self.d)-1), True)

        # 시간
        self.input_write('hrbox', self.H, True)
        # 분
        self.input_write('mnbox', self.M, True)
        # 초
        self.input_write('scbox', self.S, True)
        time.sleep(0.1)

        self.az = self.getInputValue('azbox')
        self.el = self.getInputValue('elbox')


    def input_write(self, id, text, flag=False):
        elem = driver.find_element(By.ID, id)
        # elem.clear()
        elem.click()
        elem.send_keys(Keys.CONTROL + "A")  # ctrl + a 단축키
        elem.send_keys(text)

        if flag:
            elem.send_keys(Keys.ENTER)

    def select_write(self, id, text, flag=False):
        elem = driver.find_element(By.ID, id)
        select = Select(elem)
        select.select_by_index(text)
        time.sleep(0.5)

        if flag:
            elem.send_keys(Keys.ENTER)

    def getInputValue(self, id):
        elem = driver.find_element(By.ID, id)
        value = elem.get_attribute("value")
        return value