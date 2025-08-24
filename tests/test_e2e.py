from selenium import webdriver
from selenium.webdriver.chrome.options import Options # 1. Import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LIVE_SERVER_URL = "http://127.0.0.1:5000"

def test_dashboard_interaction():
    # 2. Configure Chrome to detach and stay open after the script finishes
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # 3. Initialize the driver with the new options
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(f"{LIVE_SERVER_URL}/dashboard")

    wait = WebDriverWait(driver, 10)

    # Wait for the option to be ready and select it
    msft_option_xpath = "//select[@id='stock-select']/option[@value='MSFT']"
    wait.until(EC.element_to_be_clickable((By.XPATH, msft_option_xpath)))

    stock_select_element = driver.find_element(By.ID, "stock-select")
    select = Select(stock_select_element)
    select.select_by_value("MSFT")

    # Wait for the table to appear
    data_table = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )

    # Assertions to confirm the test passed
    assert data_table.is_displayed()
    assert "50-Day Avg." in data_table.text

    # We no longer need driver.quit() because of the "detach" option