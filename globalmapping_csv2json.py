import streamlit as st
import pandas as pd
import json

# --- Page Configuration (Tab title, layout) ---
st.set_page_config(
    page_title="CSV to JSON Mapper",
    page_icon="🔄",
    layout="centered"
)

# --- App Header ---
st.title("🔄 CSV to Store Mapping Converter")
st.markdown("""
    Upload your CSV file, map the columns, and download the formatted JSON.
""")
st.divider()

# --- Step 1: File Upload ---
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load Data
        df = pd.read_csv(uploaded_file)

        st.success("File uploaded successfully!")

        # Show a preview of the data
        with st.expander("👀 Preview CSV Data"):
            st.dataframe(df.head())

        st.divider()

        # --- Step 2: Column Mapping ---
        st.subheader("🛠 Map Your Columns")
        st.caption("Select which columns from your CSV correspond to the required JSON fields.")

        col1, col2 = st.columns(2)

        with col1:
            # Dropdown for Store ID
            store_col = st.selectbox(
                "Select 'Store ID' column:",
                options=df.columns,
                index=0  # Default to first column
            )

        with col2:
            # Dropdown for Global Chain ID
            chain_col = st.selectbox(
                "Select 'Global Chain ID' column:",
                options=df.columns,
                index=1 if len(df.columns) > 1 else 0
            )

        # --- Step 3: Conversion & Download ---
        st.divider()
        st.subheader("📥 Download Result")

        if st.button("Generate JSON"):
            # Create the mapping
            df_mapped = df[[store_col, chain_col]].rename(columns={
                store_col: 'storeId',
                chain_col: 'globalChainId'
            })

            # Convert to list of dicts
            mappings_list = df_mapped.to_dict(orient='records')

            # Create final structure
            final_json = {"mappings": mappings_list}

            # Convert to JSON string
            json_str = json.dumps(final_json, indent=4)

            # Show a snippet of the result
            st.info(f"Generated {len(mappings_list)} mappings.")
            st.code(json.dumps({"mappings": mappings_list[:2]}, indent=4) + "\n...", language='json')

            # Download Button
            st.download_button(
                label="⬇️ Download mappings.json",
                data=json_str,
                file_name="mappings.json",
                mime="application/json",
                type="primary"  # Makes the button stand out
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("👆 Please upload a CSV file to get started.")