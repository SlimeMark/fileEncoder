import binascii
import tkinter as tk
from tkinter import filedialog
import os
import threading
import random

ascii_chars = [chr(i) for i in range(256)]
char_mapping = {}
reversed_char_mapping = {}
shuffled_chars = ascii_chars.copy()
file_extension = ''
file_name = ''
encrypted_file_name = ''
hex_list = []
byte_count = 0


def create_shuffle_mapping(seed):
    global shuffled_chars
    global char_mapping
    global reversed_char_mapping
    random.seed(seed)
    random.shuffle(shuffled_chars)
    char_mapping = {original: shuffled for original, shuffled in zip(ascii_chars, shuffled_chars)}
    reversed_char_mapping = {v: k for k, v in char_mapping.items()}


def get_file_extension(file_path):
    global file_extension
    global file_name
    global encrypted_file_name
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1]
    encrypted_file_name = file_name + '.txt'


def hex_to_save_char(file_path):
    global hex_list
    global byte_count
    with open(file_path, 'rb') as f:
        binary_data = f.read()
    hex_data = binascii.hexlify(binary_data)
    hex_list = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    byte_list = [bytes([ord(char_mapping.get(chr(int(hex, 16)), chr(int(hex, 16))))]) for hex in hex_list]
    byte_count = len(byte_list)
    with open(encrypted_file_name, 'wb') as f:
        f.write(b''.join(byte_list))


if __name__ == "__main__":
    seed = int(input('Enter seed: '))
    with open('seed.txt', 'w', encoding='utf-8') as f:
        f.write(str(seed) + '\n')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    thread0 = threading.Thread(target=create_shuffle_mapping, args=(seed,))
    thread1 = threading.Thread(target=get_file_extension, args=(file_path,))
    thread2 = threading.Thread(target=hex_to_save_char, args=(file_path,))

    thread0.start()
    thread0.join()

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f'Finish writing {byte_count} characters to output')
