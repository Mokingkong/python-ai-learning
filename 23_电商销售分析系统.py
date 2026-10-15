import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from zhipuai import ZhipuAI

matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

client = ZhipuAI(api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr")

print("=" * 60)
print("  电商销售数据分析系统")
print("  数据清洗 → 多维度统计 → 可视化 → AI分析 → HTML报告")
print("=" * 60)

data_file = input("\n请输入数据文件路径(默认：电商销售数据.xlsx):").strip() or "电商销售数据.xlsx"

if not os.path.exists(data_file):
    exit()

df = pd.read_excel(data_file,engine="openpyxl")
print(f"\n读取原始数据:{len(df)}行,{len(df.columns)}列")

output_dir = "电商分析报告"
os.makedirs(output_dir,exist_ok=True)
os.makedirs(os.path.join(output_dir,"images"),exist_ok=True)

print("\n----数据清洗----")
raw_rows = len(df)

df = df.drop_duplicates()
dup_count = raw_rows - len(df)
print(f"删除重复行:{dup_count}行")

df["日期"] = pd.to_datetime(df["日期"],format="mixed")
df["月份"] = df["日期"].dt.to_period("M").astype(str)
print("日期格式已统一")

missing_before = df.isnull().sum().sum()
df["销售员"] = df["销售员"].fillna("未知")
df["利润"] = df["利润"].fillna(df["销售额"]*0.25)
missing_after = df.isnull().sum().sum()
print(f"缺失值处理:{missing_before} -> {missing_after}")

df["是否异常"] = df["销售额"] > 10000
abnormal_count = df["是否异常"].sum()
print(f"标记异常订单:{abnormal_count}个(销售额>10万)")

df_clean = df[~df["是否异常"]].copy()
print(f"清洗后有效数据:{len(df_clean)}行")

print("\n----多维度统计----")

total_sales = df_clean["销售额"].sum()
total_profit = df_clean["利润"].sum()
total_orders = len(df_clean)
avg_order = df_clean["销售额"].mean()
profit_rate = total_profit / total_sales * 100

print(f"总销售额：{total_sales:,.2f} 元")
print(f"总利润：{total_profit:,.2f} 元")
print(f"订单数：{total_orders}")
print(f"客单价：{avg_order:,.2f} 元")
print(f"利润率：{profit_rate:.1f}%")

by_product = df_clean.groupby("产品")["销售额"].sum().sort_values(ascending=False).head(10)
by_category = df_clean.groupby("类别")["销售额"].sum().sort_values(ascending=False)
by_region = df_clean.groupby("地区")["销售额"].sum().sort_values(ascending=False)
by_month = df_clean.groupby("月份")["销售额"].sum().sort_values(ascending=False)
by_salesperson = df_clean.groupby("销售员")["销售额"].sum().sort_values(ascending=False)

print("\n----生成图表----")
charts = []

plt.figure(figsize=(12,6))
plt.bar(by_product.index,by_product.values,color='steelblue')
plt.title('产品销售额 TOP10',fontsize=14)
plt.xlabel('产品',fontsize=12)
plt.ylabel('销售额（元）',fontsize=12)
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
img1 = "images/01_产品销售额.png"
plt.savefig(os.path.join(output_dir,img1),dpi=150)
plt.close()
charts.append(("产品销售额 TOP10",img1))
print("产品销售额柱状图")

plt.figure(figsize=(8,8))
plt.pie(by_category.values,labels=by_category.index,autopct='%1.1f%%',startangle=90)
plt.title('各类别销售额占比',fontsize=14)
plt.tight_layout()
img2 = "images/02_类别占比.png"
plt.savefig(os.path.join(output_dir,img2),dpi=150)
plt.close()
charts.append(("类别销售额",img2))
print("类别占比饼图")

plt.figure(figsize=(12,6))
plt.plot(by_month.index,by_month.values,marker='o',color='coral',linewidth=2)
plt.title('月份销售趋势',fontsize=14)
plt.xlabel('月份',fontsize=12)
plt.ylabel('销售额（元）',fontsize=12)
plt.xticks(rotation=45)
plt.grid(True,alpha=0.3)
plt.tight_layout()
img3 = "images/03_月度趋势.png"
plt.savefig(os.path.join(output_dir,img3),dpi=150)
plt.close()
charts.append(("月份销售趋势",img3))
print("月度趋势趋势图")

plt.figure(figsize=(10,6))
plt.bar(by_region.index,by_region.values,color='seagreen')
plt.title('各地区销售额',fontsize=14)
plt.xlabel('地区',fontsize=12)
plt.ylabel("销售额（元）",fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
img4 = "images/04_地区销售额.png"
plt.savefig(os.path.join(output_dir,img4),dpi=150)
plt.close()
charts.append(("各地区销售额",img4))
print("地区销售额柱状图")


print("\n----AI智能分析----")

data_summary = f"""
电商销售数据概览：
- 总销售额：{total_sales:,.2f}元
- 总利润：{total_profit:,.2f}元
- 订单数：{total_orders}
- 客单价：{avg_order:,.2f}元
- 利润率：{profit_rate:.1f}%
- 数据清洗：删除重复{dup_count}行，处理缺失值{missing_before}个，标记异常{abnormal_count}个

产品销售额TOP5：
{by_product.head(5).to_string()}

类别销售额：
{by_category.to_string()}

地区销售额：
{by_region.to_string()}

销售员TOP3：
{by_salesperson.head(3).to_string()}

月度销售趋势（最近6个月）：
{by_month.tail(6).to_string()}
"""

messages = [
    {"role":"system","content":"你是一位资深电商数据分析师。请根据提供的销售数据，写一份专业的电商销售分析报告，包含：1. 整体业绩概述；2. 产品分析（热销品、潜力品）；3. 区域市场分析；4. 销售趋势分析；5. 问题与风险提示；6. 具体改进建议（至少4条）。用中文，数据驱动，结论明确，建议可执行。每部分用小标题。"},
    {"role":"user","content":f"请分析以下电商销售数据:\n{data_summary}"}
]

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=messages,
    temperature=0.7
)
ai_analysis = response.choices[0].message.content
print("AI分析完成")

print("\n----生成HTML报告----")

ai_html =""
for line in ai_analysis.split("\n"):
    line = line.strip()
    if line:
        if (line[0].isdigit() and "、" in line[:5]) or ("：" in line and len(line) < 30):
            ai_html += f"<h3>{line}</h3>\n"
        else:
            ai_html += f"<p>{line}</p>\n"

# 图表HTML
chart_html = ""
for title, img in charts:
    chart_html += f"<h3>{title}</h3><img src='{img}' alt='{title}'>\n"

# 统计表格
product_table = "<table><tr><th>产品</th><th>销售额</th></tr>"
for name, val in by_product.head(10).items():
    product_table += f"<tr><td>{name}</td><td>{val:,.2f}</td></tr>"
product_table += "</table>"

region_table = "<table><tr><th>地区</th><th>销售额</th></tr>"
for name, val in by_region.items():
    region_table += f"<tr><td>{name}</td><td>{val:,.2f}</td></tr>"
region_table += "</table>"

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>电商销售数据分析报告</title>
<style>
body {{ font-family: "Microsoft YaHei", sans-serif; max-width: 1000px; margin: 0 auto; padding: 30px; background: #f0f2f5; }}
.container {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
h1 {{ color: #1a1a2e; border-bottom: 4px solid #e94560; padding-bottom: 15px; }}
h2 {{ color: #16213e; margin-top: 35px; border-left: 5px solid #e94560; padding-left: 12px; }}
h3 {{ color: #0f3460; margin-top: 20px; }}
p {{ line-height: 1.8; color: #444; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
th, td {{ border: 1px solid #e0e0e0; padding: 10px 15px; text-align: left; }}
th {{ background: #16213e; color: white; }}
tr:nth-child(even) {{ background: #f8f9fa; }}
img {{ max-width: 100%; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
.card {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
.card .num {{ font-size: 24px; font-weight: bold; }}
.card .label {{ font-size: 13px; opacity: 0.9; margin-top: 5px; }}
</style>
</head>
<body>
<div class="container">
<h1>📊 电商销售数据分析报告</h1>

<h2>一、销售总览</h2>
<div class="cards">
<div class="card"><div class="num">{total_sales/10000:.1f}万</div><div class="label">总销售额</div></div>
<div class="card"><div class="num">{total_profit/10000:.1f}万</div><div class="label">总利润</div></div>
<div class="card"><div class="num">{total_orders}</div><div class="label">订单数</div></div>
<div class="card"><div class="num">{profit_rate:.1f}%</div><div class="label">利润率</div></div>
</div>
<p>数据清洗：删除重复 <strong>{dup_count}</strong> 行，处理缺失值 <strong>{missing_before}</strong> 个，标记异常订单 <strong>{abnormal_count}</strong> 个。</p>

<h2>二、产品分析</h2>
{product_table}

<h2>三、区域分析</h2>
{region_table}

<h2>四、数据可视化</h2>
{chart_html}

<h2>五、AI 智能分析与建议</h2>
{ai_html}

<hr>
<p style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
本报告由电商销售数据分析系统自动生成 | Python + pandas + matplotlib + AI
</p>
</div>
</body>
</html>
"""

report_file = os.path.join(output_dir,"电商销售分析报告.html")
with open(report_file,"w",encoding="utf-8")as f:
    f.write(html)

print(f"\n{'=' * 60}")
print(f"  ✅ 报告已生成：{report_file}")
print(f"  用浏览器打开即可查看完整报告")
print(f"{'=' * 60}")