from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try:
    driver.get("https://www.amazon.in/")
    time.sleep(3)

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("mobile")
    search_box.submit()

    time.sleep(5)

finally:
    driver.quit()




