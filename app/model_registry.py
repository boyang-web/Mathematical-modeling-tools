"""Simple model registry for the Streamlit application."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd

from core.runtime import get_runtime_root
from models.entropy_weight.runner import run_model as run_entropy_weight_model


@dataclass(frozen=True)
class ModelConfig:
    """Configuration used to render and run a model page."""

    key: str
    display_name: str
    description: str
    example_file_path: Path
    example_download_name: str
    accepted_file_types: list[str]
    result_download_name: str
    runner: Callable[[pd.DataFrame], pd.DataFrame]


PROJECT_ROOT = get_runtime_root()

MODEL_REGISTRY: dict[str, ModelConfig] = {
    "entropy_weight": ModelConfig(
        key="entropy_weight",
        display_name="熵权法",
        description="上传 CSV 或 Excel 文件，计算各指标的熵权。",
        example_file_path=PROJECT_ROOT / "models" / "entropy_weight" / "example.csv",
        example_download_name="entropy_weight_example.csv",
        accepted_file_types=["csv", "xlsx", "xls"],
        result_download_name="entropy_weight_result.xlsx",
        runner=run_entropy_weight_model,
    )
}
