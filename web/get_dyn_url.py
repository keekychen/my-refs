from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

chrome_options = webdriver.ChromeOptions()
# 注意：有些场景用无头模式会缺少资源，比如某些URL获取不到
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--auto-open-devtools-for-tabs')
chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
chrome_options.add_argument("--ignore_ssl")
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')

selenium_options = {
    'verify_ssl': False,
    'connection_timeout': None,
    # 代理地址
    # 'proxy': {    #     'http': 'http://127.0.0.1:8001',    #     'https': 'http://127.0.0.1:8001',    #     'verify_ssl': False,    # },}

chrome_options.set_capability('goog:loggingPrefs', {"performance": "ALL", 'browser': 'ALL', 'server': 'ALL'})
chrome_options.set_capability('acceptInsecureCerts', True)
chrome_options.set_capability('PageLoadStrategy', None)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options,
    seleniumwire_options=selenium_options,
)

url = "https://yhz.me"

url_list = list([])
# 最大化窗口，有些场景会判断窗口大小决定加载什么资源
driver.maximize_window()
driver.get(url)

try:
    # 自行评估3秒能否加载完所有资源并进行适当设置
    wait = WebDriverWait(driver, 3, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
    # //yhz 为一个虚拟的元素，等一个不存在的元素出现直到超时
    elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//yhz")))
except TimeoutException:
    for request in driver.requests:
        if request.response:
            url_list.append(request.url)
finally:
    driver.quit()

print(*url_list, sep="\n")
