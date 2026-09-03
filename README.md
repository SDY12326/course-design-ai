# 智维引擎：工业设备预测性维护系统

面向工厂动力段与装配段的 B/S 预测性维护工作台，串联设备台账、传感器时序、风险分类、异常检测、RUL 估计和处置建议。

## 源码目录

所有运行源码与 SQL 集中在 `source/`：`backend`（FastAPI 与算法）、`frontend`（Web UI）、`data`（NASA 数据与处理）、`model`（训练评估）、`database`（SQLite 与 `schema.sql`）、`tests`（自动化测试）以及 `source/启动系统.ps1`。

课程文档、日志、页面截图和演示视频工程保留在项目根目录。

## 运行

```powershell
.\source\启动系统.ps1
```

浏览器访问 http://127.0.0.1:8000，接口文档访问 http://127.0.0.1:8000/docs。

## 测试

```powershell
python -m pytest -q source/tests
```
