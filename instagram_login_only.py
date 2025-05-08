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
    
    # Wait 10 seconds before proceeding
    time.sleep(4)
    
    # Find and click the 'Messages' button in the sidebar
    try:
        messages_btn = driver.find_element(By.XPATH, "//a[.//span[text()='Messages']]")
        messages_btn.click()
        print("Clicked on the 'Messages' button.")
    except Exception as e:
        print("Could not find or click the 'Messages' button:", e)
    

    time.sleep(1)
    
    # After navigating to DMs, handle the 'Turn on Notifications' popup
    try:
        notif_btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Not Now' or text()='Not now']"))
        )
        notif_btn.click()
        print("Clicked 'Not Now' on notifications popup.")
        time.sleep(2)
    except Exception as e:
        print("No 'Not Now' button found for notifications popup or could not click it:", e)


    time.sleep(5)
    # Wait for the DM list to load

    # Find all DM items
    dm_items = driver.find_elements(By.XPATH, "//div[@role='row' or @role='button']")
    print(f"Found {len(dm_items)} DM items with role='row' or 'button'.")
    for i, item in enumerate(dm_items):
        print(f"{i}: tag={item.tag_name}, displayed={item.is_displayed()}, text={item.text[:50]}")

    # Click the first real chat (skip non-chat items, usually first 3)
    try:
        # Adjust the index if Instagram changes layout; here, index 3 is the first chat
        first_chat_index = 3
        first_chat = dm_items[first_chat_index]
        if first_chat.is_displayed():
            first_chat.click()
            print(f"Clicked on DM item at index {first_chat_index}: {first_chat.text[:50]}")
            time.sleep(2)
            # Type 'hi' in the message box and send
            try:
                # Try textarea first
                try:
                    textarea = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'textarea'))
                    )
                    print("Found textarea for message input.")
                except Exception:
                    # Try contenteditable div (Instagram sometimes uses this)
                    textarea = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
                    )
                    print("Found contenteditable div for message input.")

                textarea.click()
                textarea.send_keys('hi')
                textarea.send_keys(Keys.RETURN)
                print("Sent 'hi' to the first chat.")
                time.sleep(2)
            except Exception as e:
                print("Could not send 'hi' to the first chat:", e)
                # Debug: print all textareas and contenteditable divs
                textareas = driver.find_elements(By.TAG_NAME, 'textarea')
                print(f"Found {len(textareas)} textareas.")
                for i, ta in enumerate(textareas):
                    print(f"Textarea {i}: displayed={ta.is_displayed()}, enabled={ta.is_enabled()}")
                divs = driver.find_elements(By.XPATH, "//div[@contenteditable='true']")
                print(f"Found {len(divs)} contenteditable divs.")
                for i, d in enumerate(divs):
                    print(f"Div {i}: displayed={d.is_displayed()}, enabled={d.is_enabled()}, text={d.text[:30]}")
        else:
            print(f"First chat at index {first_chat_index} is not displayed.")
    except Exception as e:
        print("Could not open the first message in the DM list:", e)

    # Wait for 10 seconds before proceeding
    time.sleep(10)


    input('Press Enter to exit...')
finally:
    driver.quit() 