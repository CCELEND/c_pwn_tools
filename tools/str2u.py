#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 输入字符串，可以包含回车，Ctrl+D 结束输入
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

def main():
    while True:
        # 调用函数获取多行输入
        string = get_multiline_input()
        if string == 'quit':
            print("bye~")
            break

        try:
            # 将字符串中的每个字符转换为Unicode编码的十六进制表示
            unicode_hex_list = [format(ord(char), 'x') for char in string]

            hex_values_u = ""
            hex_values = ""
            # 输出每个字符的十六进制值
            for hex_value in unicode_hex_list:
                hex_values = hex_values + hex_value
                hex_values_u = hex_values_u + "\\u" + hex_value

            print(hex_values)
            print(hex_values_u)
            print()

        except Exception as e:
            print("[-] " + str(e))

if __name__ == '__main__':
    main()