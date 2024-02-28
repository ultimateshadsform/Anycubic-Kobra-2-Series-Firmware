#!/usr/bin/env python3

from Crypto.Cipher import AES
import os
import sys, getopt

def remove_padding(file_path):
    with open(file_path, 'rb+') as file:
        file.seek(-1, os.SEEK_END)
        padding_value = ord(file.read(1))
        file.seek(-padding_value, os.SEEK_END)
        file.truncate()

def decrypt_aes_cbc(input_file, output_file, first_aes_key, second_aes_key, offset=32):
    block_size = 16

    # Convert hex keys to bytes
    first_aes_key_bytes = bytes.fromhex(first_aes_key)

    # Read IV from the second AES key
    iv = bytes.fromhex(second_aes_key[:32])

    # Create AES cipher objects
    cipher = AES.new(first_aes_key_bytes, AES.MODE_CBC, iv)

    with open(input_file, 'rb') as file_input:
        # Seek to the specified offset
        file_input.seek(offset)

        with open(output_file, 'wb') as file_output:
            while True:
                ciphertext = file_input.read(block_size)
                if not ciphertext:
                    break

                # Decrypt the block
                plaintext = cipher.decrypt(ciphertext)
                file_output.write(plaintext)

    # Remove padding
    remove_padding(output_file)

def main(argv):
    input_file_path = ''
    output_file_path = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('ack2_swu_decrypt.py -i update.bin -o update.zip')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('ack2_swu_decrypt.py -i update.bin -o update.zip')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file_path = arg
        elif opt in ("-o", "--ofile"):
            output_file_path = arg
    print ('AnyCubic Kobra 2 BIN to SWU Converter V1.0')
    print ('Input  file: ', input_file_path)
    print ('Output file: ', output_file_path)
    first_aes_key_hex = "78B6A614B6B6E361DC84D705B7FDDA33C967DDF2970A689F8156F78EFE0B1FCE"
    second_aes_key_hex = "54E37626B9A699403064111F77858049"
    offset_value = 32  # Provide the offset value if needed
    print ('Processing...')
    decrypt_aes_cbc(input_file_path, output_file_path, first_aes_key_hex, second_aes_key_hex, offset_value)
    print ('Done!')
   
main(sys.argv[1:])

