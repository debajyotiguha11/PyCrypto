from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys, pkg_resources

def encrypt(key, filename):
	chunksize = 64 * 1024
	outFile = os.path.join(os.path.dirname(filename), "(encrypted)"+os.path.basename(filename))
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))
	
	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, "rb") as infile:
		with open(outFile, "wb") as outfile:
			outfile.write(filesize)
			outfile.write(IV)
			while True:
				chunk = infile.read(chunksize)
				
				if len(chunk) == 0:
					break

				elif len(chunk) % 16 !=0:
					chunk += ' ' *  (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
	chunksize = 64 * 1024
	with open(filename, "rb") as infile:
		filesize = infile.read(16)
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)
		
		with open(outFile, "wb") as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(int(filesize))
	
def allfiles():
	allFiles = []
	for root, subfiles, files in os.walk(os.getcwd()):
		for names in files:
			allFiles.append(os.path.join(root, names))

	return allFiles

	
choice = raw_input("Do you want to (E)ncrypt or (D)ecrypt? *Use CapitalLatter*")
password = raw_input("Enter the password: ")

encFiles = allfiles()

if choice == "E":
	for Tfiles in encFiles:	
		if os.path.basename(Tfiles).startswith("(encrypted)"):
			print "%s is already encrypted" %str(Tfiles)
			pass

		elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
			pass 
		else:
			encrypt(SHA256.new(password).digest(), str(Tfiles))
			print "Done encrypting %s" %str(Tfiles)
			os.remove(Tfiles)


elif choice == "D":
	filename = raw_input("Enter the filename to decrypt: ")
	if not os.path.exists(filename):
		print "The file does not exist"
		sys.exit(0)
	elif not filename.startswith("(encrypted)"):
		print "%s is already not encrypted" %filename
		sys.exit()
	else:
		decrypt(SHA256.new(password).digest(), filename)
		print "Done decrypting %s" %filename
		os.remove(filename)

else:
	print "Please choose a valid command."
	sys.exit()
