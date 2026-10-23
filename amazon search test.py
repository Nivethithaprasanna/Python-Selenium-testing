from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Open Amazon India
    driver.get("https://www.amazon.in/")

    print("Page title:", driver.title)

    # Step 2: Find the search box
    search_box = wait.until(
        EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))
    )

    # Step 3: Search for a product
    search_box.send_keys("laptop")
    search_box.submit()

    # Step 4: Wait for search results
    results = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
        )
    )

    # Step 5: Verify the result
    if results.is_displayed():
        print("PASS: Amazon search results are displayed")
    else:
        print("FAIL: Search results are not displayed")

finally:
    driver.quit()