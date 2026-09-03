# 课程设计AI：工业设备传感器故障预警系统
制造智能技术课程设计，B/S架构，面向工厂设备运维，实现涡轮发动机故障预警。

## 项目模块
1. data：NASA C‑MAPSS工业数据集，数据预处理脚本
2. model：LSTM故障预测训练、评估代码
3. backend：FastAPI后端接口服务
4. frontend：web前端交互页面
5. database：sqlite数据库脚本
6. logs：训练日志、实验截图
7. prompt：vibe‑coding全部AI对话记录（过程档案）

## 阶段文档
- 选题说明.md：项目选题
- 方案设计.md：整体方案规划
- 模型训练.md：模型训练评估报告
- 系统实现.md：前后端数据库集成实现

## 数据集
NASA C‑MAPSS涡轮发动机退化数据集，存放于 ./data

## 运行说明
1. 安装项目依赖
2. 初始化sqlite数据库
3. 启动FastAPI后端服务
4. 在浏览器打开前端页面，使用故障预警系统
