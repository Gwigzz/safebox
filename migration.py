"""
################################################

[!] This file is not used for the moment
[!] Need more secure & data backup

################################################
"""
import os
import json
import shutil
import sys
import time
import bcrypt

import getpass
from datetime import datetime
from cryptography.fernet import Fernet

# from safebox import authenticate_and_generate_key

from functions import (
    get_config_path,
    get_backup_directory
)

from safebox_security import (
    get_password_hash,
    generate_key,
    get_saltb64decode,
    get_credentials,
    get_safebox_file,
)

from safebox_setup import first_security_setup

from constants import FILE_SAFEBOX, FILE_CONFIG

# MIGRATION FILE. 
# OLD DATA ENCRYPRED BYE OLD KEY TO ENCRYPT WITH NEW KEY

# _____ Workflow _____
"""
Old hardcoded key (or generate it with Fernet)
        ↓
Create an encrypted backup with the old key
        ↓
Decrypt existing data using the old password
        ↓
Generate a new user-specific key
        ↓
Re-encrypt the data with the new key
        ↓
Save the encrypted data
"""

def stop_app():
    print("............................")
    input("Press an key to exit...")
    sys.exit()


def check_and_generate_fernet_key():
    """ Get key fernet """
    
    tentatives_restantes = 3

    while tentatives_restantes > 0:
        master_password = getpass.getpass("Enter main password : ")

        if bcrypt.checkpw(master_password.encode(), get_password_hash()):

            key = generate_key(
                master_password,
                get_saltb64decode()
            )
            
            return key
        else:
            tentatives_restantes -=1
            print(f"[!] Bad password ({tentatives_restantes} tries left)")


    return False


print("Change main password")
print("[!] WARNING [!]")
print("[!] This will change your old master password, and migrate the old data to the new password.")


# while True:
#     confirm_change_psw_and_migration = input("Are you sure you want to continue ? (yes/no) : ")

#     match confirm_change_psw_and_migration:
        
#         case "yes":
#             print("s")
#         case "no":
#             print("s")
#         case _:
#             print("[!] Invalide choice")

# else:
#     print("...")

stop_app()


# Check if key match & generate key (GET KEY FROM config.json)
check_password = check_and_generate_fernet_key()
if not check_password:
    print("[!] Bad fernet key.")
    input("Press an key to exit...")
    sys.exit()


# get old key
fernet_old_key = Fernet(check_password).generate_key()

# FILE_NAME           = "safebox.json"

FIELDS = ["service", "login", "password"]

def backup_vault():
    """ Save safebox.json & config.local.json """
    today = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    backup_dir = get_backup_directory()

    backup_file_pass = os.path.join(
        backup_dir,
        f"BACKUP_{today}_safebox.json"
    )

    backup_file_config = os.path.join(
        backup_dir,
        f"BACKUP_{today}_config.local.json"
    )

    try:
        # copy sabebox
        shutil.copy(
            get_safebox_file(),
            backup_file_pass
        )

        # copy config
        shutil.copy(
            get_config_path(),
            backup_file_config
        )

        print(f"[+] Save old files success :\n [COPY] {backup_file_pass}\n [COPY] {backup_file_config}")

    except Exception as er:
        print(f"[ERROR] copy original file. {er}")


# [!] SAVE OLD DATA BEFORE MGIRATION !!
backup_vault()

# 1. générer nouveau password HASH
# 2. générer nouveau salt
# 3. générer nouvelle clé

# Enter new password
first_security_setup()

fernet_new_key = check_and_generate_fernet_key()
if not fernet_new_key:
    print("[!] Bad fernet key.")
    input("Press an key to exit...")
    sys.exit()


print(f"KEY {fernet_new_key}")


def migration_data():
    try:
        old_json_password = get_credentials()

        for entry in old_json_password:

            for field in FIELDS:

                # decrypt old
                decrypted = fernet_old_key.decrypt(
                    entry[field].encode()
                )

                # encrypt new
                reencrypted = fernet_new_key.encrypt(
                    decrypted
                )

                # save back
                entry[field] = reencrypted.decode()

        # create a temp file (for security save data)
        tmp_file = get_safebox_file() + ".tmp"

        # SAUVEGARDE DATA WITH NEW KEY FERNET 
        with open(get_safebox_file(), "w", encoding="utf-8") as f:
            # json.dump(old_json_password, f, indent=4, ensure_ascii=False)
            json.dump(old_json_password, f)

        os.replace(tmp_file, get_safebox_file())

        print("[OK] Migration success.")

    except Exception as err:
        print(f"[!] Error migration : {err}")




