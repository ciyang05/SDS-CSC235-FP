import pandas as pd

# merging the enrollment and attendance datasets
attendance = pd.read_excel('2024-2025/24-25 Attendance.xlsx')
enrollment = pd.read_excel('2024-2025/24-25 Enrollment.xlsx')

# find corresponding school code and enrollment then cross match with attendance school codes and add entry to new column
merged = attendance.merge(enrollment[['School Code', 'School_Total', 'COUNTY']], on='School Code', how='left')

merged.to_excel('24-25 merged.xlsx', index=False)

# Weights 

# Define indicators 
indicators = ['Attendance Rate', 'Average # of Absences', 'Chronically Absent (10% or more)']

# Calculated weighted value for each indicator (for each school)
for indicator in indicators:
    merged[f'{indicator}_weighted'] = merged[indicator] * merged['School_Total']

# Calculate weighted averages per county (takes the weights for each school and combines to get the county weight)
# groups all schools together by their county 
county_weighted = merged.groupby('COUNTY').apply(
    # for each county group, run the following calculation
    lambda x : pd.Series({
        # adds up all weighted values for all schools in that county
        # adds up total enrollment of all schools in that county
        # divide these values -> sum of weighted values for all schools / total enrollment of all schools in that county
        indicator: x[f'{indicator}_weighted'].sum() / x['School_Total'].sum()
        for indicator in indicators
    })
).reset_index()

# Saves weighted averages per indicator for each county in a dataset
county_weighted.to_excel('24-25 County_weighted.xlsx', index=False)