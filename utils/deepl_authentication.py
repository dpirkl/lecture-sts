import os
import deepl
import deepl.exceptions as deepl_exceptions


#validate setup

path_to_licence_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_to_key_file = os.path.join(path_to_licence_folder, 'data', 'licence', 'DEEPL_AUTH_KEY.txt')


def validate_key(key: str) -> bool:
    """Validate the key.

    Args:
        key: the key to validate

    Returns: whether the key is valid

    """
    try:
        print(deepl.Translator(key).translate_text("Hallo, ich will etwas übersetzen.", target_lang="EN-GB"))
        return True
    except deepl_exceptions.AuthorizationException:
        return False
    except Exception as e:
        raise RuntimeError(f"Something went wrong. Try again later. Exception: {e}")


def get_key() -> str:
    with open(path_to_key_file) as key_file:
        return key_file.read()


def save_key(key: str) -> None:
    """Write the key to the keys.txt file.

    Args:
        key: the DEEPL_AUTH_KEY

    """

    if not os.path.exists(path_to_key_file):

        if validate_key(key):
            
            with open(path_to_key_file, "w") as key_file:
                key_file.write(key)
            print(f"Successfully saved the key to {path_to_key_file} and validated it.")
        # don't save an invalid key
        else:
            raise ValueError("Key is not valid. Try another key.")

    else:
        raise ValueError(f"Key already exists at {path_to_key_file}. If you want to change the key, delete the file "
                         f"and try again.")

