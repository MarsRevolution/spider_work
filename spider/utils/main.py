import urllib.request
import re
import csv
import os


def extract_data_from_url(url, title):
    # 下载HTML内容
    response = urllib.request.urlopen(url)
    html_content = response.read().decode('utf-8')

    # 使用正则表达式解析HTML内容
    pattern = r'<a href=".*?">.*?<img src="(/__local/.*?\.jpg).*?alt="">.*?<div class="name-group">.*?<span class="name">(.*?)</span>.*?<span class="iden">(.*?)</span>'
    teachers = re.findall(pattern, html_content, re.S)

    # 保存头像到本地，并将教师信息保存
    information = []
    base_url = "https://sdmda.bupt.edu.cn"
    for teacher in teachers:
        img_url = base_url + teacher[0]
        name = teacher[1]
        # 使用教师的名字命名图片文件
        img_name = name + ".jpg"
        # 在“教师头像”文件夹中保存图片
        root="spider\\utils\\教师头像"
        save_path = os.path.join("教师头像", img_name)
        urllib.request.urlretrieve(img_url, save_path)

        dept = teacher[2]
        photo_path = os.path.join(root, img_name)
        information.append([dept, name, title, photo_path])

    return information


# 在开始爬取前，确保“教师头像”文件夹存在，不存在则创建一个
def ensure_directory_exists(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

ensure_directory_exists("教师头像")


# 从每个URL中抓取数据
all_teachers = []
urls_titles = [
    ("https://sdmda.bupt.edu.cn/szdw/js.htm", "教授"),
    ("https://sdmda.bupt.edu.cn/szdw/fjs.htm", "副教授"),
    ("https://sdmda.bupt.edu.cn/szdw/js1.htm", "讲师")
]

for url, title in urls_titles:
    all_teachers.extend(extract_data_from_url(url, title))

# 保存所有教师信息到CSV文件
with open('teachers.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Department", "Name", "Title", "Photo"])
    writer.writerows(all_teachers)

print("爬取完成")
