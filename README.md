# course-design-ai
## 数据来源
本项目使用公开数据集：IMDB电影评论数据集
访问地址：https://hf-mirror.com/datasets/stanfordnlp/imdb
数据存放位置：`./data/`
## 数据预处理
预处理脚本位置：`./data/preprocess.py`
处理操作：数据去重、过滤无效样本、字段格式规范化
处理输出：`./data/processed_data.csv`
## 项目运行说明
### 环境依赖
Python版本：Python 3.9+
安装项目所需依赖库：
```bash
pip install -r requirements.txt
```
Course‑design‑AI/
├── data/                # 数据集、预处理后数据存放目录
│   ├── preprocess.py    # 数据预处理脚本
│   └── README.md        # 数据集说明文档
├── prompt/              # AI交互对话记录json文件
├── 选题说明.md
├── 方案设计.md
├── 学习笔记.md
└── README.md
```bash
git clone https://github.com/SDY12326/course-design-ai
cd course-design-ai
pip install -r requirements.txt
python data/preprocess.py
# 后续上传主代码后替换此处启动命令
```
# python main.py
### AI提示词记录
项目全部与AI工具交互记录存放于`prompt/`目录，分阶段保存json文件。
### 遇到的问题与解决方案
1. 问题：数据集下载缓慢
> 解决：使用hf镜像站点，加速数据集获取。
2. 问题：预处理内存占用高
> 解决：采用分批读取处理数据，降低内存开销。