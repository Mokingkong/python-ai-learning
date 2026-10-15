from bs4 import BeautifulSoup

html="""
<!DOCTYPE html>
<html>
<head>
    <title>我的网页</title>
</head>
<body>
    <h1>欢迎来到我的网站</h1>
    <p class="intro">这是一个测试网页</p>
    <div id="content">
        <p>第一段：学习Python爬虫</p>
        <p>第二段：BeautifulSoup很强大</p>
        <a href="https://www.python.org">Python官网</a>
    </div>
    <ul>
        <li class="item">苹果</li>
        <li class="item">香蕉</li>
        <li class="item">橙子</li>
    </ul>
</body>
</html>
"""

# 1. 解析HTML
soup = BeautifulSoup(html,'html.parser')


# 2. find()：找到第一个匹配的标签
title = soup.find('title')
print(f"标题标签:{title}")
print(f"标题文本:{title.text}")

h1 = soup.find('h1')
print(f"h1文本:{h1.text}")


# 3. find_all()：找到所有匹配的标签，返回列表
all_p = soup.find_all('p')
print(f"\n所有p标签数量:{len(all_p)}")
for p in all_p:
    print(f" - {p.text}")


# 4. 按class查找：class_=（注意带下划线，因为class是Python关键字）
intro = soup.find('p',class_='intro')
print(f"\nclass为intro的p:{intro.text}")

items = soup.find_all('li',class_='item')
print(f"\n所有class为item的li:")
for item in items:
    print(f" - {item.text}")

# 5. 按id查找：id=
content = soup.find('div',id='content')
print(f"\nid为content的div里的内容:")
print(content.text.strip())

# 6. 获取属性：.get('属性名')
link = soup.find('a')
print(f"\n链接文本:{link.text}")
print(f"链接地址:{link.get('href')}")

# 7. 嵌套查找：先找父标签，再在父标签里找子标签
content_div = soup.find('div',id='content')
links_in_div = content_div.find_all('a')
print(f"\ndiv里的链接数量:{len(links_in_div)}")

# 8. CSS选择器：select()（更灵活，和前端CSS选择器语法一样）
# 用标签名找
print(f"\nselect找所有Li")
for li in soup.select('li'):
    print(f" - {li.text}")

# 用.class找（点号表示class）
print(f"\nselect找clss=item:")
for item in soup.select('.item'):
    print(f" - {item.text}")

# 用#id找（#号表示id）
content2 = soup.select_one('#content')
print(f"\nselect找id=content:{content2.text.strip()[:20]}...")

# 组合选择器：div#content p 表示找id为content的div里面的所有p
ps_in_div = soup.select('div#content p')
print(f"\ndiv里的p标签:")
for p in ps_in_div:
    print(f" - {p.text}")