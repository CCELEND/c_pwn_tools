#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64
import re
import tkinter as tk
from tkinter import scrolledtext, Menu, messagebox, filedialog

# from datetime import datetime

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

# 定义一个函数来检查多个字符是否都在字符串中
def check_characters(characters, string) -> bool:
    for char in characters:
        if char in string:
            return True
    return False

def get_file_type(file_data):

    signatures = {
        b'\xFF\xD8\xFF\xDB': '.jpeg',
        b'\xFF\xD8\xFF\xE0': '.jpeg',
        b'\x89PNG\r\n\x1A\n': '.png',
        b'GIF87a': '.gif',
        b'GIF89a': '.gif',
        b'%PDF-': '.pdf',
        b'\x50\x4B\x03\x04': '.zip',
        # Add more signatures as needed
    }

    # 根据已知签名检查 file_data 的开头
    for signature, file_extension in signatures.items():
        if file_data.startswith(signature):
            return file_extension

    return ""

def save_file():
    encoded_string = input_text.get("1.0", tk.END)
    encoded_string = '\n'.join(encoded_string)

    result = ""
    try:
        file_data = base64.b64decode(encoded_string)
        file_extension = get_file_type(file_data)

        # 打开文件保存对话框，返回文件路径
        file_path = filedialog.asksaveasfilename(
            defaultextension = file_extension,  # 文件扩展名
            filetypes = [("All files", "*.*"),
                            ("Binary File", "*.bin"), 
                            ("Text files", "*.txt")],  # 文件类型过滤器
            title = "保存文件"
        )
        if file_path:  # 如果没有取消
            # 保存文件
            with open(file_path, 'wb') as file:
                file.write(file_data)  # 保存文件

    except Exception as e:
        result += f"[-] {e}"

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state=tk.DISABLED)

# base64 编码
def encode_base64(code):
    original_string = input_text.get("1.0", tk.END)
    encoded_bytes = base64.b64encode(original_string.encode(code))

    # utf-8 编码格式输出到输出框
    encoded_string = encoded_bytes.decode('utf-8')
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encoded_string)
    output_text.config(state=tk.DISABLED)

# 解码
def decode_base64():
    encoded_string = input_text.get("1.0", tk.END)
    encoded_string = '\n'.join(encoded_string)

    decoded_bytes = b""
    result = ""
    try:
        # 解码 Base64 编码的字符串
        decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
        # 尝试使用 UTF-8 解码
        result = decoded_bytes.decode('utf-8')
    except:
        try:
            decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
            # 如果 UTF-8 失败，尝试使用 GB2312 解码
            result = decoded_bytes.decode('gb2312')
        except:
            result = "[*] Unknown encoding or binary file, Please save it."

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("base64 解码")

# 配置主窗口的列和行的伸展
root.grid_columnconfigure(0, weight=1)  # 第0列会随着窗口调整大小
root.grid_columnconfigure(1, weight=1)  # 第1列会随着窗口调整大小

root.grid_rowconfigure(1, weight=1)     # 第1行会随着窗口调整大小
root.grid_rowconfigure(3, weight=1)     # 第3行会随着窗口调整大小

# 输入标签
input_label = tk.Label(root, text="输入")
input_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

# 输入操作框架
input_operate_frame = tk.Frame(root)
input_operate_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")
input_operate_frame.grid_columnconfigure(0, weight=1)  # 输入框占满整列
input_operate_frame.grid_columnconfigure(1, weight=1)  # 按钮框架占满整列
input_operate_frame.grid_rowconfigure(0, weight=1)     # 行0权重为1，可伸展

# 输入框
input_text = scrolledtext.ScrolledText(input_operate_frame, 
    wrap=tk.WORD, width=50, height=10)
input_text.grid(row=0, column=0, padx=(10,0), pady=0, sticky="nsew")
# 绑定鼠标右键点击事件到上下文菜单
input_text.bind("<Button-3>", lambda event, tw=input_text: show_context_menu(event, tw))

# 按钮框架和输入框同一行
buttons_frame = tk.Frame(input_operate_frame)
buttons_frame.grid(row=0, column=1, padx=5, pady=5)

# 编码按钮
encode_base64_utf8_button = tk.Button(buttons_frame, 
    width=20, text="base64 编码(utf-8)", command=lambda: encode_base64("utf-8"))
encode_base64_utf8_button.grid(row=0, column=0, padx=5, pady=5)

# 编码按钮
encode_base64_gbk_button = tk.Button(buttons_frame, 
    width=20, text="base64 编码(gbk)", command=lambda: encode_base64("gb2312"))
encode_base64_gbk_button.grid(row=1, column=0, padx=5, pady=5)

# 解码按钮
base64_decode_button = tk.Button(buttons_frame, 
    width=20, text="base64 解码", command=decode_base64)
base64_decode_button.grid(row=2, column=0, padx=5, pady=5)


# 输出标签
output_label = tk.Label(root, text="输出")
output_label.grid(row=2, column=0, padx=5, pady=0, sticky="w")

# 创建一个新的 Frame 用于输出文本框
output_frame = tk.Frame(root)
output_frame.grid(row=3, column=0, columnspan=2, padx=0, pady=5, sticky="nsew")
output_frame.grid_columnconfigure(0, weight=1)  # 输入框占满整列
output_frame.grid_columnconfigure(1, weight=1)  # 按钮占满整列
output_frame.grid_rowconfigure(0, weight=1)     # 行0权重为1，可伸展


# 输出框
output_text = scrolledtext.ScrolledText(output_frame, 
    wrap=tk.WORD, width=50, height=5, state=tk.DISABLED)
output_text.grid(row=0, column=0, padx=(10,0), pady=0, sticky="nsew")
# 绑定鼠标右键点击事件到上下文菜单
output_text.bind("<Button-3>", lambda event, tw=output_text: show_context_menu(event, tw))

#按钮
save_button = tk.Button(output_frame, 
    width=20, text="保存结果", command=save_file)
save_button.grid(row=0, column=1, padx=5, pady=5)

# 创建清空按钮
clear_button = tk.Button(root, 
    width=20, text="清空", 
    command=lambda: clear_text(input_text, output_text))
clear_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()