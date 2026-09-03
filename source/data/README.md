
# data目录说明
存放NASA C‑MAPSS涡轮发动机退化工业数据集，用于设备故障预警。

## 数据集信息
数据集名称：C‑MAPSS Turbofan Engine Degradation Simulation Data
官方数据仓库：https://ti.arc.nasa.gov/c/6/

### 文件清单
1. train_FD001.txt：从 NASA 官方数据仓库下载的 FD001 原始发动机传感器时序数据集
2. preprocess.py：工业数据预处理脚本
3. processed_industrial_data.csv：预处理后输出数据集

### 处理说明
1. 计算RUL剩余使用寿命
2. 构造故障二分类标签：RUL≤30标记为故障风险样本
3. 剔除无效传感器字段
4. 传感器特征标准化归一化
5. FD001 实际处理结果：20,631 行、21 列、缺失值 0

> 数据来源：NASA Prognostics Center of Excellence 官方仓库，下载地址：
> https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip
>
> 运行 `python source/data/preprocess.py` 生成 `processed_industrial_data.csv`，再运行
> `python source/data/import_to_db.py` 写入 SQLite 的 `sensor_readings` 表。
