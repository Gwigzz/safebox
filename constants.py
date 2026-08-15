import os
import sys
import re

# ===================== CONFIGURATION =====================

BASE_DIR = os.path.dirname(sys.executable) \
    if getattr(sys, 'frozen', False) \
    else os.path.dirname(__file__)

APP_NAME            = "SafeBox"

DIR_NAME_LOG        = "logs"
DIR_NAME_BACKUP     = "backup"

FILE_SETTINGS_NAME  = "settings.json"

# ROOT FILE SAFEBOX.EXE
FILE_SETTINGS       = os.path.join(BASE_DIR, FILE_SETTINGS_NAME)
FILE_LANG           = os.path.join(BASE_DIR, "lang.json")

# C...Appdata/romaing/safebox/
FILE_SAFEBOX        = "safebox.json"
FILE_CONFIG         = "config.local.json"
FILE_LOG            = "safebox.log"

# =========== Default config.local.json & settings.json ===========
DEFAULT_CONFIG_JSON = {"password_hash": "", "salt": "" }

BASE_URL            = "https://raw.githubusercontent.com/Gwigzz/test_version/main/"
BASE_URL_SETTINGS   = BASE_URL + FILE_SETTINGS_NAME

DEFAULT_SETTINGS_JSON = {
    "lang": "EN",
    "app_version": "1.5.0",
    "release_date": "10-08-2026",
    "url_website": "https://grdev.tech",
    "url_documentation": "https://grdev.tech/app/safebox/doc_FR.html"
}
""" Used during initializing app """

EMAIL_REGEX         = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
