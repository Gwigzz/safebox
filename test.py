import os
import sys
import json
import time
import ctypes
import bcrypt
import requests
from datetime import datetime
import getpass
import webbrowser
# import keyboard
from cryptography.fernet import Fernet
from colorama import Fore, Style, init
# import requests
from pathlib import Path

from constants import *

from logger_config import setup_logger

import re

from functions import (
    txt,
    txtError,
    txtInfo,
    txtSuccess,
    progress_bar,
    load_json_file,
    clear_console,
    get_config_path,
    getCurrentLang,
    check_if_config_file_exist,
    getSettings,
    load_language,
    exists,
)

from safebox_security import (
    get_password_hash,
    generate_key,
    get_saltb64decode,
)

from safebox_setup import first_security_setup
from safebox_update import compare_settings, get_online_version, get_local_version

# colorama
init()
print(f"{Fore.LIGHTGREEN_EX } -- TEST --> {Style.RESET_ALL}-- \n")

# ...... here ....

logger = setup_logger()

# print(check_if_config_file_exist())

# if check_if_config_file_exist() is True:
#     # remove file config (because is empty...)
#     print("file config exist !")

# test dev


# test grevecservice
