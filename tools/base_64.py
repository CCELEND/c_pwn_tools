#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64
import re
from datetime import datetime

# 定义一个函数来检查多个字符是否都在字符串中
def check_characters(characters, string) -> bool:
    for char in characters:
        if char in string:
            return True
    return False

# 输入 base64 字符串，可以包含回车，Ctrl+D 结束输入
def get_multiline_input(prompt="Enter/Paste your base64 text (Ctrl+D or Ctrl+Z to end, 'quit' to exit):"):
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break

        if not check_characters(['-', '.'], line):
            lines.append(line)
    return '\n'.join(lines)

# 编码
def encode_base64(original_string: str) -> str:
    """Encode a string using Base64."""
    encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

# 解码
def decode_base64(encoded_string: str) -> str:
    """Decode a Base64 encoded string."""
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

def base64_to_image(base64_string, image_path):
    # 去除Base64字符串中的前缀（如果有）
    base64_string = re.sub(r'^data:image/.+;base64,', '', base64_string)
    # 将Base64字符串解码为二进制数据
    image_data = base64.b64decode(base64_string)
    # 将二进制数据写入到图片文件
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)

def main():
    while True:
        # 调用函数获取多行输入
        user_input = get_multiline_input()

        # 去除换行符
        encoded = user_input.replace('\n', '')
        if encoded == 'quit':
            print("bye~")
            break
        
        try:
            decoded = decode_base64(encoded)
            print("\n[*] This is a text.")
            print("[+] Decode:")
            print("=================================================")
            print(decoded)  # 显示解码的结果
            print("=================================================\n")
        except:
            try:
                # 获取当前时间
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d[%H:%M:%S]")
                
                file_name = "./" + formatted_time + "_out"
                base64_to_image(encoded, file_name)

                print("[*] This is a binary.")
                print("[+] {}: The file has been saved.\n".format(file_name))
            except Exception as e:
                print("[-] " + str(e))

if __name__ == '__main__':
    main()
