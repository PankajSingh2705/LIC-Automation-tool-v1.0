# ============================================
# LIC AUTOMATION v1.0
# File : ui_helper.py
# ============================================

import os
import time

from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)


class UIHelper:

    def __init__(self, driver, wait):

        self.driver = driver
        self.wait = wait

    # --------------------------------------------------

    def wait_id(self, locator, timeout=30):

        return WebDriverWait(
            self.driver,
            timeout
        ).until(

            EC.presence_of_element_located(

                (
                    AppiumBy.ID,
                    locator
                )

            )

        )

    # --------------------------------------------------

    def find_id(self, locator):

        return self.driver.find_element(
            AppiumBy.ID,
            locator
        )

    # --------------------------------------------------

    def exists(self, locator):

        try:

            self.driver.find_element(
                AppiumBy.ID,
                locator
            )

            return True

        except NoSuchElementException:

            return False

    # --------------------------------------------------

    def click(self, locator):

        element = self.wait_id(locator)

        element.click()

    # --------------------------------------------------

    def type_text(
        self,
        locator,
        value,
        clear=True
    ):

        element = self.wait_id(locator)

        element.click()

        if clear:

            try:
                element.clear()
            except:
                pass

        element.send_keys(str(value))

    # --------------------------------------------------

    def get_text(self, locator):

        try:

            return self.wait_id(locator).text.strip()

        except:

            return ""

    # --------------------------------------------------

    def press_back(self):

        self.driver.back()

    # --------------------------------------------------

    def take_screenshot(
        self,
        folder,
        filename
    ):

        os.makedirs(
            folder,
            exist_ok=True
        )

        path = os.path.join(
            folder,
            filename
        )

        self.driver.save_screenshot(path)

        return path

    # --------------------------------------------------

    def save_xml(
        self,
        folder,
        filename
    ):

        os.makedirs(
            folder,
            exist_ok=True
        )

        path = os.path.join(
            folder,
            filename
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                self.driver.page_source
            )

        return path

    # --------------------------------------------------

    def sleep(self, seconds):

        time.sleep(seconds)

    # --------------------------------------------------

    def wait_until_exists(
        self,
        locator,
        timeout=30
    ):

        try:

            WebDriverWait(
                self.driver,
                timeout
            ).until(

                EC.presence_of_element_located(

                    (
                        AppiumBy.ID,
                        locator
                    )

                )

            )

            return True

        except TimeoutException:

            return False

    # --------------------------------------------------

    def dump_current_activity(self):

        print()

        print("PACKAGE :",
              self.driver.current_package)

        print("ACTIVITY :",
              self.driver.current_activity)

        print()