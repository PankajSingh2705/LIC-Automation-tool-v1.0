from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "Android"
options.no_reset = True

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

xml = driver.page_source

with open("details.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print("✅ details.xml saved")

driver.quit()