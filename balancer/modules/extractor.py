from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import page_load_timeout


def extract(url, hostname, tag_type, tag_name):
    driver = webdriver.Remote(
        command_executor=f'http://{hostname}:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
    )
    data = driver.get(url)
    if tag_type == 'CLASS_NAME':
        element = WebDriverWait(driver=driver,
                                timeout=page_load_timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, tag_name))
        )
    elif tag_type == 'CSS_SELECTOR':
        element = WebDriverWait(driver=driver,
                                timeout=page_load_timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, tag_name))
        )
    elif tag_type == 'XPATH':
        element = WebDriverWait(driver=driver,
                                timeout=page_load_timeout).until(
            EC.presence_of_element_located((By.XPATH, tag_name))
        )
    else:
        raise ValueError(tag_type)
    data = driver.page_source
    driver.quit()
    return data
