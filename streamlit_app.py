import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="Web Scraping Pipeline",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Python Web Scraping Pipeline")
st.write(
    "Books to Scrape + Quotes to Scrape — "
    "cleaning, validation, deduplication and consolidation."
)

output_dir = Path("output")
csv_file = output_dir / "final_dataset.csv"
summary_file = output_dir / "summary_report.json"

if csv_file.exists():
    df = pd.read_csv(csv_file)

    st.subheader("Final Dataset")
    st.write(f"Total records: **{len(df)}**")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Final Dataset",
        data=df.to_csv(index=False),
        file_name="final_dataset.csv",
        mime="text/csv"
    )

if summary_file.exists():
    with open(summary_file, "r", encoding="utf-8") as file:
        summary = json.load(file)

    st.subheader("Pipeline Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Records Collected",
        summary.get("total_records_collected", 0)
    )

    col2.metric(
        "Duplicates",
        summary.get("duplicate_records_detected", 0)
    )

    col3.metric(
        "Final Records",
        summary.get("final_record_count", 0)
    )

    with st.expander("View Complete Summary"):
        st.json(summary)

else:
    st.warning("summary_report.json not found.")