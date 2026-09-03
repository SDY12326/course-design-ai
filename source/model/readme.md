# model 目录说明
本目录存放监督学习模型训练与评估代码。在线服务使用 RandomForest 风险分类器 + z-score 异常检测；这样在普通 CPU 上即可复现实验结果，并且保留了可解释的传感器风险规则。

## 文件清单
1. train.py：RandomForest 风险分类器训练脚本
2. evaluate.py：准确率、精确率、召回率、F1 评估脚本
3. risk_classifier.joblib：训练后输出的模型权重文件（本地运行生成）

## 模型说明
- 输入：轴承温度、振动、油压、转速、油液污染度、单位能耗六项特征
- 输出：二分类概率，判断设备是否即将发生故障
- 评估指标：准确率、精确率、召回率、F1分数、混淆矩阵

## 运行顺序
1. 先运行 `python source/data/preprocess.py` 生成预处理数据集
2. 运行 `python source/model/train.py` 训练模型，输出 `source/model/risk_classifier.joblib`
3. 运行 `python source/model/evaluate.py` 完成模型评估，评估结果输出至 `logs/eval_result.json`
