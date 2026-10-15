import pandas as pd
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr")

print("="*50)
print(" AI数据分析助手")
print(" 读取CSV/Excel -> 自动统计 -> AI生成分析报告")
print("="*50)

file_path = input("\n请输入数据文件路径:").strip()

try:
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith("xlsx","xls"):
        df = pd.read_excel(file_path)
    else:
        print("仅支持CSV或Excel文件")
        exit()

except Exception as e:
    print(f"读取文件失败:{e}")
    exit()

print(f"\n读取成功,共{len(df)},{len(df.columns)}列")
print(f"列名:{list(df.columns)}")

print("\n正在做数据统计")

#数值列统计
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
status_summary = ""
if numeric_cols:
    stats = df[numeric_cols].describe().round(2)
    status_summary = f"[数值列统计]\n{stats.to_string()}"
    print(status_summary)

#缺失值统计
missing = df.isnull().sum()
missing = missing[missing > 0]
if not missing.empty:
    missing_summary = f"\n\n[缺失值统计]\n{missing.to_string()}"
    print(missing_summary)
else:
    missing_summary = "\n\n[缺失值统计]无缺失值"

print("\n列名统计")
for i,col in enumerate(df.columns):
    print(f"    {i}. {col}")

group_col = input("\n选一列做分组统计(输入列名，可留空跳过)：").strip()
group_summary = ""
if group_col and group_col in df.columns:
    if numeric_cols:
        agg_col = numeric_cols[0]
        grouped = df.groupby(group_col)[agg_col].agg(["count","mean"]),round(2)
        grouped.colums = [f"{agg_col}_数量",f"{agg_col}_均值"]
        group_summary = f"\n\n[按{group_col}分组统计({agg_col})]\n{grouped.to_string()}"
        print(group_summary)
    else:
        vc = df[group_col].value_counts.head(10)
        group_summary = f"\n\n[按{group_col}分组频次统计(前10)]\n{vc.to_string()}"
        print(group_summary)

#统计结果发给AI让AI生成分析报告
print("\nAI 正在生成分析报告...")

data_overview = f"""

数据概览:
- 数据行数:{len(df)}
- 数据列数:{len(df.columns)}
- 列名:{list(df.columns)}
- 数列名:{numeric_cols}

{status_summary}
{missing_summary}
{group_summary}
"""

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {"role":"system","content":"你是一个专业的数据分析师，用户会给你一份数据的统计结果，你写一段通俗易懂的数据分析报告，包括：1.数据整体情况 2.关键发现 3.趋势/规律 4.建议。分点说明，语言简洁，不要太技术化。"},
        {"role":"user","content":f"请根据以下统计结果写数据分析报告：\n{data_overview}"}
    ]
)

report = response.choices[0].message.content

print("\n" + "=" * 55)
print("  AI 数据分析报告")
print("=" * 55)
print(report)
print("=" * 55)

#保存文件
output_file = "AI数据分析报告.txt"
with open(output_file,"w",encoding="utf-8")as f:
    f.write("="*55+"\n")
    f.write("   AI数据分析报告\n")
    f.write("="*55+"\n\n")
    f.write(f"数据文件:{file_path}\n")
    f.write(f"生成时间:{pd.Timestamp.now()}")
    f.write("[原始统计数据]\n")
    f.write(data_overview)
    f.write("\n\n")
    f.write("[AI分析报告]\n")
    f.write(report)

print(f"\n 报告已保存到{output_file}")