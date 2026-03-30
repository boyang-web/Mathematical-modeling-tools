"""Validation helpers."""

import pandas as pd
from pandas.api.types import is_numeric_dtype


def validate_numeric_dataframe(df: pd.DataFrame) -> None:
    """Validate a DataFrame for models that require all columns to be numeric."""

    if df.empty:
        raise ValueError("数据表为空，请上传包含指标数据的文件。")

    if len(df) < 2:
        raise ValueError("数据行数过少，至少需要 2 行数据才能计算熵权。")

    non_numeric_columns = [column for column in df.columns if not is_numeric_dtype(df[column])]
    if non_numeric_columns:
        column_names = "、".join(map(str, non_numeric_columns))
        raise ValueError(f"以下列不是数值型，无法进行熵权法计算：{column_names}")
