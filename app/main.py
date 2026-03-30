"""Streamlit application entry point for the toolkit."""

from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.model_registry import MODEL_REGISTRY, ModelConfig
from core.io import dataframe_to_excel_bytes, load_example_file, read_table


def render_model_selector() -> str:
    """Render the model selector and return the selected model key."""

    st.sidebar.header("模型列表")
    options = list(MODEL_REGISTRY.keys())
    format_func = lambda key: MODEL_REGISTRY[key].display_name
    return st.sidebar.radio("请选择一个模型", options, format_func=format_func, key="selected_model")


def render_example_download(model: ModelConfig) -> None:
    """Render the example file download area."""

    try:
        example_bytes = load_example_file(model.example_file_path)
    except FileNotFoundError:
        st.info("当前模型暂未提供示例文件。")
        return

    st.download_button(
        label="下载示例数据",
        data=example_bytes,
        file_name=model.example_download_name,
        mime="text/csv",
        key=f"{model.key}_download_example",
    )


def render_model_page(model: ModelConfig) -> None:
    """Render a reusable model page using the model registry configuration."""

    st.subheader(model.display_name)
    st.write(model.description)
    render_example_download(model)

    uploaded_file = st.file_uploader(
        "上传数据文件",
        type=model.accepted_file_types,
        help="请上传与当前模型要求一致的 CSV 或 Excel 数据文件。",
        key=f"{model.key}_uploader",
    )

    preview_df = None
    if uploaded_file is not None:
        try:
            preview_df = read_table(uploaded_file)
            st.write("原始数据预览")
            st.dataframe(preview_df, use_container_width=True)
        except Exception as error:
            st.error(f"文件读取失败：{error}")
            return

    if st.button("运行模型", type="primary", key=f"{model.key}_run_button"):
        if uploaded_file is None:
            st.warning("请先上传 CSV 或 Excel 文件，再运行模型。")
            return

        try:
            source_df = preview_df if preview_df is not None else read_table(uploaded_file)
            result_df = model.runner(source_df)
            result_bytes = dataframe_to_excel_bytes(result_df)

            st.success("模型运行完成。")
            st.write("结果表")
            st.dataframe(result_df, use_container_width=True)
            st.download_button(
                label="下载结果 Excel",
                data=result_bytes,
                file_name=model.result_download_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"{model.key}_download_result",
            )
        except Exception as error:
            st.error(f"模型运行失败：{error}")


def main() -> None:
    """Run the Streamlit application."""

    st.set_page_config(page_title="数学建模工具箱", layout="wide")
    st.title("数学建模工具箱")

    selected_model_key = render_model_selector()
    selected_model = MODEL_REGISTRY[selected_model_key]
    render_model_page(selected_model)


if __name__ == "__main__":
    main()
