#coding=utf-8
from capstone import *

syscallname_dic = {}
syscallnum_dic = {}
with open("syscall64.txt", "r") as file:
	for line in file:
		(key, val) = line[13:].split()
		syscallname_dic[key] = val
		syscallnum_dic[val] = key
file.close()
data = ''

while True:
	print("+=================================+")
	print("|  1. Add hexadecimal addresses".ljust(34,' ')+'|')
	print("|  2. Hexadecimal address offset".ljust(34,' ')+'|')
	print("|  3. String length".ljust(34,' ')+'|')
	print("|  4. String reverse order".ljust(34,' ')+'|')
	print("|  5. System call query".ljust(34,' ')+'|')
	print("|  6. Disassembly".ljust(34,' ')+'|')
	print("+=================================+")
	choice = input('Enter your choice(Enter exit to leave)>> ')
	if choice == '1':
		while True:
			try:
				addr1 = input('Enter hexadecimal address1(Enter quit to return):\n')
				if addr1 == 'quit':
					print("bye~")
					break
				addr1 = int(addr1,16)
				addr2 = input('Enter hexadecimal address2:\n')
				addr2 = int(addr2,16)
				add = addr1 + addr2
				print('addition: ',hex(add))
			except:
				print("error :(")
	elif choice == '2':
		while True:
			try:
				addr1 = input('Enter hexadecimal address1(Enter quit to return):\n')
				if addr1 == 'quit':
					print("bye~")
					break
				addr1 = int(addr1,16)
				addr2 = input('Enter hexadecimal address2:\n')
				addr2 = int(addr2,16)
				offset = abs(addr1 - addr2)
				print('offset: ',hex(offset))
			except:
				print("error :(")
	elif choice == '3':
		while True:
			try:
				str1 = input('Input string(Enter quit to return):\n')
				if str1 == 'quit':
					print("bye~")
					break
				print('len:',len(str1))
			except:
				print("error :(")
	elif choice == '4':
		while True:
			try:
				str1 = input('Input string(Enter quit to return):\n')
				if str1 == 'quit':
					print("bye~")
					break
				print('reverse:',str1[::-1])
			except:
				print("error :(")
	elif choice == '5':
		while True:
			while True:
				data = input('Enter the system call, query the system call number, and enter a to query in reverse(Enter quit to return):\n')
				if data == 'a' or data == 'quit':
					break;
				if data in syscallname_dic:
					print('The system call number is: '+ syscallname_dic[data])
				else:
					print("error :(")
			if data == 'quit':
				print("bye~")
				break
			while True:
				data = input('Enter the system call number to query the system call, and enter b to query the system call in reverse(Enter quit to return):\n')
				if data == 'b' or data == 'quit':
					break;
				if data in syscallnum_dic:
					print('The system call is: '+ syscallnum_dic[data])
				else:
					print("error :(")
			if data == 'quit':
				print("bye~")
				break
	elif choice == '6':
		while True:
			try:
				code_hex = input("Input hexadecimal byte sequence(Enter quit to return):\n")
				if code_hex == 'quit':
					print("bye~")
					break
				CODE = bytes.fromhex(code_hex)
				print("Disassembly:")
				md = Cs(CS_ARCH_X86, CS_MODE_64)
				for i in md.disasm(CODE, 0x0):
					print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
			except:
				print("error :(")
	elif choice == 'exit':
		break
	else:
		print("error :(")

