import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Claim Scrubber", layout="wide")

st.title("🧾 Pre-Submission Claim Scrubber & Dashboard")

# --- Demo Data ---
demo_csv = """patient_id,dob,insurance_id,cpt_code,icd10_code
1,1990-01-01,INS123,99213,J06.9
2,,INS456,99999,J00
3,1985-05-05,,99213,
4,01/2/23,INS789,99214,J06.9
5,1992-07-07,INS111,93000,R05
"""

# --- Buttons ---
col1, col2 = st.columns(2)

uploaded_file = col1.file_uploader("📂 Upload Claims CSV", type=["csv"])
use_demo = col2.button("⚡ Use Demo Data")

# --- Load Data ---
df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    elif use_demo:
        df = pd.read_csv(StringIO(demo_csv))

        # --- If Data Exists ---
        if df is not None:

            st.subheader("📄 Raw Data")
                st.dataframe(df)

                    df_clean = df.copy()
                        error_list = []
                            risk = []

                                # Sample valid codes
                                    valid_icd = ["J06.9", "R05", "J00"]
                                        valid_cpt = ["99213", "99214", "93000"]

                                            for index, row in df.iterrows():
                                                    row_errors = []

                                                            # Missing checks
                                                                    if pd.isna(row.get("patient_id")):
                                                                                row_errors.append("Missing Patient ID")
                                                                                        if pd.isna(row.get("dob")):
                                                                                                    row_errors.append("Missing DOB")
                                                                                                            if pd.isna(row.get("insurance_id")):
                                                                                                                        row_errors.append("Missing Insurance ID")

                                                                                                                                # DOB cleaning
                                                                                                                                        try:
                                                                                                                                                    df_clean.at[index, "dob"] = pd.to_datetime(row["dob"]).strftime("%Y-%m-%d")
                                                                                                                                                            except:
                                                                                                                                                                        row_errors.append("Invalid DOB Format")

                                                                                                                                                                                # Code validation
                                                                                                                                                                                        if row.get("icd10_code") not in valid_icd:
                                                                                                                                                                                                    row_errors.append("Invalid ICD-10")

                                                                                                                                                                                                            if row.get("cpt_code") not in valid_cpt:
                                                                                                                                                                                                                        row_errors.append("Invalid CPT")

                                                                                                                                                                                                                                # Risk flag
                                                                                                                                                                                                                                        if len(row_errors) > 0:
                                                                                                                                                                                                                                                    risk.append("High")
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                        risk.append("Low")

                                                                                                                                                                                                                                                                                error_list.append(", ".join(row_errors) if row_errors else "No Error")

                                                                                                                                                                                                                                                                                    df["Errors"] = error_list
                                                                                                                                                                                                                                                                                        df["Risk"] = risk

                                                                                                                                                                                                                                                                                            # --- Validation Output ---
                                                                                                                                                                                                                                                                                                st.subheader("🔍 Validation Results")
                                                                                                                                                                                                                                                                                                    st.dataframe(df)

                                                                                                                                                                                                                                                                                                        # --- Dashboard ---
                                                                                                                                                                                                                                                                                                            st.subheader("📊 Dashboard")

                                                                                                                                                                                                                                                                                                                total_claims = len(df)
                                                                                                                                                                                                                                                                                                                    total_errors = sum(df["Errors"] != "No Error")
                                                                                                                                                                                                                                                                                                                        clean_claims = total_claims - total_errors

                                                                                                                                                                                                                                                                                                                            error_types = df["Errors"].str.split(", ").explode()
                                                                                                                                                                                                                                                                                                                                top_error = error_types.value_counts().idxmax() if not error_types.empty else "None"

                                                                                                                                                                                                                                                                                                                                    col1, col2, col3, col4 = st.columns(4)

                                                                                                                                                                                                                                                                                                                                        col1.metric("Total Claims", total_claims)
                                                                                                                                                                                                                                                                                                                                            col2.metric("Total Errors", total_errors)
                                                                                                                                                                                                                                                                                                                                                col3.metric("Clean Claims %", f"{(clean_claims/total_claims)*100:.1f}%")
                                                                                                                                                                                                                                                                                                                                                    col4.metric("Top Error", top_error)

                                                                                                                                                                                                                                                                                                                                                        # --- Download ---
                                                                                                                                                                                                                                                                                                                                                            st.subheader("📥 Download Cleaned Data")
                                                                                                                                                                                                                                                                                                                                                                csv = df_clean.to_csv(index=False).encode('utf-8')
                                                                                                                                                                                                                                                                                                                                                                    st.download_button("Download Clean CSV", csv, "cleaned_claims.csv", "text/csv")

                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                        st.info("👆 Upload a file or click 'Use Demo Data' to start.")