import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

# --- User credentials ---
username = "manga_furru_creator"
password = "Mudassir123@"

# --- Selenium setup ---
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
# Uncomment the next line to run headless (no browser window)
# chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

try:
    # --- Log in to Instagram ---
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)

    # Accept cookies if prompted
    try:
        cookies_btn = driver.find_element(By.XPATH, "//button[text()='Only allow essential cookies']")
        cookies_btn.click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # Enter username and password
    user_input = driver.find_element(By.NAME, 'username')
    pass_input = driver.find_element(By.NAME, 'password')
    user_input.send_keys(username)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Handle 'Save your login info?' popup
    try:
        # Try button first
        not_now_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Not now' or text()='Not Now']"))
        )
        not_now_btn.click()
        time.sleep(2)
    except Exception as e:
        print("No 'Not now' button found or could not click it:", e)
        # Debug: print all elements with 'Not now' text
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Not now') or contains(text(), 'Not Now')]")
        print(f"Found {len(elements)} elements with 'Not now' text.")
        for el in elements:
            print(f"Tag: {el.tag_name}, Text: {el.text}, Displayed: {el.is_displayed()}")

    # Handle 'Turn on Notifications' popup
    try:
        notif_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        notif_btn.click()
        time.sleep(2)
    except NoSuchElementException:
        pass

    print('Logged in to Instagram. You can now give further instructions.')
    input('Press Enter to exit...')
finally:
    driver.quit() 