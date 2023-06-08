import os  # 创建文件夹, 文件是否存在
import time,datetime # time 计时
import pickle  # 保存和读取cookie实现免登陆的一个工具
from time import sleep
from selenium import webdriver  # 操作浏览器的工具
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options# 手机模式


class DaMai(object):
    def __init__(self):
        pass

    @staticmethod
    def get_damai_url():
        """获取大麦网链接

        Returns:
            _type_: _description_
        """
        return "https://www.damai.cn/"
    
    @staticmethod
    def get_login_url():
        """用户登录页面URL：大麦网

        Returns:
            _type_: _description_
        """
        return 'https://m.damai.cn/damai/minilogin/index.html?returnUrl=https%3A%2F%2Fm.damai.cn%2Fdamai%2Fmine%2Fmy%2Findex.html%3Fspm%3Da2o71.home.top.duserinfo&spm=a2o71.0.0.0'
    
    


class TicketInfo(object):
    """票价信息

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        pass

    

class DmTicketHelper(object):
    """大麦网抢票助手

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        self.chrome_option = None
        self.web_driver = None
        self.web_cookie = None
        self.ticket_url = None
        self.rob_year = None
        self.rob_month = None
        self.rob_day = None
        self.rob_price = None
        pass

    def get_cookie(self):
        if not os.path.exists("dm_cookie.pkl"):
            return None
        else:
            cookies = pickle.load(open('dm_cookie.pkl', 'rb'))
            return cookies
    
    def set_rob_time(self, year:str, month:str, day: str):
        """设置抓取的时间

        Args:
            year (str): _description_
            month (str): _description_
            day (str): _description_
        """
        self.rob_year = year
        self.rob_month = month
        self.rob_day = day
        pass


    def set_mobile_option(self, mobile_option: dict):
        """设置手机选项

        Args:
            mobile_option (dict): _description_
        """
        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_option.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_option.add_experimental_option("mobileEmulation", mobile_option)
        self.chrome_option.add_argument("--auto-open-devtools-for-tabs")

    def set_ticket_url(self, item_id:str):
        self.ticket_url = f'https://m.damai.cn/damai/detail/item.html?itemId={item_id}'


    def set_ticket_info(self, ticket_info:dict):
        """设置抢票的信息

        Args:
            ticket_info (dict): _description_
        """
        pass

    def set_rob_price(self, price_tag:str):
        self.rob_price = price_tag


    def set_begin_rob_time(self, time_info):
        """设置开始抢票的时间

        Args:
            time_info (_type_): _description_
        """
        pass


    def run(self):
        """ 执行抢票流程....
        true:  通知用户抢票成功
        false: 不通知用户 返回失败原因：
        """
        # 1. cookie跳转链接 实现登录跳转到抢票页面
        if self.web_driver is None:
            self.web_driver = webdriver.Chrome(executable_path=rf'D:/bin/chromedriver.exe',options=self.chrome_option)  # 当前浏览器驱动对象
        self.web_cookie = self.get_cookie()
        self.web_driver.maximize_window() 
        if self.web_cookie is None:
            print('需要重新获取cookie')
            self.web_driver.get(DaMai.get_login_url())
            while self.web_driver.title !="我的":
                sleep(1)
            pickle.dump(self.web_driver.get_cookies(), open('dm_cookie.pkl','wb'))
            print('保存cookie')
            self.web_driver.get(self.ticket_url)
        else:
            print("获取已有的cookie")
            self.web_driver.get(self.ticket_url)
            for cookie in self.web_cookie:
                cookie_dict = {
                'domain': '.damai.cn',  # 必须要有的, 否则就是假登录
                'name': cookie.get('name'),
                'value': cookie.get('value')
                }
                self.web_driver.add_cookie(cookie_dict)
        # 2. 下单
        print("进行选座购买按钮点击")
        time.sleep(1)
        self.web_driver.find_element(By.CLASS_NAME,'buy__button').click()
        time.sleep(5)
        print("进行选择日期的操作")
        calendar = self.web_driver.find_element(By.CLASS_NAME,"bui-calendar-handle-text")
        calendar_value = str(calendar.get_attribute('innerText'))
        tag_year_month = f"{self.rob_year}/{self.rob_month}"
        # todo： 增加切换日期的策略
        if calendar_value == tag_year_month:
            # 选择日期
            print("选择具体日子")
            day_item_list = self.web_driver.find_elements_by_class_name('day-item')
            for day_item in day_item_list:
                day_str = str(day_item.get_attribute('innerText'))
                if day_str == self.rob_day:
                    print(f"选中该日期{day_str}，进行点击")
                    day_item.click()
                    break
        time.sleep(3)
        print("选择具体的票价")


        # 3. 抢票


             
        



if __name__ == "__main__":
    dm_ticket = DmTicketHelper()
    dm_ticket.set_mobile_option({"deviceName": "iPhone 6"})
    dm_ticket.set_ticket_url('721747323601')
    dm_ticket.set_rob_time('2023','06','16')
    dm_ticket.run()

