import pandas as pd 
import os 
import glob
from pandas import DataFrame

print("="*55)
print(" 批量合并 Excel / CSV 工具")
print(" 自动便利文件夹 -> 读取所有表格 -> 合并 -> 输出日志")
print("="*55)

#读取路径
folder_path = input("\n请输入文件夹路径(例:./待合并文件):").strip()

if not os.path.isdir(folder_path):
    print(f"文件夹不存在:{folder_path}")
    exit()

#找到文件夹内所有表格文件
extensions = ["*.csv","*.xlsx","*.xls"]
all_files = []

for ext in extensions:
    files = glob.glob(os.path.join(folder_path,ext))
    all_files.extend(files)

for ext in extensions:
    files = glob.glob(os.path.join(folder_path,"**",ext),recursive=True)
    all_files.extend(files)

    #glob匹配当前文件夹下该类型文件

#去重
all_files = sorted(list(set(all_files)))

if not all_files:
    print(" 该文件下没有找到Excel 或 CSV文件")
    exit()

#读取合并
print("\n正在读取合并")

dfs:list[DataFrame] = []                #存所有DataFrame
merge_log = []          #合并日志
failed_files = []

for file_path in all_files:
    file_name = os.path.basename(file_path)
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path,engine="openpyxl")

        df["来源文件"] = file_name

        dfs.append(df)
        merge_log.append(f"{file_name}:{len(df)}行,{len(df.columns)}列")
        print(f"{file_name}:{len(df)}行")

    except Exception as e:
        failed_files.append(f"{file_name}:{e}")
        print(f"{file_name}:读取失败({e})")

if not dfs:
    print("\n所有文件都读取失败,无法合并")
    exit()

#合并
merged = pd.concat(dfs,ignore_index=True)

print(f"\n合并前共{len(dfs)}个文件")
print(f"合并后:{len(merged)}行,{len(merged.columns)}列")

dup_count = merged.duplicated().sum()
if dup_count > 0:
    merged = merged.drop_duplicates()
    print(f"删除重复行:{dup_count}行")
    print(f"去重后:{len(merged)}行")

#保存合并文件
output_file = os.path.join(folder_path,"合并结果.xlsx")
merged.to_excel(output_file,index=False,engine="openpyxl")
print(f"\n合并结果已保存到:{output_file}")

log_file = os.path.join(folder_path,"合并日志.txt")
with open(log_file,"w",encoding="utf-8")as f:
    f.write("=" * 55 + "\n")
    f.write("  批量合并日志\n")
    f.write("=" * 55 + "\n\n")
    f.write(f"文件夹：{folder_path}\n")
    f.write(f"找到文件数：{len(all_files)}\n")
    f.write(f"成功读取：{len(dfs)} 个\n")
    f.write(f"读取失败：{len(failed_files)} 个\n")
    f.write(f"合并前行数：{sum(len(df) for df in dfs)}\n")
    f.write(f"合并后行数：{len(merged)}\n")
    f.write(f"删除重复行：{dup_count}\n\n")
    
    f.write("【各文件详情】\n")
    for log in merge_log:
        f.write(f"  {log}\n")
    
    if failed_files:
        f.write("\n【读取失败的文件】\n")
        for fail in failed_files:
            f.write(f"  {fail}\n")

print(f"✅ 合并日志已保存到：{log_file}")
print("\n💡 提示：合并后的文件里有'来源文件'列，可以追溯每条数据来自哪个原始文件。")