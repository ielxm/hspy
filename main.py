from crypt_utils import generate_key, encrypt_message, decrypt_message, password_file_path
from getpass import getpass
from sys import exit

import argparse, os

def setup_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument("data", nargs="?")
    parser.add_argument("-e", "--encrypt", action="store_true", help="encrypt given string")
    parser.add_argument("-d", "--decrypt", action="store_true", help= "decrypt given string")
    parser.add_argument("-g", action="store_true", help="generates secure password")
    
    args = parser.parse_args()

    if args.encrypt and args.decrypt:
        exit(1)

    return args

def main():

    args = setup_argparser()

    if not args.g and ( os.path.exists(password_file_path) and os.path.getsize(password_file_path) ) == 0:
        try:
            password = getpass("Enter your password: ")
        except KeyboardInterrupt:
            exit(1)
    else:
        password = None

    key = generate_key(password=password, save_password=True, save_salt=True, use_saved_password=True, use_saved_salt=True)

    if args.data:

        if args.decrypt:
            print(decrypt_message(encrypted_message=args.data, key=key))

        if args.encrypt:
            print(encrypt_message(unencrypted_message=args.data, key=key))

if __name__ == "__main__":
    main()