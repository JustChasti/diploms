import codecs

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from modules.decorators import default_decorator
from config import page_load_timeout


@default_decorator('get page error')
def get_city_html(url, page_name, tag_type, tag_name):
    driver = webdriver.Remote(
        command_executor='http://chrome:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
    )
    data = driver.get(url)
    element = WebDriverWait(driver=driver, timeout=page_load_timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'heading'))
    )

    file = codecs.open(f'temp/{page_name}.html', "w", "utf−8")
    data = driver.page_source
    file.write(data)
    driver.quit()
