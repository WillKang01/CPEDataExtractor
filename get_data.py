from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import re
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def print_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"{'-'*15}STARTING {func.__name__}{'-'*15}")
        result = func(*args, **kwargs)
        print(f"{'+'*15}FINISHED {func.__name__}{'+'*15}")
        return result
    return wrapper

@print_decorator
def login():
    driver.get("https://courses.cpe.ubc.ca/new_analytics/enrollments")
    wait = WebDriverWait(driver, 30)
    wait.until(EC.url_contains('enrollments'))

@print_decorator

def filtering():
    button = driver.find_element(By.XPATH, "//button[@data-automation='AnalyticsPage__Show__Filters__Button']")
    button.click()
    
    # Wait until the dropdown menu is visible
    wait = WebDriverWait(driver, 10)
    dropdown_menu = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-automation="AnalyticsPage__Filter__Catalog"]')))
    dropdown_menu.click()
    
    # List of options you want to select
    options_to_select = ["CACE - ", "CNR - ", "CSRP - ", "CVA - ", "EFO - ", "FCM - ", "HTC - ", "FHM - ", " FSTB - ", "SMS - ", "TWS - ", "ZCBS - "]

    # Iterate over the options you want to select
    for option in options_to_select:
        # Type the name of the option to filter the dropdown menu
        dropdown_menu = driver.find_element(By.CSS_SELECTOR, 'input[data-automation="AnalyticsPage__Filter__Catalog"]')
        dropdown_menu.clear()
        dropdown_menu.send_keys(option)

        # Create the regex pattern
        pattern = re.escape(option) + '.+'
        # Wait until the desired option is visible and select it
        try:
            # Define a custom expected condition that waits for an element matching the regex
            print("TRY FIND")
            # wait.until(lambda driver: re.search(pattern, driver.page_source))
            time.sleep(5)
            print("FOUND")

            # Then send the ENTER key
            catalog_filter = driver.find_element(By.CSS_SELECTOR, 'input[data-automation="AnalyticsPage__Filter__Catalog"]')
            catalog_filter.send_keys(Keys.ARROW_DOWN)
            catalog_filter.send_keys(Keys.ENTER)

        except (TimeoutException, KeyboardInterrupt):
            print("DRIVER PAGE SOURCE IS", driver.page_source)
            print("OPTION NOT FOUND IN TIME", option)
            

        # Clear the input for the next iteration
        input("Press Enter in this terminal to continue")
        

    
    
if __name__ == "__main__":
    login()
    filtering()
    
