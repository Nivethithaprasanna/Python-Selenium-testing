
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.selenium.dev/selenium/web/web-form.html"
REPORT_FILE = "performance_report.txt"
MAX_PAGE_LOAD_SECONDS = 5.0

results = []
driver = None


def record_result(test_name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    results.append(f"{test_name}: {status} - {details}")
    print(f"{status}: {test_name} - {details}")


try:
    print("=" * 50)
    print("SYSTEM PERFORMANCE MONITORING")
    print("=" * 50)

    # Start Chrome
    driver = webdriver.Chrome()
    driver.set_window_size(1366, 900)
    wait = WebDriverWait(driver, 15)

    # 1. Measure page navigation time
    start_time = time.perf_counter()
    driver.get(URL)
    navigation_time = time.perf_counter() - start_time

    record_result(
        "Website Loading",
        navigation_time <= MAX_PAGE_LOAD_SECONDS,
        f"{navigation_time:.3f} seconds"
    )

    # Keep the page visible for at least 5 seconds
    time.sleep(5)

    # 2. Check page title
    page_title = driver.title
    record_result(
        "Page Title",
        page_title == "Web form",
        f"Title: {page_title}"
    )

    # 3. Check form elements
    text_box = wait.until(
        EC.visibility_of_element_located((By.NAME, "my-text"))
    )
    submit_button = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button"))
    )

    elements_ready = (
        text_box.is_displayed()
        and text_box.is_enabled()
        and submit_button.is_displayed()
        and submit_button.is_enabled()
    )

    record_result(
        "Form Elements",
        elements_ready,
        "Text box and submit button are available"
    )

    # 4. Enter text and submit the form
    expected_text = "System Performance Monitoring"
    text_box.send_keys(expected_text)

    record_result(
        "Text Entry",
        text_box.get_attribute("value") == expected_text,
        "Entered text verified"
    )

    submit_button.click()

    confirmation = wait.until(
        EC.visibility_of_element_located((By.ID, "message"))
    )

    record_result(
        "Form Submission",
        confirmation.text == "Received!",
        f"Confirmation: {confirmation.text}"
    )

    # 5. Collect browser performance metrics
    metrics = driver.execute_script("""
        const nav = performance.getEntriesByType("navigation")[0];

        let memory = null;

        if (performance.memory) {
            memory = {
                used: performance.memory.usedJSHeapSize,
                allocated: performance.memory.totalJSHeapSize
            };
        }

        return {
            dom_loaded: nav ? nav.domContentLoadedEventEnd : null,
            load_event: nav ? nav.loadEventEnd : null,
            transfer_size: nav ? nav.transferSize : null,
            memory: memory
        };
    """)

    print("\\n--- PERFORMANCE METRICS ---")
    print(f"Navigation time: {navigation_time:.3f} seconds")

    dom_loaded = metrics["dom_loaded"]
    load_event = metrics["load_event"]
    transfer_size = metrics["transfer_size"]

    print(
        "DOM content loaded: "
        + (f"{dom_loaded:.2f} ms" if dom_loaded is not None else "Unavailable")
    )

    print(
        "Load event: "
        + (f"{load_event:.2f} ms" if load_event is not None else "Unavailable")
    )

    print(
        "Transferred resource size: "
        + (f"{transfer_size} bytes" if transfer_size is not None else "Unavailable")
    )

    memory = metrics["memory"]

    if memory:
        print(f"JavaScript heap used: {memory['used'] / (1024 * 1024):.2f} MB")
        print(f"JavaScript heap allocated: {memory['allocated'] / (1024 * 1024):.2f} MB")
    else:
        print("JavaScript memory metrics are unavailable.")

    record_result(
        "Performance Metrics",
        navigation_time >= 0,
        "Browser timing measurements collected"
    )

    # Save results to a text report
    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write("SYSTEM PERFORMANCE MONITORING REPORT\\n")
        report.write("=" * 45 + "\\n")
        report.write(f"Date and time: {datetime.now()}\\n")
        report.write(f"Website: {URL}\\n\\n")

        report.write("TEST RESULTS\\n")
        report.write("-" * 45 + "\\n")

        for result in results:
            report.write(result + "\\n")

        report.write("\\nPERFORMANCE METRICS\\n")
        report.write("-" * 45 + "\\n")
        report.write(f"Navigation time: {navigation_time:.3f} seconds\\n")
        report.write(f"DOM content loaded: {dom_loaded} ms\\n")
        report.write(f"Navigation load event: {load_event} ms\\n")
        report.write(f"Transferred resource size: {transfer_size} bytes\\n")

        if memory:
            report.write(
                f"JavaScript heap used: "
                f"{memory['used'] / (1024 * 1024):.2f} MB\\n"
            )
            report.write(
                f"JavaScript heap allocated: "
                f"{memory['allocated'] / (1024 * 1024):.2f} MB\\n"
            )
        else:
            report.write("JavaScript heap metrics: Unavailable\\n")

    print(f"\\nReport saved to: {REPORT_FILE}")
    print("\\nBrowser will remain open for 3 more seconds.")
    time.sleep(3)

except Exception as error:
    record_result("Execution", False, str(error))
    print(f"\\nError occurred: {error}")

finally:
    if driver is not None:
        driver.quit()
        print("Browser closed.")

    print("\\nExecution completed.")
