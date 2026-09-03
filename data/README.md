
# data目录说明
存放NASA C‑MAPSS涡轮发动机退化工业数据集，用于设备故障预警。

## 数据集信息
数据集名称：C‑MAPSS Turbofan Engine Degradation Simulation Data
访问地址：https://data.nasa.gov/dataset/C‑MAPSS‑Turbofan‑Engine‑Degradation‑Simulation‑Data

### 文件清单
1. train_FD001.txt：原始发动机传感器时序数据集（本地下载后上传）
2. preprocess.py：工业数据预处理脚本
3. processed_industrial_data.csv：预处理后输出数据集

### 处理说明
1. 计算RUL剩余使用寿命
2. 构造故障二分类标签：RUL≤30标记为故障风险样本
3. 剔除无效传感器字段
4. 传感器特征标准化归一化

> 网页GitHub无法运行脚本，需要本地运行preprocess.py生成processed_industrial_data.csv
