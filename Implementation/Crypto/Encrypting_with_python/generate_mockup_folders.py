#!/bin/env python3
# -*- coding: utf-8 -*-

#################################################################################################################
#																												#
#	This script generates a folder containing random files 														#
#																												#
#	Usage: 	generate_mockup_folders.py --max-files 1000 --max-size 1											#
#																												#
#			(Generates folder containing less than 1000 files with total size of the folder less thab 1 GB)		#
#																												#
#################################################################################################################

## Imports
import sys, os, random, getopt, string

## Setup
file_extensions = ['exe', 'dll', 'jpg', 'png', 'docx', 'xlsx', 'pdf', 'zip', 'rar', '7z', 'bin', 'mp3', 'wav', 'mp4', 'mkv', 'avi', 'flac', 'ogg', 'mov', 'iso', 'dat', 'db', 'jar', 'bmp', 'jpeg', 'psd', 'tif', 'pptx', 'wmv', 'odt', 'ods', 'odp']

def main():
	parameters = arguments(sys.argv[1:])
	max_files = int(parameters[0])
	max_size = int(parameters[1]) * 1000000000
	size_counter = 0
	file_counter = 0
	folder = "Documents_" + str(parameters[1]) + 'GB_' + str(max_files) + 'files'
	if os.path.isdir(folder):
		print("Folder already exists")
		sys.exit()
	else:
		os.makedirs(folder)
		while size_counter < max_size and file_counter < max_files:
			current_file_size = create_a_file(folder, max_files, max_size)
			size_counter = size_counter + current_file_size
			file_counter = file_counter + 1


def arguments(argv):
	'''
		Parse commandline arguments
	'''
	try:
		opts, args = getopt.getopt(argv, "h", ["help", "max-size=", "max-files="])
	except getopt.GetoptError as e:
		print("\n")
		print("  " + str(e))
		usage()
		sys.exit(2)

	max_size = None
	max_files = None

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt == "--max-size":
			max_size = arg
		elif opt == "--max-files":
			max_files = arg
		else:
			usage()
			sys.exit()
	if max_files.isnumeric() and max_size.isnumeric():				# Check that the valuas are numeric
		return max_files, max_size
	else:
		usage()
		sys.exit()

def create_a_file(path, max_files, max_size):
	name = ''.join(random.choice(string.ascii_lowercase) for i in range(5, random.randint(6, 32)))
	name = name + '.' + random.choice(file_extensions)
	if (max_size <= 1000000000 and max_files >= 1000):
		# Average file should be 1 MB
		file_size = random.randint(100, 2000000)
	elif (max_size <= 1000000000 and max_files >= 100) or (max_size <= 10000000000 and max_files >= 1000):
		# Average file should be 10 MB
		file_size = random.randint(100, 20000000)
	elif (max_size <= 10000000000 and max_files >= 100):
		# Average file should be 100 MB
		file_size = random.randint(100, 200000000)
	payload = os.urandom(file_size)
	file = open(path + '/' + name, 'wb')
	file.write(payload)
	file.close()
	return file_size

def usage():
	'''
		Print usage info
	'''
	print(
	'''
  USAGE:

  --help			Display this help
  --max-files		Maximum number of files to be created  		(100 / 1000)
  --max-size		Maximum total size (GB) for the folder		(1 GB / 10 GB / 100 GB)
	'''
	)

if __name__ == "__main__":
	main()