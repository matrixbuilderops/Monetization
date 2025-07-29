import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

OUTPUT_DIR = "./model_output"
LOG_FILE = "./bridge_log.txt"
POLL_INTERVAL = 5  # seconds


def setup_driver() -> webdriver.Firefox:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    return driver


def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def scrape_and_store(driver: webdriver.Firefox):
    driver.get("http://localhost:11434")  # Replace if needed
    time.sleep(2)  # Wait for page load

    try:
        # Adjust selectors based on the model UI structure
        text_elements = driver.find_elements(By.CSS_SELECTOR, ".model-output")
        contents = [el.text.strip() for el in text_elements if el.text.strip()]

        if not contents:
            return

        for i, content in enumerate(contents):
            filename = f"affirmation_{int(time.time())}_{i}.txt"
            file_path = os.path.join(OUTPUT_DIR, filename)
            with open(file_path, "w") as f:
                f.write(content)
            log_event(f"Saved: {filename}")
    except Exception as e:
        log_event(f"Error during scraping: {str(e)}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    driver = setup_driver()

    try:
        while True:
            scrape_and_store(driver)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        driver.quit()
        log_event("Daemon stopped by user.")


if __name__ == "__main__":
    main()
