# ============================================
# LIC AUTOMATION v1.0
# File : extractor.py
# ============================================

from locators import (
    AGENT_DETAILS,
    BRANCH,
    DOB,
    DOC,
    MATURITY_DATE,
    NAME,
    NEXT_PREMIUM,
    PAYMENT_MODE,
    PLAN,
    PLAN_NAME,
    PLAN_NO,
    POLICY_NO,
    POLICY_STATUS,
    PPT,
    PREMIUM,
    TERM,
)
from ui_helper import UIHelper


FIELD_LOCATORS = {
    "Policy Number": [POLICY_NO],
    "Name": [NAME],
    "DOB": [DOB],
    "DOC": [DOC],
    "Plan": [PLAN, PLAN_NO, "com.ps.lic1:id/txtPlanNo"],
    "Plan Name": [PLAN_NAME],
    "Term": [TERM],
    "PPT": [PPT],
    "Premium": [PREMIUM],
    "Payment Mode": [PAYMENT_MODE],
    "Next Premium": [NEXT_PREMIUM, "com.ps.lic1:id/txtFUP"],
    "Last Transaction": ["com.ps.lic1:id/txtLastTrans"],
    "Policy Status": [POLICY_STATUS, "com.ps.lic1:id/txtPolicyStatus"],
    "Maturity Date": [MATURITY_DATE, "com.ps.lic1:id/txtMaturityDate"],
    "Branch": [BRANCH],
    "Agent Details": [AGENT_DETAILS],
}

REQUIRED_FIELDS = [
    "Policy Number",
    "Name",
    "Plan Name",
    "Policy Status",
]


class Extractor:

    def __init__(self, driver, wait):

        self.driver = driver
        self.wait = wait
        self.ui = UIHelper(driver, wait)

    # --------------------------------------------------

    def clean_text(self, value):

        if value is None:
            return ""

        value = str(value)
        value = value.replace("\r", " ")
        value = value.replace("\n", " ")
        value = " ".join(value.split())

        return value.strip()

    # --------------------------------------------------

    def read_first_available(self, locators):

        for locator in locators:

            try:
                if not self.ui.exists(locator):
                    continue

                value = self.ui.get_text(locator)
                value = self.clean_text(value)

                if value:
                    return value

            except Exception:
                continue

        return ""

    # --------------------------------------------------

    def normalize_money(self, value):

        value = self.clean_text(value)
        value = value.replace("₹", "")
        value = value.replace("Rs.", "")
        value = value.replace("Rs", "")
        value = value.replace(",", "")

        return value.strip()

    # --------------------------------------------------

    def normalize_field_value(self, field_name, value):

        if field_name == "Premium":
            return self.normalize_money(value)

        return value

    # --------------------------------------------------

    def extract_details(self):

        data = {}

        for field_name, locators in FIELD_LOCATORS.items():
            value = self.read_first_available(locators)
            data[field_name] = self.normalize_field_value(field_name, value)

        return data

    # --------------------------------------------------

    def validate(self, data):

        missing = []

        for field_name in REQUIRED_FIELDS:

            if not data.get(field_name):
                missing.append(field_name)

        if missing:
            raise ValueError(
                "Missing required field(s): " + ", ".join(missing)
            )

        return True

    # --------------------------------------------------

    def extract(self, validate=True):

        data = self.extract_details()

        if validate:
            self.validate(data)

        return data

    # --------------------------------------------------

    def safe_console_text(self, value):

        value = self.clean_text(value)
        value = value.replace("₹", "Rs.")

        return value.encode(
            "ascii",
            errors="replace"
        ).decode("ascii")

    # --------------------------------------------------

    def print_details(self, data):

        print()
        print("EXTRACTED POLICY DETAILS")

        for field_name in FIELD_LOCATORS.keys():
            value = self.safe_console_text(data.get(field_name, ""))
            print(f"{field_name}: {value}")

        print()


