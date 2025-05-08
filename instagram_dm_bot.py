import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import getpass

# --- User credentials ---
username = input('Enter your Instagram username: ')
password = getpass.getpass('Enter your Instagram password: ')

# --- Selenium setup ---
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
# Uncomment the next line to run headless (no browser window)
# chrome_options.add_argument('--headless')

# Set path to chromedriver if not in PATH
# service = Service('path/to/chromedriver')
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

    # Handle 'Save Your Login Info?' popup
    try:
        not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now_btn.click()
        time.sleep(2)
    except NoSuchElementException:
        pass

    # Handle 'Turn on Notifications' popup
    try:
        notif_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        notif_btn.click()
        time.sleep(2)
    except NoSuchElementException:
        pass

    # --- Go to DMs ---
    driver.get('https://www.instagram.com/direct/inbox/')
    time.sleep(5)

    # --- Find unread messages ---
    # Unread chats have a blue dot (aria-label='Unread')
    unread_chats = driver.find_elements(By.XPATH, "//div[@aria-label='Unread']")
    if not unread_chats:
        print('No unread messages found.')
    else:
        print(f'Found {len(unread_chats)} unread message(s). Opening the first one...')
        unread_chats[0].click()
        time.sleep(3)

        # --- Read the last message ---
        messages = driver.find_elements(By.XPATH, "//div[@data-testid='message-container']")
        if messages:
            last_message = messages[-1].text
            print('Last message:', last_message)
        else:
            print('Could not read the last message.')

        # --- Reply with 'hi' ---
        try:
            textarea = driver.find_element(By.TAG_NAME, 'textarea')
            textarea.send_keys('hi')
            textarea.send_keys(Keys.RETURN)
            print('Replied with "hi".')
        except NoSuchElementException:
            print('Could not find the message input box.')

    print('Done.')
    time.sleep(5)
finally:
    driver.quit() 