import json

from functions import txt, txtError,txtInfo, txtSuccess, load_language

from constants import FILE_SETTINGS


# TEST FOR URL USER DOWNLOAD LAST VERSION APP : https://github.com/Gwigzz/safebox
URL_DOWNLOAD_APP = "https://github.com/Gwigzz/safebox"

lang = load_language()

def version_to_tuple(version):
    return tuple(map(int, version.split(".")))

# def get_online_version():
#     """ return online version from github repo """
#     if BASE_URL_SETTINGS is False:
#         txtError(f"Update url is invalid or empty in settings.json. URL : {BASE_URL_SETTINGS}")
#         input('...')
#     try:
#         data = requests.get(BASE_URL_SETTINGS, timeout=5).json()
#         return data
#     except Exception as err:
#         print(f"Error checking online version ... Please try again or contact us. Code error : ({err})")
#         input('...')
#         return False

def get_local_version():
    """ return current local version from computeur """
    try:
        with open(FILE_SETTINGS, "r") as local_version: 
            data = json.load(local_version)
            return data
    except Exception as err:
        print(f"Error checking local version ... ({err})")
        return False

# def check_versions():

#     online  = get_online_version()
#     local   = get_local_version()

#     online_version      = online.get('app_version')
#     local_version       = local.get('app_version')

#     if not online:
#         txtError("Error get_online_version()")
#         return
        
#     if not local:
#         txtError("Error get_local_version()")
#         return

#     # compare version
#     if version_to_tuple(online_version) > version_to_tuple(local_version):

#         txtInfo(f"{lang.update.available}")

#         txtError(f"{lang.update.v_local}: {local_version}")
#         txtSuccess(f"{lang.update.v_online}: {online_version}")

#         txtInfo(f"{lang.update.dwnl_help} : {URL_DOWNLOAD_APP}")

#     else:
#         txtSuccess(f"{lang.update.success} V {local_version}")

# --------------------------------------

def compare_settings(local_data, online_data):
    """
    Compare two dictionaries:
    - missing keys
    - extra keys
    - modified values
    - unchanged values

    Return dict with results.
    """

    ignored_keys = {"lang"}

    result = {
        "missing_keys": [],
        "extra_keys": [],
        "modified_values": {},
        "same_values": {}
    }

    local_keys = set(local_data.keys())
    online_keys = set(online_data.keys())

    # Removed keys
    result["missing_keys"] = list(local_keys - online_keys)

    # New keys
    result["extra_keys"] = list(online_keys - local_keys)

    # Compare values
    for key in local_keys.intersection(online_keys):
        if key in ignored_keys:
            continue

        if local_data[key] != online_data[key]:
            result["modified_values"][key] = {
                "local": local_data[key],
                "online": online_data[key]
            }
        else:
            result["same_values"][key] = local_data[key]

    return result

