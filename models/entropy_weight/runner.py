"""Entropy-weight method implementation."""

import numpy as np
import pandas as pd

from core.validator import validate_numeric_dataframe


def validate_entropy_weight_input(df: pd.DataFrame) -> None:
    """Validate input rules required by the entropy-weight model."""

    validate_numeric_dataframe(df)


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize each column to the range from 0 to 1."""

    normalized_df = pd.DataFrame(index=df.index)

    for column in df.columns:
        column_min = df[column].min()
        column_max = df[column].max()

        if column_max == column_min:
            normalized_df[column] = 1.0
        else:
            normalized_df[column] = (df[column] - column_min) / (column_max - column_min)

    return normalized_df


def calculate_proportions(normalized_df: pd.DataFrame) -> pd.DataFrame:
    """Convert normalized values into proportions for each column."""

    proportion_df = pd.DataFrame(index=normalized_df.index)

    for column in normalized_df.columns:
        column_sum = normalized_df[column].sum()

        if column_sum == 0:
            proportion_df[column] = 1 / len(normalized_df)
        else:
            proportion_df[column] = normalized_df[column] / column_sum

    return proportion_df


def calculate_entropy(proportion_df: pd.DataFrame) -> pd.Series:
    """Calculate the entropy value of each column."""

    row_count = len(proportion_df)
    entropy_values: dict[str, float] = {}

    for column in proportion_df.columns:
        proportions = proportion_df[column].replace(0, np.nan)
        entropy = -(proportions * np.log(proportions)).sum(skipna=True) / np.log(row_count)
        entropy_values[column] = float(entropy)

    return pd.Series(entropy_values)


def calculate_difference_coefficients(entropy_series: pd.Series) -> pd.Series:
    """Calculate the difference coefficient of each column."""

    return 1 - entropy_series


def calculate_weights(difference_series: pd.Series) -> pd.Series:
    """Calculate the final weights from difference coefficients."""

    total = difference_series.sum()

    if total == 0:
        return pd.Series(
            [1 / len(difference_series)] * len(difference_series),
            index=difference_series.index,
            dtype=float,
        )

    return difference_series / total


def run_model(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full entropy-weight method and return the result table."""

    validate_entropy_weight_input(df)

    normalized_df = normalize_dataframe(df)
    proportion_df = calculate_proportions(normalized_df)
    entropy_series = calculate_entropy(proportion_df)
    difference_series = calculate_difference_coefficients(entropy_series)
    weight_series = calculate_weights(difference_series)

    result_df = pd.DataFrame(
        {
            "指标名": weight_series.index,
            "权重": weight_series.values,
        }
    )

    return result_df.sort_values(by="权重", ascending=False).reset_index(drop=True)
