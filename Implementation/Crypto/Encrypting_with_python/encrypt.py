#!/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.backends import default_backend


## Logging  --  Record start time, duration, end time and process
def logging(method, algorithm):
	for directory in os.listdir(os.getcwd()):
		if os.path.isdir(directory):
			path = directory

			log_file = open('encryption.log', 'a')

			start_pt = time.process_time()
			start_time = time.time()

			print("Encryption process started with " + method + " at \t\t" + str(start_pt) + " (" + str(time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(start_time))) + ")")
			log_file.write("Encryption process started with " + method + " at \t\t" + str(start_pt) + " (" + str(time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(start_time))) + ")\n")

			print("Encrypting folder " + path + "...")
			log_file.write("Encrypting " + path + "...\n")
			files(method, algorithm, path)

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
			log_file.close()

## File and folders  --  Search all the files in given directory
def files(method, algorithm, path):
	for filename in os.listdir(path):
		if 'enc' not in filename:
			file = open(path + '/' + filename, 'rb').read()
			print('Encrypting file: ' + path + '/' + filename)
			if algorithm == 'symmetric':
				encrypted_file = symmetric_encryption(file, method)
			elif algorithm == 'asymmetric':
				encrypted_file = ''
				for i in range(0, len(file), 200):
					encrypted_line = asymmetric_encryption(file[i:(i+200)], method)
					print(i)
					encrypted_file = encrypted_file + str(encrypted_line)
				encrypted_file = bytes(encrypted_file, encoding="UTF-8")
			else:
				sys.exit()
			f = open(path + '/' + filename + '.enc_' + method, 'wb')
			f.write(encrypted_file)
			f.close()

## Encryption  --  Encrypt each file individually
def symmetric_encryption(file, method):
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

def asymmetric_encryption(file, method):
	if method == 'RSA':
		with open('public_key_rsa.pem', 'rb') as public_key_file:
			public_key = serialization.load_pem_public_key(public_key_file.read(), backend=default_backend())
		ciphertext = public_key.encrypt(file, asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))

	return ciphertext


# Main function
def main():
    subprocess.call('clear', shell=True)                                # Clear the screen
    logging('AES', 'symmetric')
    logging('Camellia', 'symmetric')
    logging('TripleDES', 'symmetric')
    logging('Blowfish', 'symmetric')
    logging('ARC4', 'symmetric')
    logging('IDEA', 'symmetric')
    #logging('RSA', 'asymmetric')

if __name__ == '__main__':
    sys.exit(main())
