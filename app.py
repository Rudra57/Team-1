import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Evidence Table", layout="wide")

path = Path("data/output/output.csv")

st.title("Evidence Table")

if not path.exists():
    st.error(f"File not found.")
    st.stop()

df = pd.read_csv(path)

st.write(f"Rows: {len(df)} | Columns: {len(df.columns)}")

search = st.text_input("Search table")

if search:
    mask = df.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1
    )
    df_display = df[mask]
else:
    df_display = df

st.dataframe(df_display, use_container_width=True, height=700)

csv_download = df_display.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download",
    data=csv_download,
    file_name="evidence_table.csv",
    mime="text/csv"
)