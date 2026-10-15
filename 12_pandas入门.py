import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir,"douban_top250.csv")
df = pd.read_csv(csv_path)

print("=====前5行=====")
print(df["电影名"].head())  #查看前5行（默认5行)

# print("\n=====后3行=====")
# print(df.tail(3))

print("\n=====电影名+评分两列=====")
print(df[["电影名","评分"]].head())

# print(f"\n数据形状:{df.shape}")
# print(f"行数:{df.shape[0]},列数:{df.shape[1]}")

# print("\n=====统计描述=====")
# print(df.describe)

print("\n=====第0行（第一部电影）=====")
print(df.iloc[0])

print("\n=====第0到第2行（前三部）=====")
print(df.iloc[0:3])   #左闭右开
#pd.to_numeric转换为数值，coerce表示转换不料的变成NaN
df["评分数值"] = pd.to_numeric(df["评分"],errors="coerce")

print("\n=====评分大于9.5的电影=====")
high_rated = df[df["评分数值"]>9.5]
print(high_rated[["排名","电影名","评分数值"]])

print("\n===== 评分>9.4 且 国家包含美国 =====")
us_high = df[(df["评分数值"]>9.4) & (df["年份/国家/类型"].str.contains("美国",na=False))]
print(us_high[["电影名","评分数值","年份/国家/类型"]])

print("\n===== 犯罪类型电影 =====")
crime = df[df["年份/国家/类型"].str.contains("犯罪",na=False)]
print(f"共{len(crime)}部犯罪类型电影")
print(crime[["电影名","评分数值"]].head(10))

print("\n=====按评分降序（前10）=====")
sorted_df = df.sort_values("评分数值",ascending=False)
print(sorted_df[["电影名","评分数值"]].head(10))

print("\n===== 评分最低的10部 =====")
lowest = df.sort_values("评分数值",ascending=True)  #ascending控制排序是升序还是降序，默认升序
print(lowest[["电影名","评分数值"]].head(10))

#正则从“评价人数”提取数字
df["评价人数数值"] = df["评价人数"].str.extract(r"(\d+)").astype(float)
print("\n===== 评价人数最多的10部 =====")
most_review = df.sort_values("评价人数数值",ascending=False)
print(most_review[["电影名","评分数值","评价人数数值"]].head(10))

#从”年份/国家/类型“提取上映年份
df["上映年份"] = df["年份/国家/类型"].str.extract(r"(\d{4})").astype(float)
print("\n===== 2000年以后上映的电影 =====")
after_2000 = df[df["上映年份"] >= 2000]
print(f"共{len(after_2000)}部")
print(after_2000[["电影名","上映年份","评分数值"]].head(10))

#缺失值处理
print("\n===== 每列空值数量 =====")
print(df.isnull().sum())

#删除有空值的行
df_dropna = df.dropna()
print(f"\n删除空值后:{len(df_dropna)}行(原{len(df)}行)")

# ========== 分组统计 groupby ==========
# 先新增一列：年代（1990s, 2000s, 2010s...）
# 上映年份除以10取整再乘10，得到年代的整数，再转成字符串加s
df["年代"] = (pd.to_numeric(df["上映年份"],errors="coerce")//10*10).astype("Int64").astype(str)+"s"   #Int64是可空整数类型

print("\n===== 按年代分组统计 =====")
grouped = df.groupby("年代").agg(
    电影数量=("电影名","count"),
    平均评分=("评分数值","mean"),
    最高评分=("评分数值","max"),
    平均评价人数=("评价人数数值","mean")
).round(2)
print(grouped)

print("\n===== 电影类型出现此书(前15) =====")
df["类型"] = df["年份/国家/类型"].str.split("/").str[-1].str.strip()

all_type = []
for types in df["类型"].dropna():
    for t in types.split():
        all_type.append(t)

type_counts = pd.Series(all_type).value_counts()
print(type_counts.head(15))

#整理最终结果：只保留需要的列
result = df[["排名","电影名","评分数值","评价人数数值","上映年份","导演/主演","一句话简介"]]

# 2. 写入单个 sheet 的 Excel
# index=False 表示不把行索引写入文件
result.to_excel("douban_top250_分析结果.xlsx",index=False,sheet_name="电影数据")
print("\n 以保存到 douban_top250_分析结果.xlsx")

# 3. 写入多个 sheet（一个 Excel 文件里多个工作表）
with pd.ExcelWriter("douban_完整分析.xlsx") as writer:
    result.to_excel(writer,sheet_name="全部电影",index=False)#全部电影数据
    top20 = result.sort_values("评分数值",ascending=False).head(20)
    top20.to_excel(writer,sheet_name="评分Top20",index=False)#评分最高的20部

    #按年代分组
    grouped.to_excel(writer,sheet_name="年代统计")

print("以保存到douban_完整分析.xlsx(含3个sheet)")