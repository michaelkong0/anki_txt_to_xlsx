import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="TXT → Spreadsheet Converter", layout="centered")

st.title("TXT → Spreadsheet Converter")

uploaded_file = st.file_uploader("Upload a tab-separated .txt file", type=["txt"])

def clean_text(s):
    # Keep only basic printable ASCII characters: letters, numbers, punctuation, whitespace
    return re.sub(r"[^ -~]", "", s)

if uploaded_file is not None:
    # Read the uploaded file as a string
    text = uploaded_file.read().decode("utf-8", errors="ignore")

    # Clean each line
    cleaned_lines = [clean_text(line) for line in text.splitlines()]

    # Convert to DataFrame (tab-separated)
    data = [line.split("\t") for line in cleaned_lines]
    df = pd.DataFrame(data)

    st.subheader("Preview of cleaned data")
    st.dataframe(df.head())

    # Export to Excel
    output = BytesIO()
    df.to_excel(output, index=False, header=False)
    output.seek(0)

    st.download_button(
        label="Download as Excel (.xlsx)",
        data=output,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
