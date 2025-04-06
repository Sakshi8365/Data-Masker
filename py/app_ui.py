import streamlit as st
import pandas as pd
from masker import mask_text

st.set_page_config(page_title="DataMasker 🕵️", layout="centered")

st.title("🕵️ DataMasker - Smart Data Redactor")
st.markdown("Upload a **.txt** or **.csv** file to redact sensitive information with fake data.")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"])

if uploaded_file is not None:
    ext = uploaded_file.name.split(".")[-1].lower()
    st.sidebar.header("Redaction Settings")
    redact_names = st.sidebar.checkbox("Redact Names", value=True)
    redact_emails = st.sidebar.checkbox("Redact Emails", value=True)
    redact_phones = st.sidebar.checkbox("Redact Phone Numbers", value=True)
    redact_companies = st.sidebar.checkbox("Redact Companies", value=True)
    redact_locations = st.sidebar.checkbox("Redact Locations", value=True)

    redaction_config = {
        "names": redact_names,
        "emails": redact_emails,
        "phones": redact_phones,
        "companies": redact_companies,
        "locations": redact_locations
    }


    if ext == "txt":
        text = uploaded_file.read().decode("utf-8")
        redacted_text, summary = mask_text(text, redaction_config)


        st.subheader("🔐 Redacted Text:")
        st.text_area("Result", redacted_text, height=300)

        st.download_button(
            label="📥 Download Redacted TXT",
            data=redacted_text,
            file_name="redacted_text.txt",
            mime="text/plain"
        )

        st.subheader("📊 Redaction Summary:")
        for key, value in summary.items():
            st.markdown(f"**{key.capitalize()}**: {value}")

    elif ext == "csv":
        df = pd.read_csv(uploaded_file)
        summary = {
            "names": 0,
            "emails": 0,
            "phones": 0,
            "companies": 0,
            "locations": 0
        }

        for col in df.columns:
            new_col = []
            for value in df[col]:
                if isinstance(value, str):
                    redacted_value, temp_summary = mask_text(value, redaction_config)
                    new_col.append(redacted_value)
                    for key in summary:
                        summary[key] += temp_summary[key]
                else:
                    new_col.append(value)
            df[col] = new_col

        st.subheader("🔐 Redacted CSV Preview:")
        st.dataframe(df)

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Redacted CSV",
            data=csv_data,
            file_name="redacted_data.csv",
            mime="text/csv"
        )

        st.subheader("📊 Redaction Summary:")
        for key, value in summary.items():
            st.markdown(f"**{key.capitalize()}**: {value}")


