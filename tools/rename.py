#coding=utf-8
import os

def get_filename_list(directory):
    filename_list = os.listdir(directory)
    return filename_list

directory = input('Enter file directory >> ')

while True:
	print("+=================================================+")
	print("|  1. Delete renaming of specified characters".ljust(50,' ')+'|')
	print("|  2. Add renaming of specified characters".ljust(50,' ')+'|')
	print("|  3. Replace renaming of specified characters".ljust(50,' ')+'|')
	print("+=================================================+")
	choice = input('Enter your choice(Enter exit to leave) >> ')
	if choice == '1':
		while True:
			filename_list = get_filename_list(directory)
			try:
				new_filename = ""
				filename = ""
				delete_strings = input('Enter the strings to be deleted(Enter quit to return):\n')
				if delete_strings == 'quit':
					print("bye~")
					break
				for i in range(len(filename_list)):
					filename = filename_list[i]
					if filename.find(delete_strings)!=-1:
						
						new_filename = filename.replace(delete_strings,"")
						filename = directory + "\\" + filename
						new_filename = directory + "\\" +new_filename
						os.rename(filename, new_filename)
			except:
				print("error :(")
	# elif choice == '2':
	elif choice == '3':
		while True:
			filename_list = get_filename_list(directory)
			try:
				new_filename = ""
				filename = ""
				replace_strings = ""

				replaced_strings = input('Enter the replaced strings(Enter quit to return):\n')
				if replaced_strings == 'quit':
					print("bye~")
					break

				replace_strings = input('Enter replacement strings:\n')
				for i in range(len(filename_list)):
					filename = filename_list[i]
					if filename.find(replaced_strings)!=-1:

						new_filename = filename.replace(replaced_strings, replace_strings)
						filename = directory + "\\" + filename
						new_filename = directory + "\\" +new_filename
						os.rename(filename, new_filename)
			except:
				print("error :(")

	elif choice == 'exit':
		break
	else:
		print("error :(")





