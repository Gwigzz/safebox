import base64
import os
import bcrypt
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from functions import get_config_path, get_safebox_directory

from constants import FILE_SAFEBOX

#########################################################################

def generate_key(password: str, salt: bytes):

    if isinstance(password, str):
        password = password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    return base64.urlsafe_b64encode(
        kdf.derive(password)
    )

def load_json_file(filename):
    """ Load data from JSON FILE """
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as er:
        print(f"Impossible to load this file : {filename}. Error : {er}")
        input("Press key to continue ...")
        # print(f"Error : {er}")
        return

#########################################################################

def decrypt_data(data, fernet):
    return fernet.decrypt(data.encode()).decode()

def get_safebox_file():
    """Return encrypted vault file path."""
    return os.path.join(
        get_safebox_directory(),
        FILE_SAFEBOX
    )

def get_credentials():
    """Load data from safebox file."""
    try:
        with open(get_safebox_file(), "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print("[*] Error : safebox.json not found.")
        return None

    except json.JSONDecodeError:
        print("[*] Error : safebox.json is invalid.")
        return None


# [!] Need edit by atomic fonction
def edit_config_value(key, value):
    try:
        config = load_json_file(get_config_path())
        config[key] = value
        # save information
        with open(get_config_path(), "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except KeyError as er:
        print(f"Error : {er}")

def generate_hash(plain_password):
    """ generate a hash password based64 encoded utf-8 """
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
    

def generate_salt():
    """ generate salt encoded64 """
    salt = base64.b64encode(os.urandom(16)).decode()
    return salt

def get_saltb64decode():
    """ Get salt from config.json """
    config = load_json_file(get_config_path())
    salt = base64.b64decode(config["salt"])
    return salt

def get_salt():
    config = load_json_file(get_config_path())
    return config["salt"]

def get_password_hash():
    """ Get password hash from config.json """
    config = load_json_file(get_config_path())
    stored_hash = config["password_hash"].encode()
    return stored_hash

def check_if_master_password_is_configured():
    config = load_json_file(get_config_path())
    return bool(
        config.get("password_hash")
        and config.get("salt")
    )

# def is_master_password_configured():
#     config = load_json_file(get_config_path())
#     return (
#         config["password_hash"] != "..."
#         and
#         config["salt"] != "..."
#     )
#########################################################################


