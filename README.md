# hspy

# How to use
```shell
python hspy.py --help
```
```plaintext
[alex@archlinux hspy]$ (main)
 » .venv/bin/python main.py --help
usage: main.py [-h] [-e] [-d] [-g] [data]

positional arguments:
  data

options:
  -h, --help     show this help message and exit
  -e, --encrypt  encrypt given string
  -d, --decrypt  decrypt given string
  -g             generates secure password
```

## Generate or manually specify your password
You can automatically generate a secure password by running:
```shell
python hspy.py -g
```
Alternatively, if you do not specify an option, the script will prompt you to enter a password manually.

Keep in mind that ``hspy.py`` uses symmetric encryption. You must use the same salt and password for both encryption and decryption. If you lose your salt or password, your data will be permanently lost.

## Encryption
To encrypt a specific string:
```shell
python hspy.py -e "Some text"
```

You can also use shell substitution to encrypt the contents of a file. For example, to encrypt ``file.txt``:
```shell
python hspy.py -e "$(cat /path/to/file.txt)"
```

## Decryption
To decrypt an encrypted string, use the ``-d`` flag:
```shell
python hspy.py -d "Some encrypted text"
```