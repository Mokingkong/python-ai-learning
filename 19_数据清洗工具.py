import pandas as pd
import numpy as np

print("=" * 55)
print("  数据清洗工具")
print("  自动检测 + 清洗 + 对比报告")
print("=" * 55)

#读数据
file_path = input("\n请输入数据文件路径：").strip()

try:
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsv",".xls"):
        df = pd.read_excel(file_path)
    else:
        print("仅支持CSV和Excel")
        exit()
except Exception as e:
    print(f"读取失败:{e}")
    exit()

print(f"读取成功，原始数据:{len(df)}行,{len(df.columns)}列")

df_original = df.copy()

#清洗前检验报告(重复行，缺失值)
print("\n"+"="*55)
print(" 清洗前检验")
print("="*55)

dup_count = df.duplicated().sum()
print(f"\n重复行:{dup_count}行")

missing = df.isnull().sum()
missing = missing[missing > 0]
print("\n 缺失值统计:")
if not missing.empty:
    for col,cnt in missing.items():
        pct = cnt / len(df)*100
        print(f"    {col}: {cnt} 个 ({pct:.1f})")
else:
    print(" 无缺失值")

print(f"\n各列数据类型:")
print(df.dtypes.to_string())

#除去重复

print("\n" + "=" * 55)
print("  开始自动清洗")
print("=" * 55)

if dup_count >0:
    df = df.drop_duplicates()
    print(f"\n 已删除{dup_count}行重复数据，剩余{len(df)}行")
else:
    print("\n无重复行,跳过")


#缺失处理(缺失值处理的三条规则：1.缺失超50%直接删除列（数据少无价值）2.中位数填充 3.文字用“未知”填充)
print("\n----缺失值处理----")
numeric_col = df.select_dtypes(include=["number"]).columns.to_list()
text_cols = df.select_dtypes(include=["object"]).columns.to_list()

for col in df.columns:
    null_cnt = df[col].isnull().sum()
    if null_cnt == 0:
        continue

    null_pnt = null_cnt / len(df) *100

    if null_cnt > 50:
        df = df.drop(columns=[col])
        print(f"删除列{col}:缺失率{null_pnt:.1f}% > 50%")

    elif col in numeric_col:
        median_val = df[col].median
        df[col] = df[col].fillna(median_val)
        print(f"    数值列{col}:用中位数{median_val}填充{null_cnt}个缺失值")

    else:
        df[col] = df[col].fillna("未知")
        print(f"    文字列{col}:用“未知”填充{null_cnt}个缺失值")

#字符串清理(去空格，统一格式)
print("----字符串清理----")
for col in text_cols:
    if col in df.columns:
        before = df[col].isnull().sum()
        df[col] = df[col].astype(str).str.strip()
        #空值NAN变成了“nan”，现在要把“nan”空值去除
        df[col] = df[col].replace("nan",np.nan)
        print(f"{col}:已去除前后空格")

for col in numeric_col:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col],errors="coerce")

#异常值检测(标记，不删除，异常只是异常)
print("\n----异常值检测----")
outlier_report = []
for col in numeric_col:
    if col not in df.columns:
        continue

    if not pd.api.types.is_numeric_dtype(df[col]):
        print(f"    {col}:不是数值类型，跳过异常值检测")
        continue

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3-Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]
    if len(outliers) > 0:
        print(f"{col}:检测到{len(outliers)}个异常值(范围[{lower:.2f},{upper:.2f}])")
        outlier_report.append(f"{col}:{len(outliers)}个异常值，正常范围[{lower:.2f},{upper:.2f}]")
        df[f"{col}_是否异常"] = (df[col] < lower) | (df[col] > upper)

    else:
        print(f"{col}:无异常值")

#清洗后报告
print("\n" + "=" * 55)
print("  清洗完成")
print("=" * 55)
print(f"\n清洗后数据：{len(df)} 行，{len(df.columns)} 列")

missing_after = df.isnull().sum().sum()
print(f"剩余缺失值:{missing_after}个")

#保存
clean_file = "清洗后_" + file_path
if file_path.endswith(".csv"):
    df.to_csv(clean_file,index=False,encoding="utf-8-sig")
else:
    df.to_excel(clean_file,index=False)

print(f"\n 清洗后数据已保存到:{clean_file}")

report_file = "数据清洗报告.txt"
with open(report_file,"w",encoding="utf-8")as f:
    f.write("="*55+"\n")
    f.write("   数据清洗报告\n")
    f.write("="*55+"\n\n")
    f.write(f"原始文件:{file_path}\n")
    f.write(f"清洗前:{len(df_original)}行,{len(df_original.columns)}列\n")
    f.write(f"清洗后:{len(df)}行,{len(df.columns)}列\n")
    f.write(f"删除重复行:{dup_count}行\n")
    f.write(f"剩余缺失值:{missing_after}个\n\n")

    f.write("[缺失值处理详细]\n")
    if not missing.empty:
        for col,cnt in missing.items():
            f.write(f"  {col}:原始缺失{cnt}个\n")
    else:
        f.write("无缺失值")

    if outlier_report:
        f.write("\n[异常值检测]\n")
        for item in outlier_report:
            f.write(f" {item}\n")
        f.write("\n注意，异常值已标记，未删除，请人工核实后决定是否保留。")

print(f"清理报告已保存到:{report_file}")
print(f"\n提示，异常值制作了标记，没有删除，请打开清洗后的文件查看“是否异常”列,人工判断是否保留。")
