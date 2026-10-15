import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# 产品和类别
products = {
    "手机": ["iPhone 15", "小米14", "华为Mate60", "OPPO Find X7", "vivo X100"],
    "电脑": ["MacBook Pro", "ThinkPad X1", "戴尔XPS", "华为MateBook", "联想小新"],
    "耳机": ["AirPods Pro", "索尼WH-1000XM5", "小米Buds", "华为FreeBuds", "Bose QC45"],
    "平板": ["iPad Pro", "华为MatePad", "小米平板6", "三星Tab S9", "联想小新Pad"],
    "配件": ["手机壳", "充电器", "数据线", "鼠标", "键盘"]
}

regions = ["华东", "华南", "华北", "华中", "西南", "西北", "东北"]
salespeople = ["张三", "李四", "王五", "赵六", "钱七", "孙八"]

rows = []
start_date = datetime(2024, 1, 1)

for i in range(100):
    category = random.choice(list(products.keys()))
    product = random.choice(products[category])
    region = random.choice(regions)
    salesperson = random.choice(salespeople)
    date = start_date + timedelta(days=random.randint(0, 364))
    quantity = random.randint(1, 20)
    unit_price = round(random.uniform(50, 15000), 2)
    sales = round(quantity * unit_price, 2)
    profit = round(sales * random.uniform(0.1, 0.4), 2)
    
    rows.append({
        "订单号": f"ORD{1000+i}",
        "日期": date.strftime("%Y-%m-%d"),
        "产品": product,
        "类别": category,
        "地区": region,
        "销售员": salesperson,
        "数量": quantity,
        "单价": unit_price,
        "销售额": sales,
        "利润": profit
    })

df = pd.DataFrame(rows)

# 故意加入脏数据
# 1. 重复5行
df = pd.concat([df, df.sample(5)], ignore_index=True)

# 2. 缺失值：10个订单的销售员为空，5个利润为空
df.loc[df.sample(10).index, "销售员"] = np.nan
df.loc[df.sample(5).index, "利润"] = np.nan

# 3. 异常值：3个销售额特别大
df.loc[df.sample(3).index, "销售额"] = 999999

# 4. 日期格式不统一：5个日期用斜杠格式
slash_dates = df.sample(5).index
for idx in slash_dates:
    d = datetime.strptime(df.loc[idx, "日期"], "%Y-%m-%d")
    df.loc[idx, "日期"] = d.strftime("%Y/%m/%d")

df.to_excel("电商销售数据.xlsx", index=False, engine="openpyxl")
print(f"✅ 已生成电商销售数据.xlsx，共 {len(df)} 行")
print(f"   包含：重复行、缺失值、异常值、日期格式不统一")
