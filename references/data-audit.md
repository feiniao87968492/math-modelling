# 数据审计规则 — Data Audit

## 审计清单

### 1. 数据字典

- 记录所有数据文件中的字段名、含义、单位、类型（数值/类别/时间/文本）
- 对含义模糊的字段标记为"待确认"并记录推测含义
- 输出到 `data/facts/data_dictionary.yaml`

### 2. 缺失值

- 统计每个字段的缺失值数量和比例
- 缺失处理策略必须记录方法和数量
- 缺失率 > 30% 的字段需评估是否可用
- 输出到 `data/facts/missing_values.yaml`

### 3. 异常值

- 异常值不能直接删除
- 必须说明异常值的判断标准（IQR、Z-score、业务阈值等）
- 记录异常值对结果的影响评估
- 输出到 `data/facts/outliers.yaml`

### 4. 单位

- 检查所有数值字段的单位是否一致
- 不一致的单位必须转换并记录转换公式
- 无量纲量必须标明

### 5. 重复记录

- 检查完全重复行
- 检查关键字段重复（如同一时间段同一实体多条记录）

### 6. 时间泄露

- 时间序列数据禁止随机划分训练/测试集
- 必须使用滚动窗口、expanding window 或按时间切割
- 特征构造时禁止使用未来信息

### 7. 数据版本

- 所有 processed 数据应有来源追踪
- 数据转换步骤必须记录
- 输出到 `data/facts/data_version.yaml`

## 输出文件

| 文件 | 内容 |
|------|------|
| `data/facts/data_dictionary.yaml` | 全字段字典（名称、含义、单位、类型） |
| `data/facts/missing_values.yaml` | 缺失值统计与处理策略 |
| `data/facts/outliers.yaml` | 异常值判断标准与处理 |
| `data/facts/data_version.yaml` | 数据转换步骤与版本记录 |
