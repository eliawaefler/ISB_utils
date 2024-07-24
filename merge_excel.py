import pandas as pd

# Excel-Datei und Blattnamen festlegen
input_file = "Fachdatenmodell DIB.xlsx"
sheet_name = "Geschäftsobjekte"

# Excel-Datei laden
df = pd.read_excel(input_file, sheet_name=sheet_name, engine='xlrd')

# Zeilen ab A3 (also ab Index 2) filtern, in denen die Spalte B den Text "Betriebsmittel" enthält
filtered_df = df.iloc[2:]
filtered_df = filtered_df[filtered_df['B'].str.contains("Betriebsmittel", na=False)]

# Neue Excel-Datei speichern mit den gefilterten Daten der Spalte A
output_file = "ISB_report.xlsx"
filtered_df[['A']].to_excel(output_file, index=False, header=False)

print(f"Die gefilterten Daten wurden in {output_file} gespeichert.")
