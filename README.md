# 数学建模工具箱

这是一个给数学建模团队使用的本地 Python 工具。当前第一版提供一个简单的 Streamlit 页面，支持上传 CSV 或 Excel 数据，运行熵权法，查看结果，并下载结果 Excel。

## 项目用途

- 在网页界面中选择模型
- 上传数据文件
- 运行数学建模方法
- 查看结果并下载结果文件
- 为后续打包成 exe 做准备

## 目录结构

```text
math-modeling-toolkit/
├─ app/
│  ├─ __init__.py
│  └─ main.py
├─ models/
│  ├─ __init__.py
│  └─ entropy_weight/
│     ├─ __init__.py
│     ├─ example.csv
│     └─ runner.py
├─ core/
│  ├─ __init__.py
│  ├─ io.py
│  └─ validator.py
├─ build_exe.bat
├─ launch.py
├─ requirements.txt
└─ README.md
```

## 安装依赖

建议使用 Python 3.10 及以上版本。

Windows 环境建议优先使用标准虚拟环境解释器：

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

```bash
pip install -r requirements.txt
```

## 如何运行 Streamlit

推荐使用启动脚本运行：

```bash
python launch.py
```

如果你使用的是 Windows 虚拟环境，更稳的方式是：

```bash
.venv\Scripts\python.exe launch.py
```

也可以直接运行：

```bash
streamlit run app/main.py
```

启动后浏览器会打开“数学建模工具箱”页面。当前版本先支持一个模型：熵权法。

## 如何测试熵权法

1. 启动项目。
2. 在左侧选择“熵权法”。
3. 点击“下载示例数据”。
4. 上传 `models/entropy_weight/example.csv`，或上传你自己的 CSV / Excel 文件。
5. 点击“运行模型”。
6. 页面会展示结果表。
7. 点击“下载结果 Excel”保存结果。

注意：

- 数据表不能为空。
- 数据至少需要 2 行。
- 当前默认所有列都参与熵权法计算。
- 所有列都必须是数值型。

## 各文件作用

- `app/main.py`：负责页面交互，不直接堆放算法细节。
- `app/model_registry.py`：统一维护模型名称、示例文件、运行函数和结果文件名。
- `core/io.py`：负责读取上传文件、导出 Excel、读取示例文件。
- `core/validator.py`：负责检查数据是否适合进入模型计算。
- `models/entropy_weight/runner.py`：负责熵权法的完整计算流程。
- `models/entropy_weight/example.csv`：提供一份可直接测试的示例数据。
- `launch.py`：负责启动 Streamlit，后续也用于 exe 打包入口。
- `build_exe.bat`：Windows 下的一键打包脚本。

## 如何打包 exe

当前项目已经补上了适合内测分发的一版打包机制，推荐按下面步骤进行：

1. 先安装项目依赖。
2. 确保当前 Python 环境可以使用 `PyInstaller`。
3. 执行 `build_exe.bat`。
4. 等待打包完成。
5. 在 `dist/math-modeling-toolkit/` 目录下找到可分发文件夹。
6. 在 `release/` 目录下找到可直接发送的 zip 压缩包。

脚本内部会自动做这些事：

- 优先使用 `.venv\Scripts\python.exe`
- 如果不存在，再回退到其他可用 Python
- 先检查本地是否已安装 `PyInstaller`
- 如果没有，再尝试自动安装 `PyInstaller`
- 清理旧的 `build/`、`dist/` 和 `release/`
- 使用更适合 Streamlit 的 `onedir` 打包方式
- 收集 `streamlit`、`pandas`、`numpy`、`openpyxl`、`xlrd` 相关资源
- 把 `app`、`core`、`models` 目录一起打包进去
- 生成一个便于双击启动的 `启动数学建模工具箱.bat`
- 自动打出 zip 压缩包，方便分发给测试者

## 分发给他人时的建议

建议把 `release/math-modeling-toolkit-win.zip` 发给测试者，或直接发送整个 `dist/math-modeling-toolkit/` 文件夹。

测试者拿到后建议这样使用：

1. 解压整个压缩包到本地目录。
2. 双击 `启动数学建模工具箱.bat`。
3. 稍等几秒，浏览器会自动打开本地页面。
4. 如果浏览器没有自动打开，可以手动访问 `http://127.0.0.1:8501`。

注意：

- 不要只单独发送 `exe` 文件，必须连同整个打包目录一起发送。
- 第一次启动时，Windows 可能弹出防火墙提示，允许本地访问即可。
- 如果测试机器的 `8501` 端口已被占用，可以设置环境变量 `MMT_STREAMLIT_PORT` 后再启动。
- 如果打包阶段提示无法安装 `PyInstaller`，通常是当前环境没有联网或 `pip` 源不可用，需要先手动安装。

## 后续如何继续完善 exe 打包

下一步建议继续完善这几件事：

- 增加一个专门的图标文件，用于 exe 图标
- 增加一个 `version.txt` 或配置文件，方便展示版本号
- 增加端口占用检测和自动切换端口
- 在打包后测试示例文件下载、结果导出、中文路径兼容性
- 如果需要给团队成员分发，可以再补一个安装包方案
