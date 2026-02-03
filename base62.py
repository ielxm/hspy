import string

ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase

def encode_base62(data:bytes|str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    
    num = int.from_bytes(data, "big")
    if num == 0:
        return ALPHABET[0]
    chars = []
    base = len(ALPHABET)
    while num > 0:
        num, rem = divmod(num, base)
        chars.append(ALPHABET[rem])
    return ''.join(reversed(chars))

def decode_base62(data:str) -> bytes:
    base = len(ALPHABET)
    num = 0
    for char in data:
        num = num * base + ALPHABET.index(char)
    length = (num.bit_length() + 7)//8
    return num.to_bytes(length, "big")