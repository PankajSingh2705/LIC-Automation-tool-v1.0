# ============================================
# LIC AUTOMATION v1.0
# File : config.py
# ============================================

# -------------------------------
# APPIUM
# -------------------------------
APPIUM_SERVER = "http://127.0.0.1:4723"

PLATFORM_NAME = "Android"
AUTOMATION_NAME = "UiAutomator2"

DEVICE_NAME = "Android"

# -------------------------------
# PERFECT PRO
# -------------------------------

APP_PACKAGE = "com.ps.lic1"

# IMPORTANT:
# We will NOT launch the activity directly because
# it is not exported.
#
# User must manually open Perfect Pro once before
# running automation.
#
# Appium will attach to the current app.
APP_ACTIVITY = ""

# -------------------------------
# TIMEOUTS
# -------------------------------

IMPLICIT_WAIT = 10

EXPLICIT_WAIT = 30

PAGE_LOAD_WAIT = 5

SEARCH_RESULT_WAIT = 5

WAIT_BETWEEN_POLICIES = 30

# -------------------------------
# RETRY
# -------------------------------

MAX_RETRY = 3

# -------------------------------
# BATCH
# -------------------------------

BATCH_SIZE = 150

# -------------------------------
# EXCEL
# -------------------------------

INPUT_EXCEL = "input/policies.xlsx"

OUTPUT_EXCEL = "output/output.xlsx"

FAILED_EXCEL = "output/failed.xlsx"

# -------------------------------
# LOGS
# -------------------------------

LOG_FILE = "output/automation.log"

# -------------------------------
# SCREENSHOT
# -------------------------------

SCREENSHOT_FOLDER = "screenshots"

# -------------------------------
# XML
# -------------------------------

XML_FOLDER = "xml"

# -------------------------------
# POLICY FIELD
# -------------------------------

POLICY_LENGTH = 9

BACKSPACE_COUNT = 10

# -------------------------------
# STATUS
# -------------------------------

STATUS_SUCCESS = "SUCCESS"

STATUS_FAILED = "FAILED"

STATUS_SKIPPED = "SKIPPED"