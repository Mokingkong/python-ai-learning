import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib
import os
from zhipuai import ZhipuAI

#开局必备，中文字体
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei','DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

client = ZhipuAI(api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr")

print("="*55)
print(" AI图文分析报告生成器")
print(" 读取数据 -> 自动统计 -> 生成图表 -> AI分析 -> HTML报告")
print("="*55)

#读取数据

data_file = input("\n请输入数据文件路径：").strip()

if not os.path.exists(data_file):
    exit()

if data_file.endswith(".csv"):
    df = pd.read_csv(data_file)
else:
    df = pd.read_excel(data_file)

print(f"\n读取成功:{len(df)}行,{len(df.columns)}列")
print(f"列名:{list(df.columns)}")

output_dir = "报告输出"
os.makedirs(output_dir,exist_ok=True)
img_dir = os.path.join(output_dir,"images")
os.makedirs(img_dir,exist_ok=True)

#自动统计
print("\n-----正在自动统计-----")

total_rows = len(df)
total_cols = len(df.columns)
missing_total = df.isnull().sum().sum()   #第一个sum统计每一列的缺失量，后一个sum把所有列的缺失量加到一起构成总表缺失量
missing_pct = round(missing_total / (total_rows * missing_total) * 100, 2)

numeric_cols = df.select_dtypes(include=["number"]).columns.to_list()
numeric_stats = df[numeric_cols].describe().round(2) if numeric_cols else pd.DataFrame()

missing_stats = df.isnull().sum()
missing_stats = missing_stats[missing_stats > 0 ].sort_values(ascending=False)

print(f"\n数值列:{numeric_cols}")
print(f"文字列:{list(df.select_dtypes(include=['object']).columns)}")
group_col = input("\n请输入分组列名(比如'产品',没有就值及回车跳过):").strip()
value_col = input("请输入统计数值列名(比如'销售额')").strip()

group_result = None
if group_col and group_col in df.columns and value_col and value_col in df.columns:
    group_result = df.groupby(group_col)[value_col].sum().sort_values(ascending=False)
    print(f"按{group_col}分组统计{value_col}完成")

#画图
print("\n----正在生成图表----")

charts = []
if group_result is not None and len(group_result) > 0:
    plt.figure(figsize=(10,6))
    plt.bar(group_result.index,group_result.values,color='steelblue')
    plt.title(f'{value_col} 按 {group_col} 统计',fontsize=14)
    plt.xlabel(group_col,fontsize=12)
    plt.ylabel(value_col,fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    bar_img = f"images/柱状图_{group_col}_{value_col}.png"
    plt.savefig(os.path.join(output_dir,bar_img),dpi=150)
    plt.close()
    charts.append(("柱状图",bar_img))
    print(f"柱状图已生成")

if group_result is not None and len(group_result) > 0:
    plt.figure(figsize=(8,8))
    plt.pie(group_result.values,labels=group_result.index,autopct='%1.1f%%',startangle=90)
    plt.title(f'{value_col} 按 {group_col} 占比',fontsize=14)
    plt.tight_layout()
    pie_img = f"images/饼图_{group_col}_{value_col}.png"
    plt.savefig(os.path.join(output_dir,pie_img),dpi=150)
    plt.close()
    charts.append(("饼图",pie_img))
    print(f"饼图已生成")

#调用AI分析
print("\n----正在调用AI生成分析----")

data_overview = f"""
数据概览:
- 总行数:{total_rows}
- 总列数:{total_cols}
- 缺失总数:{missing_total}(占比 {missing_pct})
- 数值列:{numeric_cols}
"""

if group_result is not None:
    data_overview += f"\n按{group_col} 分组统计 {value_col}: \n"
    for name,val in group_result.items():
        data_overview += f"- {name}:{val}\n"

if not numeric_stats.empty:
    data_overview += f"\n数值列统计:\n{numeric_stats.to_string()}\n"

messages = [
    {"role":"system","content":"你是一位专业的数据分析师。请根据提供的数据概览，写一份结构清晰的数据分析报告，包含以下部分：1. 数据整体情况概述；2. 关键发现（至少3点）；3. 趋势和规律分析；4. 建议和改进方向。用中文，语言专业但易懂，每部分用小标题。"},
    {"role":"user","content":f"请分析以下数据:\n{data_overview}"}
]

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=messages,
    temperature=0.7
)

ai_analysis = response.choices[0].message.content
print("AI分析完成")

#生成HTML报告
print("\n----正在生成HTML报告----")

ai_paragraphs = ai_analysis.split("\n")
ai_html = ""
for p in ai_paragraphs:
    p = p.strip()
    if p:
        if(p[0].isdigit() and "、" in p[:5]) or (": " in p and len(p) < 30):
            ai_html += f"<h3>{p}</h3>\n"
        else:
            ai_html += f"<p>{p}</p>\n"

#缺失值表格
missing_html = "" 
if len(missing_stats) > 0:
    missing_html = "<table><tr><th>列名</tr><th>缺失数量</th></tr>"
    for col,cnt in missing_stats.items():
        missing_html += f"<tr><td>{col}</td><td>{cnt}</td></tr>"
    missing_html += "</table>"
else:
    missing_html = "<p> 数据完整,无缺失值"

#生成分组统计表格html
group_html = ""
if group_result is not None:
    group_html = f"<h3>按 {group_col} 分组统计 {value_col}</h3>"
    group_html += "<table><tr><th>" + group_col + "</th><th>" + value_col + "</th><tr>"
    for name,val in group_result.items():
        group_html += f"<tr><td>{name}</td><td>{val}</td></tr>"
    group_html+="</table>"

#生成图表html
chart_html = ""
for title,img_path in charts:
    chart_html += f"<h3>{title}</h3>\n<img src='{img_path}' alt='{title}'>\n"

html_content = f"""
<h1>数据分析报告</h1>
<h2>数据概览</h2>
<p>总行数:{total_rows},总列数:{total_cols},缺失值:{missing_total}</p>
<h2>分组统计</h2>
{group_html}
<h2>{chart_html}</h2>
<h2>AI分析</h2>
{ai_html}
"""

report_file = os.path.join(output_dir,"数据分析报告.html")
with open(report_file,"w",encoding="utf-8")as f:
    f.write(html_content)

print(f"\n{'=' * 55}")
print(f"  ✅ 报告已生成：{report_file}")
print(f"  用浏览器打开即可查看完整报告")
print(f"{'=' * 55}")