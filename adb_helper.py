import subprocess
import os

XML_PATH = "temp_result.xml"


def run_adb(cmd):
    """
    Run any adb command.
    """
    full = f"adb {cmd}"

    result = subprocess.run(
        full,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[ADB ERROR]")
        print(result.stderr)

    return result.stdout


def dump_ui():
    """
    Dumps current screen XML and returns local XML path.
    """

    print("[ADB] Dumping UI hierarchy...")

    run_adb("shell uiautomator dump /sdcard/result.xml")
    run_adb(f'pull /sdcard/result.xml "{XML_PATH}"')

    if not os.path.exists(XML_PATH):
        raise Exception("temp_result.xml not created")

    print("[ADB] XML dumped successfully")

    return XML_PATH


def tap(x, y):
    run_adb(f"shell input tap {x} {y}")


def type_text(text):
    text = str(text).replace(" ", "%s")
    run_adb(f'shell input text "{text}"')


def clear_text():
    """
    Clears policy number textbox.
    """
    for _ in range(25):
        run_adb("shell input keyevent 67")


def press_back():
    run_adb("shell input keyevent 4")