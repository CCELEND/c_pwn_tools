#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 输入字符串，可以包含回车，Ctrl+D 结束输入
def get_multiline_input(prompt="Enter/Paste your unicode (Ctrl+D or Ctrl+Z to end, 'quit' to exit):"):
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
        unicode_str = get_multiline_input()
        if unicode_str == 'quit':
            print("bye~")
            break

        try:
            unicode_list = unicode_str.split('\\u')[1:]
            decoded_string = ''.join([chr(int(value, 16)) for value in unicode_list])

            print("[+] Conversion results:")
            print(decoded_string)
            print()

        except Exception as e:
            print("[-] " + str(e))

if __name__ == '__main__':
    main()