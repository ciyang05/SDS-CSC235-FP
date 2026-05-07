# CSC235: FP README
**Names:** Chiashi Yang, Victoria Reyes Borges, Kiara Sunil Singh, Jingyuan Zhou

Link to final dashboard : https://public.tableau.com/views/FPdraft1_17775286078000/FinalDashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link 

## Purpose:
The purpose of the VA system is to highlight the importance of school absence as an important risk factor for youth outcomes in the region. It serves to inform policy makers, school districts, and youth serving organizations about this topic.
How to use the system:

## How To Use The System

**Overall Averages of Indicators by School Year (line chart):**
Users can hover on a line and see the indicator, school year, and overall average. 

**Chronic Absences (%) By School Year (line chart):** 
Users can hover and see school year, county and the corresponding value for chronically absent (10% or more).  

**Attendance Rate (%) By School Year (line chart):**
Users can hover and see school year, county and the corresponding attendance rate.

**Average number of Absences by School Year (line chart):**
Users can hover and see school year, county, and the corresponding average number of absences. 

**Indicator Data by County (24-25) (map):**
Users can hover and see county and indicator value. In addition, users can click on the drag down option on the right-hand side and choose an indicator.
When hovering over a point in any of the separate indicator line charts or the map, points that correspond to the county and school year in the other 3 charts (aside from overall averages) are also displayed.


## Any known bugs:
N/A

## Data Cleaning/Analysis:

### Cleaning the Data:
1) Read from a list of schools to include (the schools in the selected counties)
2) Loop through rows to actually find the one that contains column names
    - Look for rows containing “School” and “Include”
3) Clean it as a proper table 
4) Extract included school codes
    - Filter rows where the “Include” column says “Include”
    - Get the school codes
    - Clean them and store them
5) Map each year to attendance and enrollment file
    - For each year, make a folder if it doesn't exist
6) Process attendance data
    - Load raw file
    - Clean format
    - Filter school codes
7) Process enrollment data
    - Load raw file
    - Clean format
    - Filter included schools
8) Save clean dataset into organized folders


### Data Analysis: 
**Weighting the Dataset**
1) Create a copy of the cleaned datasets, label the copy “Datasets w/Weights”
    - Datasets are separated by year.
2) Create a Python script within each folder to weight the population size of each school for corresponding county
    - First, crossmatch the school codes in the attendance and enrollment files to create a new file called “year-year merged.” This contains attendance information, school codes/names, counties, and enrollment values. 
	Calculating Indicator Weighted Values for Each County
    - For each school in the county, multiply each absenteeism indicator by the enrollment
    - Sum the corresponding indicator product within each county
        eg. sum the product of the attendance values 
    - Divide the indicator sum by total enrollment of all schools in the county, giving the weighted average for each indicator
3) Run the script. This will create two new files, a merged file and a file with the weighted indicator averages for each county. 
4) Create a new spreadsheet with aggregated values for each county across all indicators and years.
    - Edited the values to have only 1 decimal place
    - Stored in same folder, “Datasets w/Weights”

**Computing and Formatting Data for Overall Averages Visualization**
1) Done on the Overall Avgs. sheet 
    - Columns H, I, J, K, L from the Weights sheet
    - New columns created to help find the sum of each indicator in a school year: Attendance Weights (M), Average # Absences Weights (N), Chronically Absent Weights (O) 
2) For each indicator,
    - Take the proportion of each county within that school year and multiply it by the corresponding indicator value. This gives the weighted average for the county. 
        - Example formula to find weighted average for Berkshire county in 2017-2018 for Attendance Rate indicator: =(J2/SUM(J2:J6))*J2
3) After calculating all weighted averages, summed all the values within a school year for each indicator. This gives: Overall Average Attendance, Overall Average # of Absences, Overall Average Chronically Absent (10% or more)
4) In order to present the indicators on one visualization, must convert the data into a format that Tableau can easily read.
    - Must unpviot the overall average columns (so indicators are categorized by year together, allowing for a visualization of all indicators) using the Power Query tool in Excel. 
    - Upon clicking the Power Query tool, pick the three indicator columns. Do not include school year.
    - Select the Unpivot Columns option. This reformats the data, turning columns into rows. 
    - This creates a new sheet with the reformatted overall averages and is ready to use.


## Visualizations

Font Used: Oriya MN

### Overall Averages of Indicators by School Year Visualization
1) Join the sheet with the table from the Power Query “Overall Avgs Vis” to the Aggregated Data sheet using “School Year” as the connection. 
2) On the data tab, choose School Year and Overall Average from the Overall Avgs Vis dataset.
    - School Year in columns 
    - Overall Average in rows as a SUM and continuous 
3) In the marks tab, make sure the marks is set as “Line.”
4) Drag the “Indicators” variables from Overall Avgs Vis to the Color option on the marks tab. This will ensure the 3 different indicators are their own color. 
    - Change the color palette to “Colorblind Palette.”
The line graph should automatically appear upon adding variables. 

### Indicator Data by County Visualization
1) Join the sheet “County Map Data (24-25)” to Aggregated Data sheet using “County” as the connection. 
    - County Map Data (24-25) has the indicator data for each county in the school year 2024-2025.
2) Join the COUNTIESSURVEY_POLYM.shp file (shape file to get the outline of the 5 counties) to Aggregated Data using “County” as the connection. 
3) Drag “Latitude (generated)” to rows and “Longitude (generated)” to columns.
    - If the map doesn’t automatically show, change the mark to “Map.”
4) Create a parameter w/name “Indicator.” This will appear as a drag down option on the right hand side of the visualization and will allow the user to choose which indicator to display. 
    - Set data type to string. 
    - Have allowable values be set to list. 
    - In the “Value” column, add the three indicators: Attendance Rate (%), Average Absences, Chronic Absences (%). 
    - Ensure the option on the right of this table is set to fixed. 
5) Create a calculated field w/name “Value.” This will ensure that when a user picks an indicator, the correct indicator data will show. Use the following formula: 
    - IF [Indicator] = "Attendance Rate (%)" THEN [Attendance (County Map Data (24-25))]
    ELSEIF [Indicator] = "Average Absences" THEN [Average # of Absences (County Map Data (24-25))]
    ELSEIF [Indicator] = "Chronic Absences (%)" THEN [Chronically Absent (10% or more) (County Map Data (24-25))]
    END
    - Ensure that the name following “[Indicator] =” matches w/the corresponding name in the parameter and the name following “THEN” matches w/the corresponding variable in the County Map Data (24-25) dataset. 
6) From the COUNTIESSURVEY_POLYM.shp data, drag the “Geometry” variable to detail on the marks tab. 
7) Drag “County” variable from Aggregated Data to color and set it as Dimension. This will color coordinate the 5 counties. 
    - Set colors to be “Colorblind Palette.”
8) Drag the calculated field “Value” (should be a part of County Map Data (24-25)) to detail. Set it as SUM and continuous. 
9) Drag “Value” to Label on the marks tab. Again, set it as SUM and continuous. This will add the correct labels to the map. 
    - If labels are overlapping with county outlines, drag labels to center of corresponding county.
10) Drag “County” from Aggregated Data to the filter tab and set it as Dimension. This will give a legend for the map. 

### Computing and Formatting Average by County and Year Line Charts
1) Used the “Years Updated” field as the column dimension in Tableau. 
    - Ensure that “Years Updated” has a string property 
2)  Drag correct x-axis variable to the row dimension
    - When measuring Chronic Absences use “Chronically Absent (10 or more days)”
    - When measuring Average Absences use “Average # of Absences”
    - When measuring Average Attendance use “Attendance”
3) Convert all row dimensions to “Measure (Sum)” once placed in the row dimension area in Tableau 
4) Added three separate text boxes to indicate “Pre-Covid”, “Covid”, and “Post-Covid” years. Also used a textbox to provide a slight grayed out background for the Covid years.
