from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup WebDriver ---
options = Options()
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# --- Utility Functions ---
def scroll_to_bottom_slowly():
    pause = 0.3
    current = 0
    total = driver.execute_script("return document.body.scrollHeight")
    while current < total:
        driver.execute_script(f"window.scrollTo(0, {current});")
        current += 50
        time.sleep(pause)
    time.sleep(0.5)

def click_footer_link(link_text):
    """On current page, scroll to bottom, find footer, click a link by text."""
    scroll_to_bottom_slowly()
    footer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
    link = WebDriverWait(footer, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
    print(f" Clicking: {link_text}")
    old_url = driver.current_url
    driver.execute_script("arguments[0].click();", link)
    WebDriverWait(driver, 10).until(lambda d: d.current_url != old_url)
    time.sleep(0.5)

def ensure_footer_and_scroll():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
    scroll_to_bottom_slowly()

# --- Begin Navigation ---

driver.get("https://www.volza.com")
time.sleep(1)

# 1. About Volza
about_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'About Volza')]"))
)
driver.execute_script("arguments[0].click();", about_link)
WebDriverWait(driver, 10).until(EC.url_contains("/about"))
ensure_footer_and_scroll()

# 2. Vision & Mission
vm_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Vision') and contains(text(), 'Mission')]"))
)
driver.execute_script("arguments[0].click();", vm_link)
WebDriverWait(driver, 10).until(EC.url_contains("/vision-and-mission"))
ensure_footer_and_scroll()

# 3. Chain through static footer pages in order:
footer_sequence = [
    "Customer Review",
    "Career",
    "Contact Us",
    "Pricing",
    "Tickets",
    "Knowledgebase",
    "FAQ",
    "Privacy Policy",
    "Terms of Use",
    "Refunds Policy",
    "Affiliate",
    "Data Partners",
    "Consulting"
]

for page in footer_sequence:
    click_footer_link(page)
    ensure_footer_and_scroll()

print("✅ Navigation complete through all pages.")
time.sleep(2)
driver.quit()
