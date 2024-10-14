#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 输入字符串，可以包含回车，Ctrl+D 结束输入
def get_multiline_input(prompt="Enter/Paste your utf8 hex (Ctrl+D or Ctrl+Z to end, 'quit' to exit):"):
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break

        lines.append(line)
    return '\n'.join(lines)

def main():
    while True:
        # 调用函数获取多行输入
        utf8_hexs = get_multiline_input()
        if utf8_hexs == 'quit':
            print("bye~")
            break

        try:
            if 'x' in utf8_hexs:
                utf8_hex_list = utf8_hexs.split('\\x')[1:]
                utf8_hexs = ''.join(utf8_hex_list)

            utf8_bytes = bytes.fromhex(utf8_hexs)
            print("[+] Conversion results:")
            print(utf8_bytes.decode('utf-8'))
            print()

        except Exception as e:
            print("[-] " + str(e))

if __name__ == '__main__':
    main()