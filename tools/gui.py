#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import scrolledtext, Menu, messagebox

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

def str2hex(code):
    string = input_text.get("1.0", tk.END)

    hexs = ""
    hexs_pre = ""
    hexs_corres = ""
    try:
        for char in string:
            encoded = char.encode(code)
            hex_str = encoded.hex()
            hexs += hex_str
            hexs_corres += f"\\x{hex_str}"

        # 将字符串hex每两个字符前加上 '\x'
        hexs_pre = '\\x' + '\\x'.join(hexs[i:i+2] for i in range(0, len(hexs), 2))

    except Exception as e:
        hexs += f"[-] {e}"

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, hexs)
    output_text.config(state=tk.DISABLED)

    output_text2.config(state=tk.NORMAL)
    output_text2.delete("1.0", tk.END)
    output_text2.insert(tk.END, hexs_pre)
    output_text2.config(state=tk.DISABLED)

    output_text3.config(state=tk.NORMAL)
    output_text3.delete("1.0", tk.END)
    output_text3.insert(tk.END, hexs_corres)
    output_text3.config(state=tk.DISABLED)

def hex2str(code):
    hexs = input_text.get("1.0", tk.END)

    string = ""
    try:
        if 'x' in hexs:
            hex_list = hexs.split('\\x')[1:]
            hexs = ''.join(hex_list)

        hex_bytes = bytes.fromhex(hexs)
        string = hex_bytes.decode(code)

    except Exception as e:
        string += f"[-] {e}"

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, string)
    output_text.config(state=tk.DISABLED)

def str2unicode():
    string = input_text.get("1.0", tk.END)

    unicode_hexs = ""
    unicode_hexs_pre = ""
    unicode_hexs_corres = ""
    try:
        # 将字符串中的每个字符转换为Unicode编码的十六进制表示
        unicode_hex_list = [format(ord(char), 'x') for char in string]
        for hex_value in unicode_hex_list:
            unicode_hexs = unicode_hexs + hex_value
            unicode_hexs_corres = unicode_hexs_corres + "\\u" + hex_value

        # 将字符串unicode_hex每两个字符前加上 '\u'
        unicode_hexs_pre = '\\u' + '\\u'.join(unicode_hexs[i:i+2] for i in range(0, len(unicode_hexs), 2))

    except Exception as e:
        unicode_hexs += f"[-] {e}"

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, unicode_hexs)
    output_text.config(state=tk.DISABLED)

    output_text2.config(state=tk.NORMAL)
    output_text2.delete("1.0", tk.END)
    output_text2.insert(tk.END, unicode_hexs_pre)
    output_text2.config(state=tk.DISABLED)

    output_text3.config(state=tk.NORMAL)
    output_text3.delete("1.0", tk.END)
    output_text3.insert(tk.END, unicode_hexs_corres)
    output_text3.config(state=tk.DISABLED)

def unicode2str():
    unicode_str = input_text.get("1.0", tk.END)

    decoded_string = ""
    try:
        unicode_list = unicode_str.split('\\u')[1:]
        decoded_string = ''.join([chr(int(value, 16)) for value in unicode_list])

    except Exception as e:
        decoded_string += f"[-] {e}"

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, decoded_string)
    output_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("编码转换")

# 输入
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
input_text.pack(side=tk.LEFT, padx=10, pady=10)
# 绑定鼠标右键点击事件到上下文菜单
input_text.bind("<Button-3>", lambda event, tw=input_text: show_context_menu(event, tw))

buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.LEFT, padx=5, pady=5)

#按钮
to_gbk_hex_button = tk.Button(buttons_frame, text="字符串转换 GBK Hex", command=lambda: str2hex("gb2312"))
to_gbk_hex_button.grid(row=0, column=0, padx=5, pady=5)
#按钮
gbk_hex_to_str_button = tk.Button(buttons_frame, text="GBK Hex 转换字符串", command=lambda: hex2str("gb2312"))
gbk_hex_to_str_button.grid(row=0, column=1, padx=5, pady=5)

# 创建一个新的Frame用于输出文本框
output_frame = tk.Frame(root)
output_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 输出
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=50, height=5, state=tk.DISABLED)
output_text.pack(side=tk.TOP, padx=10, pady=10)
# 绑定鼠标右键点击事件到上下文菜单
output_text.bind("<Button-3>", lambda event, tw=output_text: show_context_menu(event, tw))

# # 输出
# output_text2 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=5, state=tk.DISABLED)
# output_text2.pack(padx=10, pady=10)
# # 绑定鼠标右键点击事件到上下文菜单
# output_text2.bind("<Button-3>", lambda event, tw=output_text2: show_context_menu(event, tw))

# # 输出
# output_text3 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=5, state=tk.DISABLED)
# output_text3.pack(padx=10, pady=10)
# # 绑定鼠标右键点击事件到上下文菜单
# output_text3.bind("<Button-3>", lambda event, tw=output_text3: show_context_menu(event, tw))

# # 创建清空按钮
# clear_button = tk.Button(root, width=20, text="清空", command=lambda: clear_text(input_text, output_text, output_text2, output_text3))
# clear_button.pack(padx=30, pady=10)

# #按钮
# to_gbk_hex_button = tk.Button(root, text="字符串转换 GBK Hex", command=lambda: str2hex("gb2312"))
# to_gbk_hex_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# #按钮
# gbk_hex_to_str_button = tk.Button(root, text="GBK Hex 转换字符串", command=lambda: hex2str("gb2312"))
# gbk_hex_to_str_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)


# #按钮
# to_utf8_hex_button = tk.Button(root, text="字符串转换 utf-8 Hex", command=lambda: str2hex("utf-8"))
# to_utf8_hex_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# #按钮
# utf8_hex_to_str_button = tk.Button(root, text="utf-8 Hex 转换字符串", command=lambda: hex2str("utf-8"))
# utf8_hex_to_str_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# #按钮
# to_unicode_hex_button = tk.Button(root, text="字符串转换 unicode Hex", command=str2unicode)
# to_unicode_hex_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# #按钮
# unicode_hex_to_str_button = tk.Button(root, text="unicode Hex 转换字符串", command=unicode2str)
# unicode_hex_to_str_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)




root.mainloop()