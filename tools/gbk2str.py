#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 输入字符串，可以包含回车，Ctrl+D 结束输入
def get_multiline_input(prompt="Enter/Paste your gbk hex (Ctrl+D or Ctrl+Z to end, 'quit' to exit):"):
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
        gbk_hexs = get_multiline_input()
        if gbk_hexs == 'quit':
            print("bye~")
            break

        try:
            if 'x' in gbk_hexs:
                gbk_hex_list = gbk_hexs.split('\\x')[1:]
                gbk_hexs = ''.join(gbk_hex_list)

            gbk_bytes = bytes.fromhex(gbk_hexs)
            print("[+] Conversion results:")
            print(gbk_bytes.decode('gb2312'))
            print()

        except Exception as e:
            print("[-] " + str(e))

if __name__ == '__main__':
    main()