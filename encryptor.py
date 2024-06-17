import binascii
import sys
import os
import threading

file_extension = ''
file_name = ''
encrypted_file_name = ''
hex_list = []
char_count = 0


def get_file_extension(file_path):
    global file_extension
    global file_name
    global encrypted_file_name
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1]
    encrypted_file_name = file_name.replace(file_name, '.txt')


def hex_to_save_char(file_path):
    global hex_list
    global char_count
    with open(file_path, 'rb') as f:
        binary_data = f.read()
    hex_data = binascii.hexlify(binary_data)
    hex_list = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    char_list = [chr(int(hex, 16)) for hex in hex_list]
    char_count = len(char_list)
    with open(encrypted_file_name, 'w') as f:
        f.write(''.join(char_list))


if __name__ == "__main__":
    file_path = sys.argv[1]
    thread1 = threading.Thread(target=get_file_extension, args=(file_path,))
    thread2 = threading.Thread(target=hex_to_save_char, args=(file_path,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f'Finish writing {char_count} characters to output')
