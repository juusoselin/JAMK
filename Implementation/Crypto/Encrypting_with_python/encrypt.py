#!/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend

log_file = open('encryption.log', 'a')

## Logging  --  Record start time, duration, end time and process
def logging(method):
	start_pt = time.process_time()
	start_time = time.time()

	print("Encryption process started with " + method + " at \t\t" + str(start_pt) + " (" + str(time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(start_time))) + ")")
	log_file.write("Encryption process started with " + method + " at \t\t" + str(start_pt) + " (" + str(time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(start_time))) + ")\n")

	print("Encrypting...")
	log_file.write("Encrypting...\n")
	files(method)

	end_pt = time.process_time()
	end_time = time.time()
	print("Encryption process ended at \t\t\t" + str(end_pt) + " (" + str(time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(end_time))) + ")\n")

	print("Process time elapsed (seconds): \t\t" + str(end_pt - start_pt))
	print("Total time elapsed (seconds): \t\t\t" + str(end_time - start_time))
	print('-----------------------------------------------------------------')

	log_file.write("Encryption process ended at \t\t\t" + str(end_pt) + " (" + str(time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(end_time))) + ")\n")

	log_file.write("Process time elapsed (seconds): \t\t" + str(end_pt - start_pt) + '\n')
	log_file.write("Total time elapsed (seconds): \t\t\t" + str(end_time - start_time) + '\n')
	log_file.write('-----------------------------------------------------------------\n')


## File and folders  --  Search all the files in given directory
def files(method):
	path = 'Documents_folder/'
	for filename in os.listdir(path):
		if 'enc' not in filename:
			file = open(path + filename, 'rb').read()
			encrypted_file = encryption(file, method)
			f = open(path + filename + '.enc_' + method, 'wb')
			f.write(encrypted_file)
			f.close()

## Encryption  --  Encrypt each file individually
def encryption(file, method):
	backend = default_backend()
	key = b"ihPdmsBrI8xK8RHEDNI6lONw"
	digest = hashes.Hash(hashes.MD5(), backend=default_backend())
	digest.update(key)
	hash_pw = digest.finalize()
	iv = os.urandom(16)
	if method == 'AES':
		cipher = Cipher(algorithms.AES(hash_pw), modes.CBC(iv), backend=backend)
	elif method == 'Camellia':
		cipher = Cipher(algorithms.Camellia(hash_pw), modes.CBC(iv), backend=backend)
	elif method == 'TripleDES':
		iv = os.urandom(8)
		cipher = Cipher(algorithms.TripleDES(hash_pw), modes.CBC(iv), backend=backend)
	elif method == 'Blowfish':
		iv = os.urandom(8)
		cipher = Cipher(algorithms.Blowfish(hash_pw), modes.CBC(iv), backend=backend)
	elif method == 'ARC4':
		cipher = Cipher(algorithms.ARC4(hash_pw), mode=None, backend=backend)
	elif method == 'IDEA':
		iv = os.urandom(8)
		cipher = Cipher(algorithms.IDEA(hash_pw), modes.CBC(iv), backend=backend)
	else:
		sys.exit()

	encryptor = cipher.encryptor()
	padder = padding.PKCS7(128).padder()
	padded_file = padder.update(file) + padder.finalize()
	ct = encryptor.update(padded_file) + encryptor.finalize()

	#decryptor = cipher.decryptor()
	#plaintxt = decryptor.update(ct) + decryptor.finalize()
	#unpadder = padding.PKCS7(128).unpadder()
	#unpadded_plaintxt = unpadder.update(plaintxt) + unpadder.finalize()
	
	return ct


# Main function
def main():
    subprocess.call('clear', shell=True)                                # Clear the screen
    logging('AES')
    logging('Camellia')
    logging('TripleDES')
    logging('Blowfish')
    logging('ARC4')
    logging('IDEA')

if __name__ == '__main__':
    sys.exit(main())
