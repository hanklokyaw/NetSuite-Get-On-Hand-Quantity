from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def download_reports(username, password, q1, a1, q2, a2, q3, a3, url1):
    """
    Function to automate downloading sales order data from NetSuite.
    """

    # Set up Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Navigate to the NetSuite login page
        driver.get(url1)

        # Find the username input field and enter the username
        username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "email")))
        username_input.send_keys(username)

        # Find the password input field and enter the password
        password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input.send_keys(password)

        # Click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()
        print("Logging in Net Suite...")

        try:
            # Handle security questions
            choose_account_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//td[text()='PRODUCTION']/following-sibling::td/a")))
            choose_account_link.click()
            print("Answering security question...")
        except:
            secret_question = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[2]/form/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]")))
            if q1 in secret_question.text.lower():
                username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "answer")))
                username_input.send_keys(a1)
            elif q2 in secret_question.text.lower():
                username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "answer")))
                username_input.send_keys(a2)
            elif q3 in secret_question.text.lower():
                username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "answer")))
                username_input.send_keys(a3)

            # Click the login button
            login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "submitter")))
            login_button.click()
            print("Logged into Net Suite.")

        # Wait for the page to load after login
        time.sleep(5)

        # Click the download CSV button
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[title='Export - CSV']")))
        login_button.click()
        print("Downloaded Custom Sales Data!")

        # Wait for the download to finish
        time.sleep(3)

    except:
        print("Download Failed!")

    finally:
        # Close the browser
        driver.quit()