import pandas as pd

# Read the Excel file into a DataFrame
excel_file = "C:\\Users\\yminz\\Downloads\\דוח פיצול מרץ 2024.xlsx"  # Replace with your Excel file path
df = pd.read_excel(excel_file)

# Initialize an empty list to store text
all_text = []

# Iterate through each cell in the DataFrame
for column in df.columns:
    for cell in df[column]:
        # Check if the cell contains text
        if isinstance(cell, str):
            all_text.append(cell)

# Join all the extracted text into a single string
all_text_combined = '\n'.join(all_text)

# Print or use the extracted text as needed
print(all_text_combined)

