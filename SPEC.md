# 数学建模工具箱 v0.1

## 目标
开发一个本地使用的 Streamlit 小工具，供数学建模团队使用。

## 第一版功能
1. 上传 CSV 或 Excel 文件
2. 读取数据为 pandas DataFrame
3. 执行熵权法计算
4. 在页面展示结果
5. 支持导出结果为 Excel

## 技术栈
- Python
- Streamlit
- pandas
- numpy
- openpyxl

## 结构要求
- app/main.py：页面入口
- core/io.py：读取和导出文件
- core/validator.py：数据校验
- models/entropy_weight/runner.py：熵权法计算

## 原则
- 只做最小可运行版本（MVP）
- 不实现多模型
- 不实现数据库
- 不做复杂 UI
- 保持代码简单清晰