"""
NASA C‑MAPSS涡轮发动机数据集预处理脚本
工业设备传感器时序数据清洗、归一化、特征筛选
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# 读取原始NASA数据集，此处使用train_FD001.txt
column_names = ['engine_id','cycle','setting1','setting2','setting3'] + [f"s{i}" for i in range(1,24)]
df_raw = pd.read_csv("./data/train_FD001.txt",sep='\s+',names=column_names)

# 1 构造RUL剩余使用寿命标签（故障预测标签）
rul_df = df_raw.groupby("engine_id")["cycle"].max().reset_index()
rul_df.columns = ["engine_id","max_cycle"]
df = pd.merge(df_raw,rul_df,on="engine_id")
df["RUL"] = df["max_cycle"] - df["cycle"]
# 二分类：RUL<=30 视为即将故障，标签1；否则正常标签0
df["fault_label"] = (df["RUL"] <= 30).astype(int)
df.drop(columns=["max_cycle"],inplace=True)

# 2 数据清洗：删除全零无意义传感器特征
drop_cols = ["setting3","s1","s5","s10","s16","s18","s19"]
df.drop(columns=drop_cols,errors="ignore",inplace=True)

# 3 归一化传感器特征
sensor_cols = [col for col in df.columns if col.startswith("s")]
scaler = StandardScaler()
df[sensor_cols] = scaler.fit_transform(df[sensor_cols])

# 4 输出预处理完成数据集
df.to_csv("./data/processed_industrial_data.csv",index=False,encoding="utf‑8")
print("预处理完成，输出文件：data/processed_industrial_data.csv")
print(f"数据集样本数量：{len(df)}")
print(f"故障样本数量：{df['fault_label'].sum()}")
