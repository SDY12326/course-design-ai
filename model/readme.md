# model目录说明
本目录存放工业涡轮发动机故障预测LSTM模型代码

## 文件清单
1. train.py：LSTM时序故障模型训练脚本
2. evaluate.py：模型效果评估脚本
3. fault_lstm.pt：训练完成后输出的模型权重文件（本地运行生成）

## 模型说明
- 输入：50步传感器时序特征
- 输出：二分类概率，判断设备是否即将发生故障
- 评估指标：准确率、精确率、召回率、F1分数、混淆矩阵

## 运行顺序
1. 先运行data/preprocess.py生成预处理数据集
2. 运行train.py训练模型，输出fault_lstm.pt权重
3. 运行evaluate.py完成模型评估，评估结果输出至logs/eval_result.txt
