from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

# 定义数据文件夹路径
data_folder = Path(__file__).parent / "dataset/input"

print("\n📂 数据文件夹路径:", data_folder.resolve())

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
    df = pd.read_csv(file_path)

    # 去重
    df.drop_duplicates(inplace=True)

    # 处理缺失值（数值列填充中位数）
    df.fillna(df.median(numeric_only=True), inplace=True)

    # 处理日期列
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df.dropna(subset=['release_date'], inplace=True)

    # 编码分类变量
    id_columns = ['track_id', 'playlist_id', 'album_id', 'artist_ids']
    for col in id_columns:
        if col in df.columns:
            df[col] = df[col].astype('category').cat.codes

    # 归一化数值特征
    scaler = MinMaxScaler()
    numeric_cols = ['danceability', 'energy', 'loudness', 'speechiness', 
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df

# 处理所选的 CSV 文件
for file in tqdm(selected_files, desc="处理中"):
    df_cleaned = process_file(file)
    cleaned_file_path = data_folder.parent / f"output/cleaned_{file.name}"
    
    print("\n📝 预览处理后的数据（前 5 行）：")
    print(df_cleaned[['track_id', 'playlist_id', 'album_id', 'artist_ids']].head())

    df_cleaned.to_csv(cleaned_file_path, index=False)
    print(f"✅ 已处理并保存: {cleaned_file_path}")
