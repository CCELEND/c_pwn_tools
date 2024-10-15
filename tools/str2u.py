#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 输入字符串，可以包含回车，Ctrl+D 或者 Ctrl+Z 结束输入
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

            unicode_hexs_corres = ""
            unicode_hexs = ""

            for hex_value in unicode_hex_list:
                unicode_hexs = unicode_hexs + hex_value
                unicode_hexs_corres = unicode_hexs_corres + "\\u" + hex_value

            # 将字符串unicode_hex每两个字符前加上 '\u'
            unicode_hexs_pre = '\\u' + '\\u'.join(unicode_hexs[i:i+2] for i in range(0, len(unicode_hexs), 2))

            # 输出十六进制值
            print("[+] Byte sequence:")
            print(unicode_hexs)
            print("[+] Byte sequence(prefix):")
            print(unicode_hexs_pre)
            print("[+] Correspondence sequence:")
            print(unicode_hexs_corres)
            print()

        except Exception as e:
            print("[-] " + str(e))

if __name__ == '__main__':
    main()
