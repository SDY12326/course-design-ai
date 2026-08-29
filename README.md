# course-design-ai

## 数据来源
本项目使用公开数据集：IMDB电影评论数据集
访问地址：https://hf-mirror.com/datasets/stanfordnlp/imdb
数据存放位置：`./data/`

## 数据预处理
预处理脚本位置：`./data/preprocess.py`
处理操作：数据去重、过滤无效样本、字段格式规范化
处理输出：`./data/processed_data.csv`
