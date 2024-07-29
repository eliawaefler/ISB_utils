import pandas as pd
import streamlit as st
import sys
import os
import pandas as pd
import openpyxl
import requests

def download_datamodel(debug=False):
    """
    https://www.myserver.com/api/test/schemes/MyModel/download?format=XLSX
    #?format=SQL&targetDatabase=SQLServer
    Metadata Upload/Download | dataspot. Software Handbuch
    curl -X GET -u <user>:<password> "https://www.myserver.com/api/test/schemes/MyModel/download?xsl=<report>"
    """
    path = "\\\\filer300\\USERS3004\\I0340828\\Desktop\\p_LAKEHUB\\prüfprozess_pyhton_lakehub"

    # Replace these with your actual username and password
    username = st.secrets("USERNAME")
    password = st.secrets("PW")
    url = 'https://www.insel.dataspot.com/api/test/schemes/Kataloge/download?format=XLSX'
    url = "https://www.myserver.com/api/test/schemes/MyModel/download?format=XLSX"
    url = "https://insel.dataspot.io/api/test/schemes/MyModel/download?format=XLSX"
    url = "https://insel.dataspot.io/api/test/schemes/Kataloge/download?format=XLSX"
    url = "https://www.google.ch"
    response = requests.get(url)

    if response.status_code == 200:
        st.success("google")
    else:
        st.error("no internet")

# Funktion zum Erstellen des gefilterten Excel-Berichts
def create_filtered_report():
    input_file = "Fachdatenmodell DIB.xlsx"
    sheet_name = "Geschäftsobjekte"
    output_file = "ISB_report.xlsx"

    # Excel-Datei laden
    df = pd.read_excel(input_file, sheet_name=sheet_name)

    # Zeilen ab A3 (also ab (ohne) Index 1) filtern, in denen die Spalte B den Text "Betriebsmittel" enthält
    filtered_df = df.iloc[1:]
    filtered_df = filtered_df[filtered_df.iloc[:, 1].str.contains("Betriebsmittel", na=False)]
    
    # Neue Excel-Datei speichern mit den gefilterten Daten der Spalte A
    filtered_df.iloc[:, [0]].to_excel(output_file, index=False, header=False)  # Annahme, dass die erste Spalte A ist
    return output_file

def create_config():
    input_file = "Kataloge DIB.xlsx"
    sheet_name = "Referenzwerte"
    output_file = "config.xlsx"

    # Excel-Datei laden
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    # Extract entries from cells A3 to A100 and B3 to B100
    A_values = df['A'][2:100].tolist()
    B_values = df['B'][2:100].tolist()
    
    # Create a dictionary to hold the unique A values and corresponding B values
    data_dict = {}
    for a, b in zip(A_values, B_values):
        if a in data_dict:
            data_dict[a].append(b)
        else:
            data_dict[a] = [b]
    
    # Create a new DataFrame to store the transformed data
    new_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))
    return new_df.to_excel(output_file, index=False, header=False)



# Streamlit-Frontend
st.title('Excel Report Generator')

if st.button('Run'):
    report_file = create_filtered_report()
    st.success('Report generated successfully!')

    # Bereitstellung der Datei zum Download
    with open(report_file, "rb") as file:
        st.download_button(
            label="Download Excel report",
            data=file,
            file_name=report_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
if st.button('Config'):
    report_file = create_config()
    st.success('config generated successfully!')

    # Bereitstellung der Datei zum Download
    with open(report_file, "rb") as file:
        st.download_button(
            label="Download Excel report",
            data=file,
            file_name=report_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
if st.button("download datamodell"):
    download_datamodel(debug=False)
