import requests
from bs4 import BeautifulSoup
import csv

url = "https://movie.douban.com/top250"

# 重要：加请求头，模拟浏览器访问，否则豆瓣会拒绝（403 Forbidden）
headers = {
    "User-Agent":"Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. 用requests下载网页
response = requests.get(url,headers=headers)
print(f"状态码:{response.status_code}")

# 2. 用BeautifulSoup解析

soup = BeautifulSoup(response.text,'html.parser')

# 3. 分析网页结构，找到电影列表

movies = soup.find_all('div',class_='item')
print(f"找到{len(movies)}部电影")

# ========== 新增：打开CSV文件 ==========
csv_file = open("/home/dev.practice/douban_top250.csv","w",newline="",encoding="utf-8=sig")
writer = csv.writer(csv_file)

# 写入表头（第一行，列名）
writer.writerow(["排名","电影名","评分","评价人数","导演/主演","年份/国家/类型","一句话简介"])



# 4. 遍历每部电影，提取信息
print("\n===== 豆瓣电影Top250（第1页）=====")
for i,movie in enumerate(movies,1):
    rank_tag = movie.find('em')
    rank = rank_tag.text if rank_tag else "未知"

    title_tag = movie.find('span',class_='title')
    title = title_tag.text if title_tag else "未知"

    bd_div = movie.find('div',class_='bd')

    rating = "未知"
    people = "未知"
    if bd_div:
        rating_tag = bd_div.find('span',class_ = 'rating_num')
        if rating_tag:
            rating = rating_tag.text

        for span in bd_div.find_all('span'):
            if "人评价" in span.text:
                people = span.text
                break

    info = "未知"
    if bd_div:
        p_tag = bd_div.find('p')
        if p_tag:
            full_text = p_tag.get_text("\n",strip=True)
            lines = full_text.split("\n")
            if len(lines) >= 1:
                info = lines[0].strip()
            if len(lines) >=2:
                year_info = lines[1].strip()

    inq_tag = movie.find('span',class_='inq')
    inq = inq_tag.text if inq_tag else "无简介"

    print(f"\n{rank}. 《{title}》")
    print(f"   评分: {rating}  评价人数: {people}")
    print(f"   信息: {info}")
    print(f"   年份/国家/类型: {year_info}")
    print(f"   简介: {inq}")

    # ========== 新增：写入CSV文件 ==========
    writer.writerow([rank,title,rating,people,info,year_info,inq])


csv_file.close()

print(f"\n 数据已保存到  douban_top250.csv")

# 打印第一部电影的完整HTML，看看结构
# if movies:
#     print("\n===== 第一部电影的HTML =====")
#     print(movies[0].prettify)