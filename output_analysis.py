# Remove any duplicate rows in the output csv.
# Output the final csv file with the duplicates removed.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the output csv file
df = pd.read_csv('output.csv')

# Remove any duplicate rows
df.drop_duplicates(inplace=True)

# Output the final csv file
df.to_csv('output.csv', index=False)

print('Duplicates removed successfully!')

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

def abbreviate_if_needed(name):
    words = name.split()
    if len(words) > 1:
        return ''.join(word[0] for word in words)
    else:
        return name

# Apply the function to the 'Treatment Level' column
# Calculate averages only for numeric columns
averages = df.groupby(['Treatment Variable', 'Treatment Level', 'Target Variable'])[numeric_cols].mean().reset_index()
print(averages.columns)
# Display the averages for verification
addepev3_data = averages[averages['Target Variable'] == 'ADDEPEV3']
# Sort the data by 'ATE' column in descending order
addepev3_data = addepev3_data.sort_values('ATE', ascending=False)
addepev3_data['Treatment Level'] = addepev3_data['Treatment Level'].apply(abbreviate_if_needed)

print(addepev3_data)

# Filter data for MENTHLTH
menthlth_data = averages[averages['Target Variable'] == 'MENTHLTH']
# Sort the data by 'ATE' column in descending order
menthlth_data = menthlth_data.sort_values('ATE', ascending=False)
# Abbreviate the 'Treatment Level' column
menthlth_data['Treatment Level'] = menthlth_data['Treatment Level'].apply(abbreviate_if_needed)

print(menthlth_data)

plt.figure(figsize=(12, 6))
plt.errorbar(addepev3_data['Treatment Variable'] + ' ' + addepev3_data['Treatment Level'],
             addepev3_data['ATE'],
             yerr=[addepev3_data['ATE'] - addepev3_data['Lower Bound'], addepev3_data['Upper Bound'] - addepev3_data['ATE']],
             fmt='o', capsize=5)
# Print out each treatment level and its average treatment affect
for i, row in addepev3_data.iterrows():
    print(f"{row['Treatment Variable']} {row['Treatment Level']}: {row['ATE']}")
plt.xticks(rotation=60, ha='right')
plt.xlabel('Treatment Variable and Level')
plt.ylabel('ATE')
plt.title('Average ATE for ADDEPEV3')
plt.tight_layout()  # Adjust layout to make room for elements
plt.savefig('average_ate_addepev3.png')
plt.show()

plt.figure(figsize=(10, 6))
plt.errorbar(menthlth_data['Treatment Variable'] + ' ' + menthlth_data['Treatment Level'],
             menthlth_data['ATE'],
             yerr=[menthlth_data['ATE'] - menthlth_data['Lower Bound'], menthlth_data['Upper Bound'] - menthlth_data['ATE']],
             fmt='o', capsize=5)
for i, row in menthlth_data.iterrows():
    print(f"{row['Treatment Variable']} {row['Treatment Level']}: {row['ATE']}")
plt.xticks(rotation=60, ha='right')
plt.xlabel('Treatment Variable and Level')
plt.ylabel('ATE')
plt.title('Average ATE for MENTHLTH')
plt.tight_layout()  # Adjust layout here as well
plt.savefig('average_ate_menthlth.png')
plt.show()



# Variable names
variable_names = ['GENHLTH', 'MARITAL', '_SEX', 'MENTHLTH', '_EDUCAG',
                  '_INCOMG1', 'POORHLTH', 'ADDEPEV3', '_AGEG5YR', '_AGE65YR', '_AGE80',
                  '_AGE_G', 'DECIDE', 'DIFFALON', 'ACEDEPRS', 'ACEDRINK', 'ACEDRUGS',
                  'ACEPRISN', 'ACEDIVRC', 'ACEPUNCH', 'ACEHURT1', 'ACESWEAR', 'ACETOUCH',
                  'ACETTHEM', 'ACEHVSEX']
labels = [
    "General Health",
    "Marital Status",
    "Calculated sex variable",
    "Number of Days Mental Health Not Good",
    "Computed level of education completed categories",
    "Computed income categories",
    "Poor Physical or Mental Health",
    "(Ever told) you had a depressive disorder",
    "Reported age in five-year age categories calculated variable",
    "Reported age in two age groups calculated variable",
    "Imputed Age value collapsed above 80",
    "Imputed age in six groups",
    "Difficulty Concentrating or Remembering",
    "Difficulty Doing Errands Alone",
    "Live With Anyone Depressed, Mentally Ill, Or Suicidal?",
    "Live With a Problem Drinker/Alcoholic?",
    "Live With Anyone Who Used Illegal Drugs or Abused Prescriptions?",
    "Live With Anyone Who Served Time in Prison or Jail?",
    "Were Your Parents Divorced/Separated?",
    "How Often Did Your Parents Beat Each Other Up?",
    "How Often Did A Parent Physically Hurt You In Any Way?",
    "How Often Did A Parent Swear At You?",
    "How Often Did Anyone Ever Touch You Sexually?",
    "How Often Did Anyone Make You Touch Them Sexually?",
    "How Often Did Anyone Ever Force You to Have Sex?"
]
print(len(variable_names))
print(len(labels))

fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('tight')
ax.axis('off')

# Sort the table data alphabetically by variable_name
sorted_data = sorted(zip(variable_names, labels), key=lambda x: x[0])
table_data = [["Variable Name", "Label"]] + sorted_data

# Adjust column widths here. Increase or decrease the values as needed.
# The values in the list represent the width of each column.
# For example, setting to [0.2, 0.4] makes the first column narrower than the second.
colWidths = [0.2, 0.6]

table = ax.table(cellText=table_data, loc='center', cellLoc='left', colWidths=colWidths)

# Alternate row colors
colors = ["#F5F5F5", "#FFFFFF"]  # Light grey and white for alternating rows
for i, row in enumerate(table.get_celld().values()):
    row.set_facecolor(colors[i % 2])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

plt.show()

# Save the table as a PNG image
fig.savefig('variable_names_labels.png')