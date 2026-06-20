# ============================================
# LIC AUTOMATION v1.0
# File : navigator.py
# ============================================

import os
import time
from datetime import datetime

from appium.webdriver.common.appiumby import AppiumBy

from config import (
    APP_PACKAGE,
    BACKSPACE_COUNT,
    EXPLICIT_WAIT,
    MAX_RETRY,
    POLICY_LENGTH,
    SCREENSHOT_FOLDER,
    SEARCH_RESULT_WAIT,
    XML_FOLDER,
)
from locators import (
    CLOSE_BUTTON,
    NAME,
    POLICY_NO,
    POLICY_NUMBER,
    POLICY_STATUS,
    POLICY_STATUS_BUTTON,
)
from ui_helper import UIHelper


DETAIL_SCREEN_IDS = [
    NAME,
    POLICY_NO,
    POLICY_STATUS,
    "com.ps.lic1:id/txtPolicyStatus",
    "com.ps.lic1:id/txtmaybe",
]

CLOSE_BUTTON_IDS = [
    CLOSE_BUTTON,
    "com.ps.lic1:id/btnCLOSE",
]


class Navigator:

    def __init__(self, driver, wait):

        self.driver = driver
        self.wait = wait
        self.ui = UIHelper(driver, wait)

    # --------------------------------------------------

    def open_app_state(self):

        print()
        print("APP STATE CHECK")
        print("PACKAGE :", self.driver.current_package)
        print("ACTIVITY:", self.driver.current_activity)
        print()

        return self.driver.current_package == APP_PACKAGE

    # --------------------------------------------------

    def is_search_screen(self):

        return self.ui.exists(POLICY_NUMBER)

    # --------------------------------------------------

    def is_details_screen(self):

        for locator in DETAIL_SCREEN_IDS:

            if self.ui.exists(locator):
                return True

        return False

    # --------------------------------------------------

    def verify_search_screen(self):

        if self.is_search_screen():
            return True

        if self.is_details_screen():
            self.close_details()

        if self.is_search_screen():
            return True

        self.recover_to_search()

        return self.is_search_screen()

    # --------------------------------------------------

    def clear_policy_field(self):

        element = self.ui.wait_id(
            POLICY_NUMBER,
            timeout=EXPLICIT_WAIT
        )

        element.click()

        try:
            element.clear()
            return True
        except Exception:
            pass

        for _ in range(BACKSPACE_COUNT):
            self.driver.press_keycode(67)

        return True

    # --------------------------------------------------

    def enter_policy(self, policy_number):

        policy_number = str(policy_number).strip()

        if len(policy_number) != POLICY_LENGTH:
            raise ValueError(
                f"Policy number must be {POLICY_LENGTH} digits: {policy_number}"
            )

        if not self.verify_search_screen():
            raise RuntimeError("Search screen not found before entering policy")

        print("Enter Policy:", policy_number)

        self.clear_policy_field()

        self.ui.type_text(
            POLICY_NUMBER,
            policy_number,
            clear=False
        )

        return True

    # --------------------------------------------------

    def click_status(self):

        print("Clicking POLICY STATUS...")

        try:
            self.ui.click(POLICY_STATUS_BUTTON)
            return True
        except Exception:
            pass

        try:
            button = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("POLICY STATUS")'
            )
            button.click()
            return True
        except Exception:
            pass

        try:
            buttons = self.driver.find_elements(
                AppiumBy.CLASS_NAME,
                "android.widget.Button"
            )

            for button in buttons:
                text = (button.text or "").strip().upper()

                if "POLICY" in text and "STATUS" in text:
                    button.click()
                    return True

        except Exception:
            pass

        return False

    # --------------------------------------------------

    def wait_for_details(self, timeout=None):

        timeout = timeout or EXPLICIT_WAIT

        print("Waiting for details screen...")

        end_time = time.time() + timeout

        while time.time() < end_time:

            if self.is_details_screen():
                print("Details screen detected")
                return True

            time.sleep(1)

        return False

    # --------------------------------------------------

    def close_details(self):

        if not self.is_details_screen():
            return True

        print("Closing details screen...")

        for locator in CLOSE_BUTTON_IDS:

            try:
                if not self.ui.exists(locator):
                    continue

                self.ui.find_id(locator).click()
                time.sleep(SEARCH_RESULT_WAIT)

                if self.is_search_screen():
                    return True

            except Exception:
                pass

        try:
            close_button = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("CLOSE")'
            )
            close_button.click()
            time.sleep(SEARCH_RESULT_WAIT)

            if self.is_search_screen():
                return True

        except Exception:
            pass

        return self.recover_to_search()

    # --------------------------------------------------

    def recover_to_search(self):

        print("Recovery started...")

        for _ in range(4):

            if self.is_search_screen():
                return True

            try:
                self.driver.back()
            except Exception:
                pass

            time.sleep(1)

        return self.is_search_screen()

    # --------------------------------------------------

    def capture_error_state(self, policy_number, prefix="navigator_error"):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_policy = str(policy_number).strip() or "unknown"
        filename = f"{prefix}_{safe_policy}_{timestamp}"

        screenshot_path = self.ui.take_screenshot(
            SCREENSHOT_FOLDER,
            f"{filename}.png"
        )

        xml_path = self.ui.save_xml(
            XML_FOLDER,
            f"{filename}.xml"
        )

        print("Screenshot:", os.path.abspath(screenshot_path))
        print("XML       :", os.path.abspath(xml_path))

        return {
            "screenshot": screenshot_path,
            "xml": xml_path,
        }

    # --------------------------------------------------

    def search_policy_once(self, policy_number):

        self.enter_policy(policy_number)

        if not self.click_status():
            raise RuntimeError("POLICY STATUS button click failed")

        if not self.wait_for_details():
            raise TimeoutError("Details screen did not open")

        return True

    # --------------------------------------------------

    def search_policy(self, policy_number, max_retry=None):

        max_retry = max_retry or MAX_RETRY
        last_error = None

        for attempt in range(1, max_retry + 1):

            print()
            print(f"Policy {policy_number} attempt {attempt}/{max_retry}")

            try:
                self.search_policy_once(policy_number)
                return True

            except Exception as error:
                last_error = error
                print("Attempt failed:", error)

                self.capture_error_state(
                    policy_number,
                    prefix=f"attempt_{attempt}"
                )

                self.recover_to_search()

        raise RuntimeError(
            f"Policy {policy_number} failed after {max_retry} attempts"
        ) from last_error

