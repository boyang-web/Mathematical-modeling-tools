"""Common input and output helpers."""

from io import BytesIO
from pathlib import Path

import pandas as pd


def read_table(uploaded_file) -> pd.DataFrame:
    """Read an uploaded CSV or Excel file into a DataFrame."""

    if uploaded_file is None:
        raise ValueError("未接收到上传文件。")

    file_name = uploaded_file.name.lower()

    try:
        uploaded_file.seek(0)

        if file_name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        if file_name.endswith(".xlsx"):
            return pd.read_excel(uploaded_file, engine="openpyxl")
        if file_name.endswith(".xls"):
            return pd.read_excel(uploaded_file, engine="xlrd")
    except Exception as error:
        raise ValueError(f"文件内容无法读取，请检查文件是否损坏或格式是否正确：{error}") from error

    raise ValueError("仅支持 csv、xlsx、xls 格式的文件。")


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to Excel bytes for downloading."""

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="result")
    buffer.seek(0)
    return buffer.getvalue()


def load_example_file(path: str | Path) -> bytes:
    """Load the example file as raw bytes for downloading."""

    return Path(path).read_bytes()
