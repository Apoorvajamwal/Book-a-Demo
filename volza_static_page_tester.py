from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup Chrome ---
options = Options()
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)
driver.maximize_window()


def scroll_to_element_slowly(element):
    """Scroll down slowly until the element is visible in the viewport."""
    current_scroll = 0
    step = 50
    pause = 0.2
    while not is_in_viewport(element):
        current_scroll += step
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(pause)
    time.sleep(1)


def slow_scroll_to_bottom():
    """Scroll slowly from top to bottom of the page."""
    scroll_pause_time = 0.3
    current_scroll = 0
    total_height = driver.execute_script("return document.body.scrollHeight")
    while current_scroll < total_height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        current_scroll += 50
        time.sleep(scroll_pause_time)


def is_in_viewport(element):
    return driver.execute_script("""
        var elem = arguments[0],
            box = elem.getBoundingClientRect();
        return (
            box.top >= 0 &&
            box.left >= 0 &&
            box.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            box.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    """, element)


def click_element_via_js(element):
    driver.execute_script("arguments[0].click();", element)


# --- Step 1: Open volza.com ---
driver.get("https://www.volza.com")

# --- Step 2: Wait and scroll to 'About Volza' ---
about_volza = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'About Volza')]"))
)
scroll_to_element_slowly(about_volza)
click_element_via_js(about_volza)

# --- Step 3: On About page, scroll slowly to bottom ---
WebDriverWait(driver, 10).until(EC.url_contains("/about"))
time.sleep(1)
slow_scroll_to_bottom()

# --- Step 4: Wait and click 'Vision & Mission' ---
vision_mission = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Vision') and contains(text(), 'Mission')]"))
)
scroll_to_element_slowly(vision_mission)
click_element_via_js(vision_mission)

# --- Step 5: On Vision & Mission page, scroll slowly to bottom ---
WebDriverWait(driver, 10).until(EC.url_contains("/vision-and-mission"))
time.sleep(1)
slow_scroll_to_bottom()

# Optional pause before closing
time.sleep(3)
driver.quit()