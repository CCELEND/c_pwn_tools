#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# pyinstaller --onefile --windowed script.py

import tkinter as tk
from tkinter import scrolledtext, Menu, messagebox

STATUSVAL_STATUS = {}
STATUS_STATUSVAL = {}
with open("WinStatus.txt", "r") as file:
	for line in file:
		SplitList = line.split(' ', 5)
		STATUS = SplitList[0]
		STATUSVAL = int(SplitList[1], 0)
		STATUS_STATUSVAL[STATUS] = STATUSVAL
		STATUSVAL_STATUS[STATUSVAL] = STATUS
file.close()

# 右键复制
def copy_text(event, text_widget):
	try:
		# 获取选中的文本
		selected_text = text_widget.get("sel.first", "sel.last")
		if selected_text:
			text_widget.clipboard_clear()
			text_widget.clipboard_append(selected_text)
	except tk.TclError:
		pass  # 如果没有选中文本，忽略错误

# 右键粘贴
def paste_text(event, text_widget):
	try:
		text_widget.insert(tk.INSERT, text_widget.clipboard_get())
	except tk.TclError:
		pass  # 如果剪贴板为空，忽略错误

# 右键剪切
def cut_text(event, text_widget):
	try:
		selected_text = text_widget.get("sel.first", "sel.last")
		if selected_text:
			text_widget.clipboard_clear()
			text_widget.clipboard_append(selected_text)
			text_widget.delete("sel.first", "sel.last")
	except tk.TclError:
		pass

# 右键菜单
def show_context_menu(event, text_widget):
	# 创建上下文菜单
	context_menu = Menu(text_widget, tearoff=0)
	context_menu.add_command(label="复制", command=lambda e=event: copy_text(e, text_widget))
	context_menu.add_command(label="粘贴", command=lambda e=event: paste_text(e, text_widget))
	context_menu.add_command(label="剪切", command=lambda e=event: cut_text(e, text_widget))
	# 在鼠标右键点击的位置显示菜单
	context_menu.tk_popup(event.x_root, event.y_root)
	context_menu.grab_release()

# 清空输入输出框
def clear_text(*text_widgets):
	for text_widget in text_widgets:
		if text_widget.cget('state') == tk.DISABLED:
			text_widget.config(state=tk.NORMAL)
			text_widget.delete("1.0", tk.END)
			text_widget.config(state=tk.DISABLED)
		else:
			text_widget.delete("1.0", tk.END)

# 编辑文本框
def edit_text(text_widget, data):
	if text_widget.cget('state') == tk.DISABLED:
		text_widget.config(state=tk.NORMAL)
		text_widget.delete("1.0", tk.END)
		text_widget.insert(tk.END, data)
		text_widget.config(state=tk.DISABLED)
	else:
		text_widget.delete("1.0", tk.END)
		text_widget.insert(tk.END, data)

def STATUSVAL_to_STATUS():
	STATUSVAL_STR = input_text.get("1.0", tk.END)
	STATUSVAL_STR = STATUSVAL_STR.strip()

	if STATUSVAL_STR == "":
		clear_text(output_text, output_text2)
		return

	STATUSVAL = 0
	try:
		STATUSVAL = int(STATUSVAL_STR, 0)
	except:
		try:
			STATUSVAL = int(STATUSVAL_STR, 16)
		except Exception as e:
			STATUSVAL_STR = f"[-] {e}"
			clear_text(output_text, output_text2)
			edit_text(output_text, STATUSVAL_STR)
			return

	STATUS_STR = ""
	if STATUSVAL not in STATUSVAL_STATUS:
		STATUSVAL_STR = "[-] Wrong Status value!"
	else:
		STATUSVAL_STR = "{}({})".format(hex(STATUSVAL), STATUSVAL)
		STATUS_STR = STATUSVAL_STATUS[STATUSVAL]

	edit_text(output_text, STATUSVAL_STR)
	edit_text(output_text2, STATUS_STR)
	# edit_text(output_text3, hexs_corres)


def STATUS_to_STATUSVAL():
	STATUS_STR = input_text.get("1.0", tk.END)
	STATUS = STATUS_STR.strip()

	if STATUS == "":
		clear_text(output_text, output_text2)
		return

	STATUSVAL_STR = ""
	try:
		if STATUS not in STATUS_STATUSVAL:
			STATUSVAL_STR += "[-] Wrong Status code!"
		else:
			STATUSVAL = STATUS_STATUSVAL[STATUS]
			STATUSVAL_STR = "{}({})".format(hex(STATUSVAL), STATUSVAL)
	except Exception as e:
		STATUSVAL_STR += f"[-] {e}"

	clear_text(output_text2)
	edit_text(output_text, STATUSVAL_STR)


root = tk.Tk()
root.title("WinStatus")

# 配置主窗口的列和行的伸展
root.grid_columnconfigure(0, weight=1)  # 第0列会随着窗口调整大小
root.grid_columnconfigure(1, weight=1)  # 第1列会随着窗口调整大小

root.grid_rowconfigure(1, weight=1)     # 第1行会随着窗口调整大小
root.grid_rowconfigure(3, weight=1)     # 第3行会随着窗口调整大小


# 输入标签
input_label = tk.Label(root, text="输入")
input_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

# 输入框
input_text = scrolledtext.ScrolledText(root, 
	wrap=tk.WORD, width=50, height=10)
input_text.grid(row=1, column=0, padx=(10,0), pady=0, sticky="nsew")
# 绑定鼠标右键点击事件到上下文菜单
input_text.bind("<Button-3>", lambda event, tw=input_text: show_context_menu(event, tw))

# 按钮框架和输入框同一行
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=1, column=1, padx=5, pady=5)

#按钮
STATUSVAL_to_STATUS_button = tk.Button(buttons_frame, 
	width=20, text="状态码值转换状态码", command=STATUSVAL_to_STATUS)
STATUSVAL_to_STATUS_button.grid(row=0, column=0, padx=5, pady=5)
#按钮
STATUS_to_STATUSVAL_button = tk.Button(buttons_frame, 
	width=20, text="状态码转换状态码值", command=STATUS_to_STATUSVAL)
STATUS_to_STATUSVAL_button.grid(row=0, column=1, padx=5, pady=5)


# 输出标签
output_label = tk.Label(root, text="输出")
output_label.grid(row=2, column=0, padx=5, pady=0, sticky="w")

# 创建一个新的 Frame 用于输出文本框
output_frame = tk.Frame(root)
output_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=0, sticky="nsew")
# 配置输出框架的列和行的伸展
output_frame.grid_columnconfigure(0, weight=1)  # 使输出框占满整列
output_frame.grid_rowconfigure(0, weight=1)     # 使第一个输出框占满整行
output_frame.grid_rowconfigure(1, weight=1)     # 使第二个输出框占满整行
# output_frame.grid_rowconfigure(2, weight=1)     # 使第三个输出框占满整行

# 输出框1
output_text = scrolledtext.ScrolledText(output_frame, 
	wrap=tk.WORD, width=50, height=5, state=tk.DISABLED)
output_text.grid(row=0, column=0, padx=5, pady=0, sticky="nsew")
# 绑定鼠标右键点击事件到上下文菜单
output_text.bind("<Button-3>", lambda event, tw=output_text: show_context_menu(event, tw))

# 输出框2
output_text2 = scrolledtext.ScrolledText(output_frame, 
	wrap=tk.WORD, width=50, height=5, state=tk.DISABLED)
output_text2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
# 绑定鼠标右键点击事件到上下文菜单
output_text2.bind("<Button-3>", lambda event, tw=output_text2: show_context_menu(event, tw))

# # 输出框3
# output_text3 = scrolledtext.ScrolledText(output_frame, 
#     wrap=tk.WORD, width=50, height=5, state=tk.DISABLED)
# output_text3.grid(row=2, column=0, padx=5, pady=0, sticky="nsew")
# # 绑定鼠标右键点击事件到上下文菜单
# output_text3.bind("<Button-3>", lambda event, tw=output_text3: show_context_menu(event, tw))

# 创建清空按钮
clear_button = tk.Button(root, 
	width=20, text="清空", 
	command=lambda: clear_text(input_text, output_text, output_text2))
clear_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()
