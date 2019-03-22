
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

TB_LOGIN_URL = 'https://login.taobao.com/'
CHROME_DRIVER = 'D:/chromedriver/chromedriver.exe'


class SessionException(Exception):
    '''
    会话异常类
    '''

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class SessionDriver:

    def __init__(self):
        self.browser = None

    def get_session(self, username, password):
        '''
        获取cookies
        :param username:
        :param password:
        :return: cookies
        '''
        cookies = {}
        try:
            self.__init_browser()
            self.__switch_to_password_mode()
            time.sleep(1)
            self.__switch_to_weibologin()
            time.sleep(4)
            self.__write_username(username)
            time.sleep(0.5)
            self.__write_password(password)
            time.sleep(0.5)
            self.__submit()
            # 提取cookie
            for cookie in self.browser.get_cookies():
                cookies[cookie['name']] = cookie['value']
        finally:
            self.__destroy_browser()
        return cookies

    def __switch_to_password_mode(self):
        '''
        切换到密码模式，通过密码模式找到微博登录窗口
        :return:
        '''
        if self.browser.find_element_by_id('J_QRCodeLogin').is_displayed():
            self.browser.find_element_by_id('J_Quick2Static').click()



    def __switch_to_weibologin(self):
        '''
        切换微博登录（由于主页面有滑动模块）
        :return:
        '''
        self.browser.find_element_by_xpath('//*[@class="weibo-login"]').click()

    def __write_username(self, username):
        """
        输入账号
        :param username:
        :return:
        """
        self.browser.find_element_by_name('username').send_keys(username)

    def __write_password(self, password):
        '''
        输入密码
        :param password:
        :return:
        '''
        password_input_element = self.browser.find_element_by_name('password')
        password_input_element.clear()
        password_input_element.send_keys(password)

    def __submit(self):
        '''
        提交登录
        :return:
        '''
        self.browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()
        time.sleep(3)
        if self.__is_element_exist("#J_Message"):
            error_message_element = self.browser.find_element_by_css_selector('#J_Message > p')
            error_message = error_message_element.text
            raise SessionException('登录出错'+ error_message)

    def __init_browser(self):
        '''
        初始化selenium浏览器
        :return:
        '''
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument('--proxy-server=http://127.0.0.1:8877')
        # self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)
        self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER)
        self.browser.implicitly_wait(3)
        self.browser.maximize_window()
        self.browser.get(TB_LOGIN_URL)

    def __destroy_browser(self):
        '''
        销毁selenium浏览器
        :return:
        '''
        if self.browser is not None:
            pass
            # self.browser.quit()

    def __is_element_exist(self, selector):
        '''
        检查是否存在指定元素,是否跳转淘宝主页
        :param selector:
        :return:
        '''
        try:
            self.browser.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False

