import binascii
import tkinter as tk
from tkinter import filedialog
import os
import threading

file_extension = ''
file_name = ''
encrypted_file_name = ''
hex_list = []
byte_count = 0
char_mapping = {
    'A': '!', 'B': '@', 'C': '#', 'D': '$', 'E': '%', 'F': '^', 'G': '&', 'H': '*', 'I': '(', 'J': ')', 'K': '-',
    'L': '+', 'M': '[', 'N': ']', 'O': '{', 'P': '}', 'Q': ';', 'R': ':', 'S': ',', 'T': '.', 'U': '<', 'V': '>',
    'W': '/', 'X': '?', 'Y': '`', 'Z': '~',
    'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '0', 'k': 'a',
    'l': 'b', 'm': 'c', 'n': 'd', 'o': 'e', 'p': 'f', 'q': 'g', 'r': 'h', 's': 'i', 't': 'j', 'u': 'k', 'v': 'l',
    'w': 'm', 'x': 'n', 'y': 'o', 'z': 'p',
    '0': 'q', '1': 'r', '2': 's', '3': 't', '4': 'u', '5': 'v', '6': 'w', '7': 'x', '8': 'y', '9': 'z'
}
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
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    thread1 = threading.Thread(target=get_file_extension, args=(file_path,))
    thread2 = threading.Thread(target=hex_to_save_char, args=(file_path,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f'Finish writing {byte_count} characters to output')
