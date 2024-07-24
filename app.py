import pandas as pd
import streamlit as st

# Funktion zum Erstellen des gefilterten Excel-Berichts
def create_filtered_report():
    input_file = "Fachdatenmodell DIB.xlsx"
    sheet_name = "Geschäftsobjekte"
    output_file = "ISB_report.xlsx"

    # Excel-Datei laden
    df = pd.read_excel(input_file, sheet_name=sheet_name)

    # Zeilen ab A3 (also ab Index 2) filtern, in denen die Spalte B den Text "Betriebsmittel" enthält
    filtered_df = df.iloc[2:]
    filtered_df = filtered_df[filtered_df['B'].str.contains("Betriebsmittel", na=False)]

    # Neue Excel-Datei speichern mit den gefilterten Daten der Spalte A
    filtered_df[['A']].to_excel(output_file, index=False, header=False)
    return output_file

# Streamlit-Frontend
st.title('Excel Report Generator')

if st.button('Run'):
    report_file = create_filtered_report()
    st.success('Report generated successfully!')

    # Bereitstellung der Datei zum Download
    with open(report_file, "rb") as file:
        btn = st.download_button(
            label="Download Excel report",
            data=file,
            file_name=report_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
