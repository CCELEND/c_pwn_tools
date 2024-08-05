#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import yagmail
import shutil
import random
import string
import threading
import time
import sys
import re
import os

LOGO_COLOR = """\033[32m\033[1m
	  .oooooo.                                        .o8                               o8o  oooo    .oooo.   
	 d8P'  `Y8b                                      "888                               `"'  `888  .dP""Y88b  
	888           .oooo.o  .ooooo.  ooo. .oo.    .oooo888  ooo. .oo.  .oo.    .oooo.   oooo   888        ]8P' 
	888          d88(  "8 d88' `88b `888P"Y88b  d88' `888  `888P"Y88bP"Y88b  `P  )88b  `888   888      .d8P'  
	888          `"Y88b.  888ooo888  888   888  888   888   888   888   888   .oP"888   888   888    .dP'     
	`88b    ooo  o.  )88b 888    .o  888   888  888   888   888   888   888  d8(  888   888   888  .oP     .o 
	 `Y8bood8P'  8""888P' `Y8bod8P' o888o o888o `Y8bod88P" o888o o888o o888o `Y888""8o o888o o888o 8888888888\033[0m

	                                       \033[33m\033[1mWelcome to the Csendmail2                                   
	      This tool can send emails and attachments with random string content through multiple threads 
	                                         Use for stress testing 
	                                               Version 2.2\033[0m   
"""

HELP_INFO = """\033[35m\033[1mNAME\033[0m
    Csendmail2.py - send emails and attachments with random string content
\033[35m\033[1mSYNOPSIS\033[0m
    python3 Csendmail2.py [options...] or 
    ./Csendmail2.py [options...]
\033[35m\033[1mDESCRIPTION\033[0m
    -t <thread number>, --thread=<thread number>
        The maximum number of threads to be enabled is 16
    -n <emails number>, --mail=<emails number>
        The number of emails sent by each thread
    -se <sender address>, --sender=<sender address>
        Sender address
    -re <receiver address>, --receiver=<receiver address>
        Receiver address
    -ho <smtp server>, --host=<smtp server>
        Smtp server address
    -pa <authorization code>, --password=<authorization code>
        Authorization code
    -po <port number>, --port=<port number>
        SMTP server port: 465 or 25
    -at <true|false>, --attachment=<true|false>
        Enable attachment mode or not
    -atl <attachment length>, --atlength=<attachment length>
        Maximum length of attachment: 30MB or 30720KB at most; The minimum is 0KB    
        This option is required when enable attachment mode
    -de, --delete
        Delete files in the attachment directory
    -v, --version
        Version information
    -h, --help
        Help information"""

def help():
	print(HELP_INFO)

def err_msg(msg):
	print("\033[31m\033[1m[-]\033[0m " + msg)

def good_msg(msg):
	print("\033[32m\033[1m[+]\033[0m " + msg)

def note_msg(msg):
	print("\033[34m\033[1m[*]\033[0m " + msg)

def info_msg_all(msg):
	print("\033[33m\033[1m" + msg + "\033[0m")

# 生成随机字符串，包括大小写字母、数字和标点符号
def generate_random_string_with_visible_chars(length):
	characters = string.ascii_letters + string.digits + string.punctuation
	random_string = ''.join(random.choices(characters, k = length))
	return random_string
   
# 生成一个1到num_end范围内的随机整数 
def generate_random_number_end_at(num_end):
	return random.randint(1, num_end)

# 生成随机字符串的文件名，包括字母、数字
def generate_random_string_file_name(length):
	characters = string.ascii_letters + string.digits
	random_string = ''.join(random.choices(characters, k=length))
	return random_string

# 创建附件目录
def create_attachment_directory():
	if not os.path.exists("attachment"):
		try:
			os.makedirs("attachment")
			good_msg("Attachment directory [attachment] has been created.")
		except Exception as e:
			err_msg("Attachment directory [attachment] creation failed: " + str(e))

# 生成附件
def generate_attachment(attachment_path, content, file_type):
	if file_type == 'txt':
		with open(attachment_path, 'w', encoding = 'utf-8') as file:
			file.write(content)
	elif file_type == 'bin':
		with open(attachment_path, 'wb') as file:
			file.write(content.encode("utf-8"))

# 删除附件目录下的文件
def delete_attachment():
	# 定义文件路径
	attachment_path = "attachment"

	# 检查文件路径是否存在
	if os.path.exists(attachment_path):
		try:
			# 使用with语句来处理文件和目录的删除
			with os.scandir(attachment_path) as dir_list:
				for entry in dir_list:
					if entry.is_file() or entry.is_symlink():
						os.remove(entry.path)
					elif entry.is_dir():
						shutil.rmtree(entry.path)
			good_msg("Successfully deleted files in the [attachment].")
		except Exception as e:
			err_msg("Failed to delete files in the [attachment]: " + str(e))
	else:
		err_msg("Attachment directory [attachment] does not exist!")


# 从字符串提取数
def get_num_from_string(string):
	match = re.search(r'\d+(\.\d+)?', string)
	if match:
		number = match.group()
		return float(number)
	else:
		err_msg("No number found!")
		return 0

MB = 1048576
KB = 1024
MB_LIMIT = 30
KB_LIMIT = 30720
THREAD_LIMIT = 16
SMTP_PORT = 25
SMTP_SSL_PORT = 465

thread_state = True
# 发送邮件的工作线程
def send_mail(thread_name, sender, password, host, port, 
		receiver, mail_num, attachment_mode, atlength):

	global thread_state
	#初始化 yagmail
	yag = yagmail.SMTP(user = sender, 
		password = password, 
		host = host, 
		port = port)

	# 邮件主题和内容
	subject_length = 0
	subject_contents = ""
	body_length = 0
	body_contents = ""

	# 附件名和内容
	attachment_name_length = 0
	attachment_name = ""
	attachment_contents_length = 0;
	attachment_contents = ""
	# 获得字符串中的数
	atlength_num = get_num_from_string(atlength)

	for i in range(0, mail_num):
		# 生成邮件主题和内容
		subject_length = generate_random_number_end_at(20)
		subject_contents = generate_random_string_with_visible_chars(subject_length)
		body_length = generate_random_number_end_at(1 * KB)
		body_contents = generate_random_string_with_visible_chars(body_length)

		# 每发送20个邮件时暂停1s
		if (i % 20 == 0 and i != 0):
			time.sleep(1)

		subject_contents = '{}-[{}]'.format(subject_contents, str(i).zfill(3))
		body_contents = '{}-[{}]'.format(body_contents, str(i).zfill(3))
		try:
			# 附件模式
			if attachment_mode:
				# 生成附件名和内容
				attachment_name_length = generate_random_number_end_at(20)
				attachment_name = generate_random_string_file_name(attachment_name_length)

				if 'MB' in atlength:
					attachment_contents_length = generate_random_number_end_at(int(atlength_num * MB))
				else:
					attachment_contents_length = generate_random_number_end_at(int(atlength_num * KB))

				attachment_contents = generate_random_string_with_visible_chars(attachment_contents_length)
				# 创建附件文件 
				attachment_path = 'attachment/' + attachment_name
				generate_attachment(attachment_path, attachment_contents, file_type = 'bin')

			#发送邮件
				yag.send(to = receiver, subject = subject_contents, contents = [body_contents, attachment_path])
			else:
				yag.send(to = receiver, subject = subject_contents, contents = body_contents)
			print('  \033[32m\033[1m[+]\033[0m   {}    {}          Email sent successfully.'.format(thread_name, str(i).zfill(3)))
		except Exception as e:
			print('  \033[31m\033[1m[-]\033[0m   {}    {}          Email sending failed: {}'.format(thread_name, str(i).zfill(3), str(e)))
			thread_state = False
			yag.close()
			exit()

	yag.close()

# 显示参数
def parameter_display(param_dir):
	good_msg("Parameter analysis:")
	print(param_dir)

# 单参数处理
def single_parameter(param):
	if param in ['-h', '--help']:
		help()
		exit()
	elif param in ['-de', '--delete']:
		delete_attachment()
		exit()
	elif param in ['-v', '--version']:
		exit()
	else:
		err_msg("Parameter error!")
		help()
		exit()


# 判断是否存在错误的参数，有错误就返回 true
def is_error_arg(param_dir):
	is_error_flag = True;
	is_attachment_mode = False

	for param, value in param_dir.items():
		if value is None and param not in ['-atl', 'atlength']:
			return True

		elif param in ['-t', 'thread']:
			try:
				thread_num = int(value)
				if thread_num > 0 and thread_num <= THREAD_LIMIT:
					is_error_flag = False
				else:
					return True
			except:
				return True
		elif param in ['-n', 'mail']:
			try:
				mail_num = int(value)
				if mail_num > 0:
					is_error_flag = False
				else:
					return True
			except:
				return True
		elif param in ['-po', 'port']:
			try:
				port = int(value)
				if port == SMTP_SSL_PORT or port == SMTP_PORT:
					is_error_flag = False
				else:
					return True
			except:
				return True

		# 检查邮件地址的正则表达式
		elif param in ['-re', 'receiver', '-se', 'sender']:
			pattern = re.compile(
				'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
			if (pattern.search(value)):
				is_error_flag = False
			else:
				return True

		elif param in ['-pa', 'password']:
			pattern = re.compile(
				'^[a-zA-Z0-9]{16,16}$')
			if (pattern.search(value)):
				is_error_flag = False
			else:
				return True

		elif param in ['-at', 'attachment']:
			if value == 'true':
				is_attachment_mode = True
				is_error_flag = False;
			elif value == 'false':
				is_attachment_mode = False
				is_error_flag = False;
			else:
				return True

		elif param in ['-atl', 'atlength']:
			if is_attachment_mode:
				if value is None:
					return True
				pattern = re.compile(
					'(^[0-9]{1,2}(\\.[0-9]{1,2})?MB$)|(^[0-9]{1,5}(\\.[0-9]{1,2})?KB$)')
				if (pattern.search(value)):
					num = get_num_from_string(value)
					if 'MB' in value and num > MB_LIMIT:
						return True
					elif 'KB' in value and num > KB_LIMIT:
						return True
					else:
						is_error_flag = False;
				else:
					return True
			else:
				is_error_flag = False;

	return is_error_flag

def main():

	print(LOGO_COLOR)
	if len(sys.argv) == 1:
		help()
		exit()
	elif len(sys.argv) == 2:
		single_parameter(sys.argv[1])

	thread_num = 0
	mail_num = 0
	port = 0
	receiver = ""
	sender = ""
	host = ""
	password = ""
	atlength = ""
	attachment_mode = False

	short_param_dir = {
		'-t': None,
		'-n': None,
		'-re': None,
		'-se': None,
		'-pa': None,
		'-ho': None,
		'-po': None,
		'-at': None,
		'-atl': None
	}
	is_short_param = False

	long_param_dir = {
		'thread': None,
		'mail': None,
		'receiver': None,
		'sender': None,
		'host': None,
		'password': None,
		'port': None,
		'attachment': None,
		'atlength': None
	}
	is_long_param = False

	# 遍历命令行参数（除了脚本名称）
	for i, arg in enumerate(sys.argv[1:]):
		if arg in short_param_dir:
			is_short_param = True
		 	# 下一个参数是当前参数的值
			short_param_dir[arg] = sys.argv[i + 2] if i + 2 < len(sys.argv) else None

		# 处理长格式参数 (例如：--param=value)
		elif arg.startswith('--'):
			is_long_param = True
			param = arg[2:].split('=')[0]
			if param in long_param_dir:
				long_param_dir[param] = arg.split('=')[1] if '=' in arg else None

	if (is_short_param):
		if (is_error_arg(short_param_dir)):
			err_msg("Parameter error!")
			help()
			exit()
		else:
			# parameter_display(short_param_dir)
			thread_num = int(short_param_dir['-t'])
			mail_num = int(short_param_dir['-n'])
			port = int(short_param_dir['-po'])
			receiver = short_param_dir['-re']
			sender = short_param_dir['-se']
			password = short_param_dir['-pa']
			host = short_param_dir['-ho']
			if short_param_dir['-at'] == 'true':
				attachment_mode = True
				atlength = short_param_dir['-atl']
			else:
				attachment_mode = False
				atlength = '0KB'
	else:
		if (is_error_arg(long_param_dir)):
			err_msg("Parameter error!")
			help()
			exit()
		else:
			# parameter_display(long_param_dir)
			thread_num = int(long_param_dir['thread'])
			mail_num = int(long_param_dir['mail'])
			port = int(long_param_dir['port'])
			receiver = long_param_dir['receiver']
			host = long_param_dir['host']
			password = long_param_dir['password']
			sender = long_param_dir['sender']
			if long_param_dir['attachment'] == 'true':
				attachment_mode = True
				atlength = long_param_dir['atlength']
			else:
				attachment_mode = False
				atlength = '0KB'
	# test
	# parameter_display(short_param_dir)
	# parameter_display(long_param_dir)

	# 附件模式
	if attachment_mode:
		create_attachment_directory()

	global thread_state
	note_msg("Creating and starting {} threads...".format(thread_num))
	note_msg("Start sending emails...")
	info_msg_all("  State Thread Name Email Index  Info")
	try:
		# 创建线程列表
		thread_list = []
		# 创建并启动线程
		for i in range(thread_num):
			thread = threading.Thread(target=send_mail, args=("Thread{}".format(str(i).zfill(2)), 
				sender, password, host, port, receiver, mail_num, attachment_mode, atlength))
			thread_list.append(thread)
			thread.start()
		# 等待所有线程完成
		for thread in thread_list:
			thread.join()

		if thread_state:
			good_msg("Email sending completed.")
		else:
			err_msg("Email sending failed!")

	except Exception as e:
		err_msg("Failed to start thread: " + str(e))

if __name__ == '__main__':
	main()
