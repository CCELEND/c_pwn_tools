#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64
import re

# 输入 base64 字符串，可以包含回车，Ctrl+D 结束输入
def get_multiline_input(prompt="Enter/Paste your text (Ctrl+D or Ctrl+Z to end, 'quit' to exit):"):
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
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
            print("[*] This is a binary.")
            file_name = "./out"
            base64_to_image(encoded, file_name)
            print("[+] {}: The file has been saved.\n".format(file_name))

if __name__ == '__main__':
    main()
