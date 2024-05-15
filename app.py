import streamlit as st
import ifcopenshell
import ifc_utils
import os

# Create directories to save uploaded files if they don't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

if not os.path.exists("cleaned"):
    os.makedirs("cleaned")

# Streamlit app
st.title("IFC File Utilities")

# Upload IFC files
uploaded_files = st.file_uploader("Upload IFC files", type=["ifc"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name}")

# Select action
action = st.selectbox("Select action", ["Clean IFC", "Compare IFCs"])

if action == "Clean IFC":
    uploaded_files = [f for f in os.listdir("uploads") if f.endswith(".ifc")]
    if uploaded_files:
        selected_file = st.selectbox("Select IFC file to clean", uploaded_files)
        if st.button("Clean IFC"):
            cleaned_model = ifc_utils.clean_ifc(os.path.join("uploads", selected_file), printout=True)
            cleaned_file_path = os.path.join("cleaned", f"cleaned_{selected_file}")
            cleaned_model.write(cleaned_file_path)
            st.success(f"Cleaned IFC file saved as {cleaned_file_path}")
            st.download_button(
                label="Download Cleaned IFC",
                data=open(cleaned_file_path, "rb").read(),
                file_name=f"cleaned_{selected_file}"
            )

elif action == "Compare IFCs":
    uploaded_files = [f for f in os.listdir("uploads") if f.endswith(".ifc")]
    if len(uploaded_files) >= 2:
        file1 = st.selectbox("Select first IFC file", uploaded_files)
        file2 = st.selectbox("Select second IFC file", uploaded_files)
        if st.button("Compare IFCs"):
            result = ifc_utils.compare_ifcs(os.path.join("uploads", file1), os.path.join("uploads", file2), printout=True)
            st.write("Comparison Result:")
            st.json(result)
    else:
        st.warning("Please upload at least two IFC files to compare.")

if __name__ == "__main__":
    st.run()
