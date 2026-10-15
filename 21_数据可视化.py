import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os

matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei','SimHei','DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

print("="*55)
print(" 数据可视化工具")
print(" 读取数据->生成图表->保存为图片")
print("="*55)

#读取数据
data_file = input("\n请输入数据文件路径(比如 douban_top250.csv)：").strip()

if not os.path.exists(data_file):
    print(f"你丫的文件压根不存在:{data_file}")
    exit()

if data_file.endswith(".csv"):
    df = pd.read_csv(data_file)
else:
    df = pd.read_excel(data_file,engine="openpyxl")

#造输出文件夹
output_dir = "图表输出"
os.makedirs(output_dir,exist_ok=True)

#开始画图，先来个柱状图
print("\n----先来个柱状图开开胃----")

cat_col = input("请输入分类列名（例：‘产品’）:").strip()
val_col = input("请输入数值列名（例：‘销售额’）:").strip()

if cat_col in df.columns and val_col in df.columns:
    chart_data = df.groupby(cat_col)[val_col].sum().sort_values(ascending=False)

    plt.figure(figsize=(10,6))
    plt.bar(chart_data.index,chart_data.values,color='steelblue')
    plt.title(f'{val_col} 按 {cat_col} 统计',fontsize=14)
    plt.xlabel(cat_col,fontsize=12)
    plt.ylabel(val_col,fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    bar_file = os.path.join(output_dir,f'柱状图_{cat_col}_{val_col}.png')
    plt.savefig(bar_file,dpi=150)
    plt.close()
    print(f"柱状图以保存:{bar_file}")
else:
    print(f"列名不存在，跳过柱状图")

print("\n----第二来折线图-----")

make_line = input("是否生成折线图?(y/n):").strip().lower()

if make_line == 'y':
    x_col = input("请输入x轴列名（比如‘日期’）：").strip()
    y_col = input("请输入y轴列名（比如‘销售额’）：").strip()

    if x_col in df.columns and y_col in df.columns:
        df_sorted = df.sort_values(by=x_col)

        plt.figure(figsize=(10,6))
        plt.plot(df_sorted[x_col],df_sorted[y_col],marker='o',color='coral',linewidth=2)
        plt.title(f'{y_col} 变化趋势',fontsize=14)
        plt.xlabel(x_col,fontsize=12)
        plt.ylabel(y_col,fontsize=12)
        plt.grid(True,alpha=0.3)
        plt.tight_layout()

        line_file = os.path.join(output_dir,f'折线图_{x_col}_{y_col}.png')
        plt.savefig(line_file,dpi=150)
        plt.close()
        print(f"折线图已保存:{line_file}")
    else:
        print(f"列名不存在，跳过折线图")

print("\n----三来个饼图----")
make_pie = input("是否生成饼图?:(y/n):").strip().lower()

if make_pie == 'y':
    pie_col = input("请输入分类列名（比如‘产品’）：").strip()
    pie_val = input("请输入数值列名（比如‘销售额’）：").strip()

    if pie_col in df.columns and pie_val in df.columns:
        pie_data = df.groupby(pie_col)[pie_val].sum()

        plt.figure(figsize=(8,8))
        plt.pie(pie_data,labels=pie_data.index,autopct='%1.1f%%',startangle=90)
        plt.title(f'{pie_val} 按{pie_col} 占比',fontsize=14)
        plt.tight_layout()

        pie_file = os.path.join(output_dir,f'饼图_{pie_col}_{pie_val}.png')
        plt.savefig(pie_file,dpi=150)
        plt.close()
        print(f"饼图已保存：{line_file}")
    else:
        print(f"列名不存在，跳过饼图")

print("\n----最后一个来个散点图----")
make_scatter = input("是否生成散点图？（y/n）:").strip().lower()

if make_scatter == 'y':
    x_col = input("请输入X轴数值列名：").strip()
    y_col = input("请输入Y轴数值列名：").strip()

    if x_col in df.columns and y_col in df.columns:
        plt.figure(figsize=(10,6))
        plt.scatter(df[x_col],df[y_col],alpha=0.6,color='green',s=50)
        plt.title(f'{x_col} 与 {y_col} 关系',fontsize = 14)
        plt.xlabel(x_col,fontsize=12)
        plt.ylabel(y_col,fontsize=12)
        plt.grid(True,alpha=0.3)
        plt.tight_layout()

        scatter_file = os.path.join(output_dir,f'散点图_{x_col}_{y_col}.png')
        plt.savefig(scatter_file,dpi=150)
        plt.close()
        print(f"散点图已保存：{scatter_file}")
    else:
        print(f"列名不存在，跳过散点图")

print(f"\n{'=' * 55}")
print(f"  全部图表已保存到文件夹：{output_dir}/")
print(f"{'=' * 55}")