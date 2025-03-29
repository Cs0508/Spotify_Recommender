from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 定义数据文件夹路径
data_folder = Path(__file__).parent / "dataset"

print(data_folder.resolve())

# 获取所有 CSV 文件
csv_files = list(data_folder.glob("*.csv"))
print("找到的文件:", [file.name for file in csv_files])

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
    df['track_id'] = df['track_id'].astype('category').cat.codes
    df['playlist_id'] = df['playlist_id'].astype('category').cat.codes

    # 归一化数值特征
    scaler = MinMaxScaler()
    numeric_cols = ['danceability', 'energy', 'loudness', 'speechiness', 
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df

# 遍历所有 CSV 文件并处理
for file in csv_files:
    df_cleaned = process_file(file)
    cleaned_file_path = data_folder / f"cleaned_{file.name}"
    df_cleaned.to_csv(cleaned_file_path, index=False)
    print(f"已处理并保存: {cleaned_file_path}")
