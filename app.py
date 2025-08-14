import streamlit as st
import pandas as pd
import re
from io import StringIO, BytesIO
import os, csv


st.set_page_config(page_title="Anki txt to xlsx converter", layout="centered")
st.title("Anki txt to xlsx converter")

# -------------------
# Instructions
# -------------------
st.markdown("### How to Export Your Deck")

st.markdown("1. **Press on the settings icon next to the deck**")
st.image("image1.png", use_container_width=True)

st.markdown("2. **Then select export**")
st.image("image2.png", use_container_width=True)

st.markdown("3. **Change the format to 'Cards in plain text (TXT)', make sure the deck is correct, and UNCHECK 'Include HTML'**")
st.image("image3.png", use_container_width=True)

uploaded_file = st.file_uploader("Upload your exported tab-separated `.txt` file", type=["txt"])

def clean_preserve_tabs(text: str) -> str:
    # Keep printable ASCII (0x20–0x7E) PLUS tab/newline/carriage return
    return re.sub(r"[^\t\n\r\x20-\x7E]", "", text)

if uploaded_file:
    base_name = os.path.splitext(uploaded_file.name)[0]
    output_filename = f"{base_name}.xlsx"

    # Decode with utf-8 then fallback
    raw = uploaded_file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1", errors="ignore")

    cleaned = clean_preserve_tabs(text)

    # Parse as TSV, skipping the first 2 rows
    df = pd.read_csv(
        StringIO(cleaned),
        sep="\t",
        header=None,
        skiprows=2,
        engine="python",
        dtype=str,
        quoting=csv.QUOTE_NONE,
        on_bad_lines="skip",
    )
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    st.subheader("Preview")
    st.dataframe(df.head(30), use_container_width=True)

    # Download as Excel
    buf = BytesIO()
    df.to_excel(buf, index=False, header=False)
    buf.seek(0)
    st.download_button(
        f"Download {output_filename}",
        data=buf,
        file_name=output_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
