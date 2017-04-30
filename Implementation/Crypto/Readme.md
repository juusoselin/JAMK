# Tools for the encryption assignment

## Encrypting with python
**encrypt.py** encrypts all the subfolders and their contents in a working directory with either AES, Camellia, TripleDES, Blowfish, ARC4 or IDEA, records the time and process time taken by each process and outputs them to _encryption.log_.

**generate_mockup_folders.py** creates folder containing random binary files with following parameters 

```
--max-files		Maximum number of files to be created  		(100 / 1000)
--max-size		Maximum total size (GB) for the folder		(1 GB / 10 GB / 100 GB)

```

## Malware Analysis
**file_info.sh** is a small Bash script to run various static analysis tools in a row. Outputs are located in the _Static_-folder.

**Dynamic**-folder also contains Wireshark captures as well as information about the dynamic links.

