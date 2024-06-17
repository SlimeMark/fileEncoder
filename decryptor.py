import binascii
import tkinter as tk
from tkinter import filedialog
import os
import threading
import encryptor

file_extension = ''
file_name = ''
decrypted_file_name = ''
hex_list = []
byte_count = 0
char_mapping = encryptor.reversed_char_mapping


def get_original_filename(file_path):
    global file_extension
    global file_name
    global decrypted_file_name
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1]
    decrypted_file_name = file_name.replace('.txt', '')


def char_to_save_hex(file_path):
    global hex_list
    global byte_count
    with open(file_path, 'rb') as f:
        byte_data = f.read()
    char_list = [chr(byte) for byte in byte_data]
    hex_list = [binascii.hexlify(bytes([ord(char_mapping.get(char, '\0'))])) for char in char_list]
    byte_count = len(hex_list)
    with open(decrypted_file_name, 'wb') as f:
        for hex in hex_list:
            f.write(binascii.unhexlify(hex))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    thread1 = threading.Thread(target=get_original_filename, args=(file_path,))
    thread2 = threading.Thread(target=char_to_save_hex, args=(file_path,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f'Finish writing {byte_count} bytes to output')