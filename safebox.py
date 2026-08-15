############################################
#               MAIN FILE APP              #
############################################

# ======================
# STANDARD LIBRARY
# ======================

import os
import sys
import json
import time
import ctypes
import getpass
import threading
from datetime import datetime
from tkinter import messagebox

# ======================
# THIRD PARTY
# ======================

import bcrypt
import pystray

from PIL import Image

from cryptography.fernet import Fernet

from colorama import Fore, Style, just_fix_windows_console

# ======================
# LOCAL IMPORTS
# ======================

from constants import EMAIL_REGEX

from safebox_setup import create_and_configure_file_config

from safebox_security import (
    get_password_hash,
    generate_key,
    get_saltb64decode,
    decrypt_data,
    get_credentials,
    get_safebox_file
)

from functions import (
    create_default_icon,
    load_language,
    load_json_file,
    txt,
    txtError,
    txtInfo,
    txtSuccess,
    progress_bar,
    clear_console,
    get_config_path,
    check_if_config_file_exist,
    getSettings,
    exists,
    open_documentation
)

# ------------------ END IMPORT LIBS ------------------

# ------------------ [!] Check if app already running [!] ------------------
mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "SafeBoxUniqueMutex")
last_error = ctypes.windll.kernel32.GetLastError()

if last_error == 183:
    messagebox.showinfo("Safebox", "The Safebox application is already running.")
    sys.exit()
# ------------------------------------------------------------------

# ============ Define Console title ===========
ctypes.windll.kernel32.SetConsoleTitleW.restype = ctypes.c_bool
ctypes.windll.kernel32.SetConsoleTitleW.argtypes = [ctypes.c_wchar_p]

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

# ============================================

# init colorama (Require for color text)
just_fix_windows_console()

# ============================================

# Check if config.local.json exist
if not check_if_config_file_exist():

    try:
        create_and_configure_file_config()
        clear_console()

    except Exception as err:
        txtError(f"Error initialize setup. Please check in logs file. : {err}")
        txtInfo("Please retry operation. If error persist, contact administrator: grdev.contac@proton.me")
        input("Press enter to quit... ")
        sys.exit()

def authenticate_and_generate_key():
    """ Authenticate user, checking hash, salt ... if ok, generate key for fernet """
    
    tentatives_restantes = 3

    while tentatives_restantes > 0:
        master_password = getpass.getpass("Login : ")

        if bcrypt.checkpw(master_password.encode(), get_password_hash()):

            key = generate_key(
                master_password,
                get_saltb64decode()
            )
            
            return key
        
        else:
            tentatives_restantes -=1
            txtError(f"Bad password ({tentatives_restantes} tries left)")

    return False

# Check if key match & generate key
fernet_key = authenticate_and_generate_key()

if not fernet_key:
    txtError('Error : authenticate_and_generate_key()')
    time.sleep(2)
    sys.exit()

# [+] DYNAMIC KEY FERNET [+]
fernet = Fernet(fernet_key)

# ============== LANGAGE & CONFIG ==============
config          = load_json_file(get_config_path())
lang            = load_language()

VERSION_APP     = getSettings().get('app_version')

# ======================================================
def banner():
    banner = f"""                                               
    ███████  █████  ███████ ███████     ██████   ██████  ██   ██ {Fore.GREEN}V {VERSION_APP}{Fore.RESET} 
    ██      ██   ██ ██      ██          ██   ██ ██    ██  ██ ██  
    ███████ ███████ █████   █████       ██████  ██    ██   ███   
         ██ ██   ██ ██      ██          ██   ██ ██    ██  ██ ██  
    ███████ ██   ██ ██      ███████     ██████   ██████  ██   ██ 
"""
    print(banner)
# ======================================================

# ----------------- ICON TASKBAR PYSTRAY -----------------
display_app = ctypes.windll.kernel32.GetConsoleWindow()


# check if ico.ico exist
if exists("ico.ico"):
    image = Image.open("ico.ico")
else:
    image = create_default_icon()

def on_open():
    """ Open console, with forcing window """
    # ctypes.windll.user32.ShowWindow(display_app, 9)
    user32 = ctypes.windll.user32
    user32.ShowWindow(display_app, 9)
    user32.ShowWindow(display_app, 5)
    user32.SetForegroundWindow(display_app)

def reduct_console():
    ctypes.windll.user32.ShowWindow(display_app, 0)

def on_exit():
    icon.stop()
    os._exit(0)

def watch_console():
    user32 = ctypes.windll.user32
    while True:

        # minimise window
        if user32.IsIconic(display_app):
            reduct_console()
            time.sleep(1)
        time.sleep(0.2)

def start_tray():
    icon.run()

# Menu icon taskbar
icon = pystray.Icon(
    "Neural", 
    image, 
    title=f"SafeBox V {VERSION_APP}",
    menu=pystray.Menu(
        pystray.MenuItem("Open", on_open, default=True),
        pystray.MenuItem("Help / Notice", open_documentation),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(f"V {VERSION_APP}", action=None, enabled=False),
        pystray.MenuItem("Exit", on_exit)
))
# ------------------------------------------------------

# ====================== APP FONCTIONS ========================

# [!] BUGUED !!!
def restart_app():
    clear_console()

    if getattr(sys, "frozen", False):
        os.execv(sys.executable, [sys.executable] + sys.argv[1:])
    else:
        os.execv(sys.executable,[sys.executable, os.path.abspath(sys.argv[0])] + sys.argv[1:])

def open_safebox_directory():
    """ Open the dir which content safebox.json file """
    try:
        folder = os.path.dirname(get_safebox_file())
        txtInfo(f"Open dir from -> {folder}")
        os.startfile(folder)
    except Exception as err:
        txtError(f"ERROR. Impossible open dir -> {err}")


# ------------ Main Functions ------------

def add_credentials():

    txt("\n--- Add credentials ---", Fore.CYAN)
    service = input("Service name : ")
    login = input("Login : ")
    password = input("Password : ")

    try:
        with open(get_safebox_file(), 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    entry = {
        "id": f"{int(time.time())}",
        "added_date": datetime.now().strftime('%d/%m/%Y'),
        "service": fernet.encrypt(service.encode()).decode(),
        "login": fernet.encrypt(login.encode()).decode(),
        "password": fernet.encrypt(password.encode()).decode()
    }

    get_id = entry['id']

    data.append(entry)

    with open(get_safebox_file(), 'w') as f:
        json.dump(data, f, indent=4)

    clear_console()
    banner()
    txtSuccess("Success")
    txtInfo(f"ID: {get_id}")

def show_list(tri=None):

    data = get_credentials()

    if not data:
        txtInfo("The file is empty. [+] Press (1) for credentials.")
        return
    
    progress_bar(0.01)
    if tri == "asc":
        data.sort(key=lambda x: datetime.strptime(x['added_date'], '%d/%m/%Y'))
    elif tri == "desc":
        data.sort(key=lambda x: datetime.strptime(x['added_date'], '%d/%m/%Y'), reverse=True)

    try:
        # txt(f"\n---------- ({len(data)}) Results ----------", Fore.GREEN)
        for entry in data:
            print(f"""
ID         : {entry['id']}
Date ajout : {entry['added_date']}
Service    : {decrypt_data(entry['service'], fernet)}
Login      : {decrypt_data(entry['login'], fernet)}
Password   : {Fore.BLACK}{decrypt_data(entry['password'], fernet)}{Style.RESET_ALL}
{'-' * 40}""")
        txt(f"\n---------- ({len(data)}) Results ----------\n", Fore.GREEN)
        
    except Exception as err:
        txtError("Error. Data corruption.")
        txtError(f"Current key is not compatible with register key.")

def list_emails():
    """
    Display all emails registered
    """
    data = get_credentials()
    seen = set()
    emails = []

    if not data:
        txtInfo("File is empty. type (1) or --add for add data.")
        return  

    for entry in data:
        login = decrypt_data(entry["login"], fernet)

        if EMAIL_REGEX.match(login) and login not in seen:
            seen.add(login)
            emails.append(login)

    if not emails:
        txtInfo("No email address found.")
        return         


    for i, email in enumerate(emails, start=1):
        print(f"""
({Fore.YELLOW}{i}{Style.RESET_ALL}) {email}
{'-' * 40}""")

    txt(f"\n---------- ({len(emails)}) Results ----------\n", Fore.GREEN)

def search_by_keyword(keyword):

    txt("\n--- Search ---", Fore.CYAN)

    keyword = keyword.lower()

    data = get_credentials()

    results = []
    for entry in data:
        service = decrypt_data(entry['service'], fernet)
        login = decrypt_data(entry['login'], fernet)
        if keyword in service.lower() or keyword in login.lower():
            results.append({
                "id": entry['id'],
                "added_date": entry['added_date'],
                "service": service,
                "login": login,
                "password": decrypt_data(entry['password'], fernet)
            })


    if results:
        # txt(f"\nResults ({len(results)}) for keyword : '{keyword}'", Fore.GREEN)
        for entry in results:
            print(f"""
ID         : {entry['id']}
Date ajout : {entry['added_date']}
Service    : {entry['service']}
Login      : {entry['login']}
Password   : {Fore.BLACK}{entry['password']}{Style.RESET_ALL}
{'-' * 40}
""")
        txt(f"\n({len(results)}) Results for '{keyword}'", Fore.GREEN)
    else:
        txtInfo(f"No results found for '{keyword}'")

def remove_password(id_):

    print(f"{'-' * 40}")
    txt("\n--- Delete ---", Fore.CYAN)

    data = get_credentials()

    for entry in data:
        if entry['id'] == id_:
            print(f"""
ID         : {entry['id']}
Added date : {entry['added_date']}
Service    : {decrypt_data(entry['service'], fernet)}
Login      : {decrypt_data(entry['login'], fernet)}
Password   : {Fore.BLACK}{decrypt_data(entry['password'], fernet)}{Style.RESET_ALL}
""")

            confirm = input("Do you want to delete it? (yes/no) : ").strip().lower()
            if confirm == "yes":
                txtInfo("Deletion...")
                data.remove(entry)

                with open(get_safebox_file(), 'w') as f:
                    json.dump(data, f, indent=4)
                    
                progress_bar(0.03)
                txtSuccess(f"Password with ID '{id_}' was deleted.")
            else:
                txtInfo("Deletion cancelled")
            return
    txtInfo(f"No credentials found with ID '{id_}'.")

def find_password(id_):

    # if not check_main_psw():
    #     return
    
    data = get_credentials()

    for entry in data:
        if entry['id'] == id_:
            print(f"{'-' * 40}")
            txt("\nResult :", Fore.CYAN)
            print(f"""
ID         : {entry['id']}
Date ajout : {entry['added_date']}
Service    : {decrypt_data(entry['service'], fernet)}
Login      : {decrypt_data(entry['login'], fernet)}
Password   : {Fore.BLACK}{decrypt_data(entry['password'], fernet)}{Style.RESET_ALL}
{'-' * 40}""")
            return

    txt(f"No credentials found with ID {id_}.", Fore.YELLOW)

def edit_password(id_):

    txt("\n--- Edit ---", Fore.CYAN)
    # if not check_main_psw():
    #     return
    
    data = get_credentials()

    for entry in data:
        if entry['id'] == id_:
            txt(f"Credentials for: {entry['id']}:", Fore.GREEN)
            current_service = decrypt_data(entry['service'], fernet)
            current_login   = decrypt_data(entry['login'], fernet)
            current_pass    = decrypt_data(entry['password'], fernet)

            print(f"""
ID         : {entry['id']}
Date ajout : {entry['added_date']}
Service    : {current_service}
Login      : {current_login}
Password   : {Fore.BLACK}{current_pass}{Style.RESET_ALL}
""")
            
            txtInfo("Leave empty so as not to modify the field.")

            new_service = input(f"New service ({current_service}) : ").strip()
            new_login   = input(f"New login   ({current_login})   : ").strip()
            new_pass    = input(f"New password ({current_pass})   : ").strip()

            if new_service:
                entry['service'] = fernet.encrypt(new_service.encode()).decode()
            if new_login:
                entry['login'] = fernet.encrypt(new_login.encode()).decode()
            if new_pass:
                entry['password'] = fernet.encrypt(new_pass.encode()).decode()

            with open(get_safebox_file(), 'w') as f:
                json.dump(data, f, indent=4)

            txtSuccess("Successfully updated")
            return
        
    txtInfo(f"No credentials found with ID : {id_}.")


# ------------ Menu Commands ------------

def show_commands():
    print(f"""{Fore.LIGHTCYAN_EX}
------------------------------------------------
---------- HELP / AVAILABLE COMMANDS -----------
------------------------------------------------
--add               : {lang.help_menu.add_pass}

==================== Search ====================
--search <keyword>  : {lang.help_menu.search}
--find <id>         : {lang.help_menu.find}
--list              : {lang.help_menu.list}
--emails            : {lang.help_menu.emails}
--sort-asc          : {lang.help_menu.sort_asc}
--sort-desc         : {lang.help_menu.sort_desc}

================= Edit / Remove ================
--edit <id>         : {lang.help_menu.edit}
--remove <id>       : {lang.help_menu.remove}

==================== Other ====================
--update            : {lang.help_menu.update}
--logout            : {lang.help_menu.logout}
--cmd               : {lang.help_menu.cmd}
--clear             : {lang.help_menu.clear}
--open-dir          : {lang.help_menu.opend_dir}
--doc               : {lang.help_menu.help}
--exit              : {lang.help_menu.exit}
------------------------------------------------
{Fore.RESET}""")


def handle_commands(choix):
    """ Set the commands for the console """

    commands = {
        "--logout": lambda args: restart_app(),

        "--cmd": lambda args: show_commands(),

        "--add": lambda args: add_credentials(),

        "--list": lambda args: show_list(),

        "--emails": lambda args: list_emails(),

        "--sort-asc": lambda args: show_list(tri="asc"),

        "--sort-desc": lambda args: show_list(tri="desc"),

        "--clear": lambda args: (clear_console(), banner()),

        "--open-dir": lambda args: open_safebox_directory(),

        "--doc": lambda args: open_documentation(),

        "--search": lambda args: search_by_keyword(args),

        "--remove": lambda args: remove_password(args),

        "--find": lambda args: find_password(args),

        "--edit": lambda args: edit_password(args),

        "--update": lambda args: txtInfo("Please, check if new version is enable on this official SafeBox app. : "),

        "--exit": lambda args: on_exit()
    }

    parts = choix.split(" ", 1)

    command = parts[0]

    args = parts[1].strip() if len(parts) > 1 else ""

    if command in commands:
        commands[command](args)
    else:
        txtInfo(f"Unknown command : '{choix}'")

def menu():
    """  
    Main Menu
    """
    
    while True:
        txt("------- MENU ------", Fore.MAGENTA)
        print(f"[{Fore.YELLOW}1{Style.RESET_ALL}] {lang.menu.add_pass}")
        print(f"[{Fore.YELLOW}2{Style.RESET_ALL}] {lang.menu.list}")
        print(f"[{Fore.YELLOW}3{Style.RESET_ALL}] {lang.menu.cmd}")
        print(f"[{Fore.YELLOW}4{Style.RESET_ALL}] {lang.menu.doc}")
        print(f"[{Fore.YELLOW}5{Style.RESET_ALL}] {lang.menu.clear}")
        txt("-------------------\n", Fore.MAGENTA)

        choix = input("Choix : ").strip()

        match choix:
            case "1":
                add_credentials()
            case "2":
                show_list()
            case "3":
                show_commands()
            case "4":
                open_documentation()
            case "5":
                clear_console(), banner(), menu()

                break

            # handle commands
            case choix if choix.startswith("--"):
                handle_commands(choix)
            case _:
                txtError(f"'{choix}' {lang.error.choice}")


# ==================== ENTRY POINT ======================
if __name__ == "__main__":

    # icon arrière plan 
    threading.Thread(target=start_tray, daemon=True).start()
    # surveillance minimize
    threading.Thread(target=watch_console, daemon=True).start()

    set_console_title(f"SAFEBOX")

    clear_console()
    banner()
    menu()