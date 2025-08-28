import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

# Update these with your demo details
your_name = "Apoorva"
your_email = "sample@yopmail.com"
your_phone = "1234567890"
your_company = "volza test"
your_requirements = "Testing the demo booking process"
your_country_code = "+91"  # Example: India

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)

def human_click(element):
    location = element.location_once_scrolled_into_view
    size = element.size
    x = location['x'] + size['width'] // 2
    y = location['y'] + size['height'] // 2
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()
    time.sleep(0.2)

# Start undetected Chrome browser
driver = uc.Chrome()
driver.get("https://www.volza.com/")
wait = WebDriverWait(driver, 20)

try:
    print("Waiting for demo button...")
    demo_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'bookalivedemo') or contains(text(), 'Book a Personalized Demo') or contains(text(), 'Book A Live Demo') ]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", demo_button)
    demo_button.click()
    print("Demo button clicked.")

    time.sleep(2)
    print("Filling name...")
    name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Name*']")))
    human_type(name_field, your_name)

    print("Selecting country code...")
    try:
        country_select = wait.until(EC.presence_of_element_located((By.ID, "country-select")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", country_select)
        country_select.click()
        time.sleep(0.5)
        country_select.send_keys(your_country_code)
        print("Country code selected via select element.")
    except Exception as e:
        print(f"Country code selection failed: {e}")

    print("Filling phone number...")
    try:
        phone_field = wait.until(EC.presence_of_element_located((By.ID, "enquiryPhoneNumber")))
        driver.execute_script("arguments[0].focus();", phone_field)
        human_type(phone_field, your_phone)
        print("Phone number filled via typing.")
    except Exception as e:
        print(f"Phone number typing failed: {e}. Trying JS...")
        driver.execute_script(f"document.getElementById('enquiryPhoneNumber').value = '{your_phone}';")
        print("Phone number filled via JS.")

    print("Filling email...")
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email*']")))
    human_type(email_field, your_email)

    print("Filling company name...")
    company_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Company name']")))
    human_type(company_field, your_company)

    print("Filling requirements...")
    requirements_field = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Please describe your requirements*']")))
    human_type(requirements_field, your_requirements)

    print("Submitting form...")
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='enquirySubmitBtn' or contains(text(),'Submit Now')]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_button)
    submit_button.click()
    print("Demo request submitted!")
except Exception as e:
    print("Could not complete demo booking:", e)
finally:
    driver.quit()
