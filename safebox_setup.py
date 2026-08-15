import sys
import time
import getpass
import json
import os
from colorama import Fore, Style, just_fix_windows_console

from functions import (
    check_if_config_file_exist,
    get_config_path,
    get_safebox_directory,
    load_language,
    exists
)

from safebox_security import (
    edit_config_value,
    generate_hash,
    generate_salt,
    get_safebox_file
)

from constants import DIR_NAME_BACKUP, DEFAULT_CONFIG_JSON

from logger_config import setup_logger

# ----------------------------------------------------
# - File for first safebox installation
# 1. Init first installation : Considering "config.local.json" not exist & check "settings.json" if exist. 
# 2. create "backup" folder
# 3. first_security_setup()
# ----------------------------------------------------


# init colorama (Require for color text)
just_fix_windows_console()

logger = setup_logger()

def create_and_configure_file_config():

    if check_if_config_file_exist():
        return
    
    print(f"\n{Fore.YELLOW}[+] Installation & Setup{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}[*] File config.local.json missing.{Style.RESET_ALL}")
        
    while True:

        confirm = input(
            "Do you want to automatically generate the file app configuration ? (yes/no)"
            ).lower().strip()

        match confirm:

            case "yes":

                try: 
                    # creat config.local.json & init
                    with open(get_config_path(), "w", encoding="utf-8") as fichier:

                        print("[.] Creating config.local.json ....")
                        json.dump(DEFAULT_CONFIG_JSON, fichier, indent=4)

                    time.sleep(0.2)
                    print("[+] config.local.json created.")

                    time.sleep(0.1)
                    print("[.] Creating 'backup' folder...")
                    os.makedirs(
                        os.path.join(get_safebox_directory(), DIR_NAME_BACKUP),
                        exist_ok=True
                    )
                    print("[+] Folder 'backup' was created.")

                    # time.sleep(0.1)
                    # print("[+] settings.json created.")

                    # Starting init main pass, hash & salt
                    print("[*] Initializing safebox setup ...")

                    time.sleep(0.1)

                    # FIRST SECURITY CONFIGURATION
                    first_security_setup()

                    return

                except Exception as err:

                    print(f"[ERROR] Impossible to create file. {err}. check in log file app")
                    logger.exception(err)
                    input("Press key to continue ...")
                    sys.exit()

            case "no":
                input("[*] Press an key to quit ...")
                sys.exit()
                break

            case _:
                print("[!] Invalide choice. yes / no ")


lang = load_language()

def first_security_setup():

    print(f"\n{Fore.YELLOW}{lang.first_menu_setup.p1}\n{Style.RESET_ALL}")

    while True:

        password_1 = getpass.getpass(
            f"{lang.first_menu_setup.pass1}"
        )

        password_2 = getpass.getpass(
            f"{lang.first_menu_setup.pass2}"
        )

        if password_1 != password_2:
            print(f"{Fore.RED}\n{lang.first_menu_setup.pass_inco}\n{Style.RESET_ALL}")
            continue


        print(f"""
{Fore.RED}{lang.first_menu_setup.becarfull}{Style.RESET_ALL}
{Fore.GREEN}
{lang.first_menu_setup.p2}

{lang.first_menu_setup.p3}
{Style.RESET_ALL}
{Fore.YELLOW}
{lang.first_menu_setup.p4}
{lang.first_menu_setup.p6}

{lang.first_menu_setup.p7}
{lang.first_menu_setup.p8}{get_safebox_file()}
{Style.RESET_ALL}
""")
        confirm = input(
            lang.first_menu_setup.conf_pass
        ).lower().strip()

        if confirm in ["oui", "o", "yes", "y"]:

            edit_config_value(
                "password_hash",
                generate_hash(password_1)
            )

            edit_config_value(
                "salt",
                generate_salt()
            )

            print(f"{Fore.GREEN}\n[+] {lang.first_menu_setup.conf_ok}{Style.RESET_ALL}")

            time.sleep(1)

            return True

        else:

            print(f"\n{lang.first_menu_setup.out}")

            # remove file config.local.json, because is empty, not configured, when user restarting app, app is bugged
            if check_if_config_file_exist() is True:
                try:
                    # remove file config (because is empty...)
                    os.remove(get_config_path())
                except Exception as err:
                    print(f"Error removing config.local.json file. Please remove manually for new init app. : {err}")

            input("Press an key to continue...")

            sys.exit()


