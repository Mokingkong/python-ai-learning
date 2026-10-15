import pandas as pd
import os

#Q1:评分最高的 5 部电影是哪些？（排序 + head）
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir,"douban_top250.csv")
df = pd.read_csv(csv_path)

df["评分数值"] = pd.to_numeric(df["评分"],errors="coerce")
high_5 = df.sort_values("评分数值",ascending=False)
print(high_5[["电影名","评分数值"]].head(5))

#Q2:评价人数最多的 5 部电影 (排序 + head)
df["评价人数数值"] = df["评价人数"].str.extract(r"(\d+)").astype(float)
most_review5 = df.sort_values("评价人数数值",ascending=False)
print(most_review5[["电影名","评价人数数值"]].head(5))

#Q3:1994 年上映的电影有几部？平均评分多少？（筛选 + 统计）
df["上映年份"] = df["年份/国家/类型"].str.extract(r"(\d{4})").astype("Int64")
Load_1994 = df[df["上映年份"]==1994]
average_1994 = Load_1994["评分数值"].mean()
print(f"1994年上映的电影有:{len(Load_1994)}部")
print(f"他们的平均评分是:{average_1994:.2f}")

#Q4:哪个年代的电影数量最多？（groupby + 排序）
# print("当前所有列:",df.columns.tolist())

df["年代"] = (pd.to_numeric(df["上映年份"],errors="coerce")//10*10).astype("Int64").astype(str)+"s"
grouped = df.groupby("年代").agg(     #不是哥么,这分类这么简单的吗
    电影数量 = ("电影名","count"),
    平均评分 = ("评分数值","mean"),
    平均评价人数 = ("评价人数数值","mean")
).round(2)
most_movieyear = grouped.sort_values("电影数量",ascending=False)
print(f"\n电影数量最多的年代是{most_movieyear.index[0]},共{most_movieyear["电影数量"].iloc[0]}部")

#参考结构
# year_count = df.groupby("年代")["电影名"].count()
# print(year_count.sort_values(ascending=False))
# print(f"电影数量最多的年代是: {year_count.idxmax()}，共{year_count.max()}部")

#Q5:"剧情" 类型的电影有多少部？平均评分多少？（字符串包含筛选 + 统计）
df["类型"] = df["年份/国家/类型"].str.split("/").str[-1].str.strip()
drama = df[df["类型"].str.contains("剧情",na=False)]
drama_count = len(drama)
average_drama = drama["评分数值"].mean()
print(f"剧情类型电影有{drama_count}部")
print(f"平均评分:{average_drama:.2f}")

#Q6:把分析结果写入一个 Excel 文件，包含 "全部数据" 和 "统计汇总" 两个 sheet

result = df[["排名","电影名","评分数值","评价人数数值","上映年份","导演/主演","一句话简介"]]

figure_out = grouped

with pd.ExcelWriter("pandas实战训练结果.xlsx") as writer:
    result.to_excel(writer,sheet_name="全部数据",index=False)
    figure_out.to_excel(writer,sheet_name="统计汇总")

print("已完成Q6")