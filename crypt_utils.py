from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from typing import Optional
import secrets, os

working_dir = os.path.dirname(os.path.realpath(__file__))
salt_file = "c/salt"
salt_file_path = f"{working_dir}/{salt_file}"
password_file = "c/password"
password_file_path = f"{working_dir}/{password_file}"

from base62 import encode_base62, decode_base62

def generate_secure_password() -> str:
    return secrets.token_urlsafe(24) # 32 symbols

def load_existing_password() -> str:
    password = open(password_file_path, "r").read()
    return password

def generate_secure_salt() -> bytes:
    return secrets.token_bytes(32)

def load_existing_salt() -> bytes:
    salt = open(salt_file_path, "r").read().strip()
    return bytes.fromhex(salt)

def derive_key(salt:bytes, password:str) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def generate_key(password:Optional[str]=None, save_salt:bool=True, use_saved_salt:bool=True, save_password:bool=True, use_saved_password:bool=True) -> bytes:
    if use_saved_salt and os.path.exists(password_file_path) and os.path.getsize(salt_file_path) > 0:
        salt = load_existing_salt()
    else:
        salt = generate_secure_salt()
    
    if not password:
        
        if use_saved_password and os.path.exists(password_file_path) and os.path.getsize(password_file_path) > 0:
            password = load_existing_password()
        else:
            password = generate_secure_password()

    if save_salt:
        with open(salt_file_path, "w") as file:
            file.write(salt.hex())
    
    if save_password:
        with open(password_file_path, "w") as file:
            file.write(password)

    key = derive_key(salt=salt, password=password)
    
    return key

def encrypt_message(unencrypted_message:str, key:bytes) -> str: # base62 string bc why not
    aead = ChaCha20Poly1305(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aead.encrypt(nonce, unencrypted_message.encode(), None)

    return encode_base62(nonce + ciphertext)

def decrypt_message(encrypted_message:str, key:bytes) -> str:
    aead = ChaCha20Poly1305(key)
    token = decode_base62(encrypted_message)
    nonce, ciphertext = token[:12], token[12:]

    return aead.decrypt(nonce, ciphertext, None).decode()