import json
import time
import os
import webbrowser
from PIL import Image, ImageDraw

from colorama import Fore, Style, just_fix_windows_console

from logger_config import setup_logger

from constants import FILE_CONFIG, FILE_LANG, DIR_NAME_BACKUP, FILE_SETTINGS, DEFAULT_SETTINGS_JSON, APP_NAME, URL_GITHUB_CONTENT

##############################################
### I don't know where to put all this shit. #
##############################################

"""
### Functions ### [!] need refactoring.
"""

class DictToObject:
    """ Convert array["data"] it in Objet array.data """
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                value = DictToObject(value)
            setattr(self, key, value)


# init colorama (Require for color text)
just_fix_windows_console()

logger = setup_logger()

def load_json_file(path_and_filename):
    """ Load data from JSON FILE """
    try:
        with open(path_and_filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as er:
        logger.exception(er)
        input(f"[!] Error : {er} | press key to exit ...")
        return None

def exists(path):
    """ check if file or folder exist """
    return os.path.exists(path)


def get_safebox_directory():
    """Return SafeBox root directory in AppData."""
    base = os.getenv("APPDATA")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path



def getSettings():
    """ return settings """
    return load_json_file(FILE_SETTINGS)


def generate_settings_file():

    # check if settings.json exist or not
    if not exists(FILE_SETTINGS):

        try:
            with open(FILE_SETTINGS, "x", encoding="utf-8") as fichier:

                txtInfo("settings.json file was missing. A new one has been created automatically..")
                json.dump(DEFAULT_SETTINGS_JSON, fichier, indent=4)
            return True
        except Exception as err:
            print(f"Error : {err}")
            return False
    return True


def getCurrentLang():
    return getSettings().get("lang")


def load_language():

    # check if settings.json exist
    if not exists(FILE_SETTINGS):
        generate_settings_file()

    settings = getSettings()

    # check if file lang exist
    if not exists(FILE_LANG):
        print(f"File langage 'lang.json' missing. Please download it from this address: {URL_GITHUB_CONTENT}")
        input("...")

    lang = settings.get("lang", "EN")

    langs = load_json_file(FILE_LANG)

    return DictToObject(langs.get(lang, langs.get("EN")))


# --------------------------------------------------------------

def open_documentation():

    url_documentation = getSettings().get('url_documentation')

    try:
        webbrowser.open(f"{url_documentation}")
        txtInfo(f"Website Notice : {url_documentation}")
    except:
            txtError(f"Error opening web browser. Please visite {url_documentation}")


########################
#      FILE / PATH     #
########################

def get_config_path():
    return os.path.join(
        get_safebox_directory(),
        FILE_CONFIG
    )

def get_backup_directory():
    path = os.path.join(
        get_safebox_directory(),
        DIR_NAME_BACKUP
    )
    os.makedirs(path, exist_ok=True)

    return path

def check_if_config_file_exist():
    config_file_exist = os.path.exists(get_config_path())
    return config_file_exist


# -----------------------------------------------------------


def progress_bar(milisec=0.06, steps=20):
    bar_length = steps + 10  # marge pour % et crochets

    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        bar = "█" * i + "-" * (steps - i)

        print(f"{Fore.GREEN}\r[{bar}] {percent:3d}%{Style.RESET_ALL}", end="", flush=True)
        time.sleep(milisec)

    # 👇 efface complètement la ligne
    print("\r" + " " * bar_length + "\r", end="", flush=True)


def txt(txt, color=Fore.BLUE):
    """ Add text color """
    colored = f"{color}{txt}{Style.RESET_ALL}"
    print(colored)

def txtError(msgError):
    """ [!] Error message """
    msg = txt(f"[!] {msgError} \n", Fore.RED)
    return msg

def txtSuccess(msgSuccess):
    """ [+] Success message """
    msg = txt(f"[+] {msgSuccess} \n", Fore.GREEN)
    return msg

def txtInfo(msgInfo):
    """ [*] Info message """
    msg = txt(f"[*] {msgInfo} \n", Fore.YELLOW)
    return msg

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def hide_email(email: str) -> str:
    if "@" not in email:
        return email

    local, domain = email.split("@", 1)

    if len(local) <= 6:
        masked_minimail = local[:-3] + "**" + local[-1:]
        return masked_minimail + "@" + domain

    masked_local = local[:-6] + "***" + local[-3:]
    return masked_local + "@" + domain


# generate ico default
def create_default_icon():

    image = Image.new("RGB", (64, 64), (40, 40, 40))
    draw = ImageDraw.Draw(image)

    blue = (0, 180, 255)

    draw.rounded_rectangle((16, 26, 48, 54), radius=6, fill=blue)
    draw.arc((20, 8, 44, 32), 180, 360, fill=blue, width=6)
    draw.ellipse((28, 32, 36, 40), fill=(40, 40, 40))
    draw.rectangle((30, 37, 34, 48), fill=(40, 40, 40))
    
    return image