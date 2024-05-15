import streamlit as st
from ifc_utils import *


def main():
    st.title('IFC File Cleaner')
    uploaded_file = st.file_uploader("Upload an IFC file", type=['ifc'])
    
    if uploaded_file is not None:
        # Save the uploaded file locally
        with open("uploaded.ifc", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Clean the IFC file
        cleaned_ifc = clean_ifc("uploaded.ifc")
        
        # Save the cleaned IFC file locally
        cleaned_ifc.write("cleaned.ifc")
        
        # Provide a download link for the cleaned IFC file
        with open("cleaned.ifc", "rb") as f:
            st.download_button("Download Cleaned IFC", f, file_name="cleaned.ifc")

if __name__ == "__main__":
    main()
