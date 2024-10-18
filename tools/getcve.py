import requests
from bs4 import BeautifulSoup

result_2024 = ""
result_2023 = ""
for i in range(1, 40):
    print(f"[+] {i} page.")

    # 发送请求到目标网站
    url = f'https://avd.aliyun.com/search?q=windows&page={i}'  # 替换为实际的网站URL
    response = requests.get(url)
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析网页内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到包含漏洞信息的表格
        table = soup.find('table', class_='table')

        # 遍历表格的每一行，提取信息
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 5:
                avd_id = columns[0].text.strip()
                description = columns[1].text.strip()
                date = columns[3].text.strip()
                
                # (description in ["提升", "执行", "win32"])
                if ("提升" in description or "执行" in description or "win32" in description) and "2024" in date:
                    # 打印提取的结果
                    avd_id = avd_id.replace("AVD", "CVE")
                    result_2024 += f'{avd_id} "{description}" {date}\n'

                if ("提升" in description or "执行" in description or "win32" in description)  and "2023" in date:
                    # 打印提取的结果
                    avd_id = avd_id.replace("AVD", "CVE")
                    result_2023 += f'{avd_id} "{description}" {date}\n'

    else:
        print(f'无法访问页面 {i}')

# print(f"[+] CVE-2024:")
# print(result_2024)
# print(f"[+] CVE-2023:")
# print(result_2023)

with open("CVE-2024.txt", 'w', encoding='utf-8') as file_2024:
    file_2024.write(result_2024)

with open("CVE-2023.txt", 'w', encoding='utf-8') as file_2023:
    file_2023.write(result_2023)