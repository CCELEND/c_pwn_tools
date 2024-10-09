#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64

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

def encode_base64(input_string: str) -> str:
    """Encode a string using Base64."""
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_base64(encoded_string: str) -> str:
    """Decode a Base64 encoded string."""
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

def main():
    # encoded = encode_base64(test_string)

    while True:
        # encoded = input("input base64 str: \n")

        # 调用函数获取多行输入
        user_input = get_multiline_input()

        # 去除换行符
        encoded = user_input.replace('\n', '')

        if encoded == 'quit':
            print("bye~")
            break
        decoded = decode_base64(encoded)

        print("\n[+] Decode:")
        print(decoded)  # 显示解码的结果

        print("\n")


if __name__ == '__main__':
    main()
