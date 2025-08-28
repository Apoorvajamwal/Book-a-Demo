import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Your details
your_name = "Apoorva"
your_email = "sample@yopmail.com"
your_phone = "1234567890"
your_company = "volza test"
your_requirements = "Testing the demo booking process"
your_country_code = "+91"  # For India

# Chrome options
options = uc.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

# Start browser
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 20)

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)

try:
    driver.get("https://www.volza.com/")

    # Click demo button
    demo_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Book A Live Demo')]")))
    demo_button.click()

    # Fill Name
    name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Name*']")))
    human_type(name_field, your_name)

    # Country code selection (optional)
    try:
        country_select = wait.until(EC.presence_of_element_located((By.ID, "country-select")))
        country_select.click()
        country_select.send_keys(your_country_code)
    except Exception as e:
        print(f"Country code skipped: {e}")

    # Phone
    phone_field = wait.until(EC.presence_of_element_located((By.ID, "enquiryPhoneNumber")))
    human_type(phone_field, your_phone)

    # Email
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email*']")))
    human_type(email_field, your_email)

    # Company
    company_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Company name']")))
    human_type(company_field, your_company)

    # Requirements
    requirements_field = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Please describe your requirements*']")))
    human_type(requirements_field, your_requirements)

    # Submit form
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='enquirySubmitBtn' or contains(text(),'Submit Now')]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_button)
    submit_button.click()

    print("Demo request submitted.")

    time.sleep(3)
    # Wait for the questionnaire to appear
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(),'Personalized Demo') or contains(text(),'create a Personalized Demo')]")
    ))
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(1)

    # Debug: print all options text
    options_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'form-item') and contains(@class, 'ques1')]")
    print("Available form-item options:")
    for div in options_divs:
        print(div.text.strip())

    # Click Export option
    export_div = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'form-item') and contains(@class, 'ques1') and contains(., 'Export')]")
    ))
    export_div.click()
    time.sleep(1)

    # Click India option
    india_div = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'form-item') and contains(@class, 'ques1') and contains(., 'India')]")
    ))
    india_div.click()

    print("Export and India clicked.")
except Exception as e:
    print(f"Export/India section skipped: {e}")


finally:
    time.sleep(5)
    driver.quit() 