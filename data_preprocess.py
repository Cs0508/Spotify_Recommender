from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

# 定义文件路径
data_folder = Path(__file__).parent / "dataset/input"
config_folder = Path(__file__).parent / "dataset/config"

print("\n📂 数据文件夹路径:", data_folder.resolve())

# 读取列名配置的函数
def read_columns_from_txt(filename):
    file_path = config_folder / filename
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 读取列名配置
date_cols = read_columns_from_txt("date_cols.txt")
id_cols = read_columns_from_txt("id_cols.txt")
numeric_cols = read_columns_from_txt("numeric_cols.txt")
ignore_cols = read_columns_from_txt("ignore_cols.txt")

print("\n📋 读取的列名配置:")
print("📆 日期列:", date_cols)
print("🔢 ID 列:", id_cols)
print("📊 数值列:", numeric_cols)
print("🚫 忽略列:", ignore_cols)

# 获取所有 CSV 文件
csv_files = list(data_folder.glob("*.csv"))

# 如果没有找到文件，退出
if not csv_files:
    print("⚠️ 没有找到 CSV 文件！请检查数据文件夹。")
    exit()

# 显示文件列表
print("\n📋 找到以下 CSV 文件:")
for i, file in enumerate(csv_files):
    print(f"{i+1}. {file.name}")

# 让用户选择要处理的文件
selected_indices = input("\n请输入要处理的文件编号（多个文件请用逗号分隔，例如 1,3,5）：")

# 解析用户输入
try:
    selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(",")]
    selected_files = [csv_files[i] for i in selected_indices if 0 <= i < len(csv_files)]
except ValueError:
    print("⚠️ 输入格式错误，请输入有效的文件编号！")
    exit()

# 预处理函数
def process_file(file_path):
    # 读取 CSV，保留原始列顺序
    df = pd.read_csv(file_path)
    original_columns = df.columns.tolist()  # 记录原始列顺序

    # 确定未分类的列（原样保留）
    all_cols = set(df.columns)
    classified_cols = set(date_cols + id_cols + numeric_cols + ignore_cols)
    other_cols = list(all_cols - classified_cols)  # 未分类的列，原样保留

    print(f"\n📌 未分类的列（原样保留）: {other_cols}")

    # 删除 ignore_cols 中的列
    df.drop(columns=ignore_cols, errors='ignore', inplace=True)

    # 只保留未被忽略的列，并保持原始顺序
    remaining_cols = [col for col in original_columns if col in df.columns]  # 保留其他列并按原始顺序排列

    # 保证未分类的列（other_cols）也被保留
    df = df[remaining_cols]  # 将列按原始顺序重新排列，包含未分类的列

    # 去重
    df.drop_duplicates(inplace=True)

    # 处理缺失值（数值列填充中位数）
    df.fillna(df.median(numeric_only=True), inplace=True)

    # 处理日期列
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    df.dropna(subset=date_cols, inplace=True)

    # 编码 ID 类别变量
    for col in id_cols:
        if col in df.columns:
            df[col] = df[col].astype('category').cat.codes

    # 归一化数值特征
    if numeric_cols:
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df

# 处理所选的 CSV 文件
for file in tqdm(selected_files, desc="处理中"):
    df_cleaned = process_file(file)
    cleaned_file_path = data_folder.parent / f"output/cleaned_{file.name}"

    print("\n📝 预览处理后的数据（前 5 行）：")
    print(df_cleaned.head())

    df_cleaned.to_csv(cleaned_file_path, index=False)
    print(f"✅ 已处理并保存: {cleaned_file_path}")
