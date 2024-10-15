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
            gbk_hexs_corres = ""
            gbk_hexs = ""

            for char in string:
                # 使用gbk编码对字符进行编码
                gbk_encoded = char.encode('gb2312')

                # 将gbk编码转换为十六进制
                gbk_hex = gbk_encoded.hex()

                gbk_hexs = gbk_hexs + gbk_hex
                gbk_hexs_corres = gbk_hexs_corres + "\\x" + gbk_hex

            # 将字符串gbk_hex每两个字符前加上 '\x'
            gbk_hexs_pre = '\\x' + '\\x'.join(gbk_hexs[i:i+2] for i in range(0, len(gbk_hexs), 2))

            # 输出十六进制值
            print("[+] Byte sequence:")
            print(gbk_hexs)
            print("[+] Byte sequence(prefix):")
            print(gbk_hexs_pre)
            print("[+] Correspondence sequence:")
            print(gbk_hexs_corres)
            print()

        except Exception as e:
            print("[-] " + str(e))

if __name__ == '__main__':
    main()
