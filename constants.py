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

# Files name for safebox directory path app
FILE_SETTINGS_NAME  = "settings.json"
FILE_LANG_NAME      = "lang.json"

# ROOT FILE SAFEBOX.EXE
FILE_SETTINGS       = os.path.join(BASE_DIR, FILE_SETTINGS_NAME)
FILE_LANG           = os.path.join(BASE_DIR, FILE_LANG_NAME)

# C...Appdata/romaing/safebox/
FILE_SAFEBOX        = "safebox.json"
FILE_CONFIG         = "config.local.json"
FILE_LOG            = "safebox.log"

# =========== URL Github ===========
URL_GITHUB_CONTENT  = "https://raw.githubusercontent.com/Gwigzz/safebox/main/"
RELEASE_URL         = "https://github.com/Gwigzz/safebox/releases/latest"

# =========== Default config.local.json & settings.json ===========
DEFAULT_CONFIG_JSON = {"password_hash": "", "salt": "" }
""" Default config.local.json file. Used during initializing app """

DEFAULT_SETTINGS_JSON = {
    "lang": "EN",
    "app_version": "1.5.0",
    "release_date": "10-08-2026",
    "url_website": "https://grdev.tech",
    "url_documentation": "https://grdev.tech/app/safebox/doc_FR.html"
}
""" Default settings for settings.json file. Used during initializing app """

EMAIL_REGEX         = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
