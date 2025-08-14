import streamlit as st
import pandas as pd
import re
from io import BytesIO
import os

st.set_page_config(page_title="Anki txt to xlsx converter", layout="centered")
st.title("Anki txt to xlsx converter")

uploaded_file = st.file_uploader("Upload the anki .txt file", type=["txt"])

def clean_text(s):
    # Keep only printable ASCII characters (space to ~)
    return re.sub(r"[^\t\n\r\x20-\x7E]", "", text)

if uploaded_file:
    # Derive output file name
    base_name = os.path.splitext(uploaded_file.name)[0]
    output_filename = f"{base_name}.xlsx"

    # Read as text
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = text.splitlines()

    # Remove first two rows
    lines = lines[2:]

    # Clean each line
    cleaned_lines = [clean_text(line) for line in lines]

    # Convert to DataFrame with tab as delimiter
    df = pd.DataFrame([row.split("\t") for row in cleaned_lines])

    st.subheader("Preview of spreadsheet")
    st.dataframe(df.head())

    # Export to Excel
    output = BytesIO()
    df.to_excel(output, index=False, header=False)
    output.seek(0)

    st.download_button(
        label=f"Download {output_filename}",
        data=output,
        file_name=output_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
