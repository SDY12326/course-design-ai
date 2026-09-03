# 数据库说明

`source/database/store.py` 使用 SQLite 初始化三张业务表：

- `equipment`：设备台账、产线、状态、健康度与最后采集时间。
- `sensor_readings`：设备传感器采样 JSON 与时间戳。
- `predictions`：每次诊断的风险分数、RUL、异常传感器和处置建议。

建表语句统一维护在 `source/database/schema.sql`。数据库文件 `source/database/engine.db` 在首次启动时自动创建并注入演示数据，已加入 `.gitignore`，不会把现场运行状态提交到仓库。
