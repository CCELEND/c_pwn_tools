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
            utf8_hexs_corres = ""
            utf8_hexs = ""
            for char in string:
                # 使用UTF-8编码对字符进行编码
                utf8_encoded = char.encode('utf-8')

                # 将UTF-8编码转换为十六进制
                utf8_hex = utf8_encoded.hex()

                utf8_hexs = utf8_hexs + utf8_hex
                utf8_hexs_corres = utf8_hexs_corres + "\\x" + utf8_hex

            # 将字符串utf8_hex每两个字符前加上 '\x'
            utf8_hexs_pre = '\\x' + '\\x'.join(utf8_hexs[i:i+2] for i in range(0, len(utf8_hexs), 2))

            # 输出十六进制值
            print("[+] Byte sequence:")
            print(utf8_hexs)
            print("[+] Byte sequence(prefix):")
            print(utf8_hexs_pre)
            print("[+] Correspondence sequence:")
            print(utf8_hexs_corres)
            print()

        except Exception as e:
            print("[-] " + str(e))

if __name__ == '__main__':
    main()