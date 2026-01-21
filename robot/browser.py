from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from whatsapp import wait_for_whatsapp
from bot import bot_loop
from pathlib import Path

print(Path("./data/chrome-profile").resolve())

def create_browser():
    options = Options()
    options.add_argument("--user-data-dir=./data/chrome-profile")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")

    wait_for_whatsapp(driver)

    return driver

if __name__ == "__main__":
    drive = create_browser()
    bot_loop(drive)
