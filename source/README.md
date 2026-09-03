# 源码目录

本目录集中保存系统运行所需的应用源码与数据库 SQL：

- `backend/`：FastAPI 服务与智能诊断算法
- `frontend/`：浏览器端工作台
- `database/`：SQLite 访问模块和 `schema.sql`
- `data/`：NASA C-MAPSS 数据、预处理和入库脚本
- `model/`：RandomForest 训练与评估代码
- `tests/`：API 与算法自动化测试
- `启动系统.ps1`：Windows 一键启动脚本

在项目根目录运行 `./source/启动系统.ps1` 可启动系统。
