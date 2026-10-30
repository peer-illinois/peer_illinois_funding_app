# Get basic statistics for year-to-year report

# NOTE: IN PROGRESS (10/10/2026)

import pandas as pd
from datetime import datetime as dt

# set today's date
today = dt.today().strftime("%Y-%m-%d")

# set file paths
shared_folder = r"C:\Users\cdpou\Documents\Projects"
data_file_path = rf"{shared_folder}\peer_app_data"
file_path = rf"{data_file_path}"

# save path
app_path = rf"{shared_folder}\peer_illinois_funding_app"

# read in data
df_26 = pd.read_parquet(rf"{app_path}\app_data_wide_fy2026.parquet")
df_27 = pd.read_parquet(rf"{app_path}\app_data_wide_fy2027.parquet")

# print shape of the dataframes

print(len(df_26))
print(len(df_27))
print(df_26.shape)
print(df_27.shape)

# read in report "General" (rcg) and "Finance" (rcf) for 2025
irc_file_25 = pd.ExcelFile(rf"{shared_folder}\peer_app_data\raw\2025-Report-Card-Public-Data-Set.xlsx")
df_rcg_25 = pd.read_excel(rf"{file_path}\raw\2025-Report-Card-Public-Data-Set.xlsx", sheet_name = "General")
df_rcf_25 = pd.read_excel(rf"{file_path}\raw\2025-Report-Card-Public-Data-Set.xlsx", sheet_name = "Finance")

# filter for districts 
df_rcg_25_district = df_rcg_25[df_rcg_25["Level"]=="District"]
df_rcf_25_district = df_rcf_25[df_rcf_25["Level"]=="District"]

# filter for state

df_rcg_25_state = df_rcg_25[df_rcg_25["Level"]=="Statewide"]
df_rcf_25_state = df_rcf_25[df_rcf_25["Level"]=="Statewide"]

# fill df_rcf_state and df_rcg_state missing values with -999999

df_rcf_25_state = df_rcf_25_state.fillna(-999999)
df_rcg_25_state = df_rcg_25_state.fillna(-999999)

print(df_rcg_25.columns)

# keep necessary columns

df_rcg_25_district = df_rcg_25_district[["RCDTS","# Student Enrollment","# Student Enrollment - White","# Student Enrollment - Black or African American", "# Student Enrollment - Hispanic or Latino","# Student Enrollment - Asian","# Student Enrollment - Native Hawaiian or Other Pacific Islander","# Student Enrollment - American Indian or Alaska Native","# Student Enrollment - IEP","# Student Enrollment - EL","# Student Enrollment - Former EL","# Student Enrollment - Never EL","# Student Enrollment - Low Income","# Student Enrollment - Homeless"]]
df_rcf_25_district = df_rcf_25_district[["RCDTS","District","EBF Tier","% EBF Capacity to Meet Expectations","$ Total Per-Pupil Expenditures - State/Local","$ Local Property Taxes","% Local Property Taxes","$ Other Local Funding","% Other Local Funding","$ Evidence-Based Funding","% Evidence-Based Funding","$ Other State Funding","% Other State Funding","$ Federal Funding","% Federal Funding","$ Total Revenue Source","$ EAV per Pupil","$ Total School Tax Rate per $100","$ Instructional Expenditure per Pupil"]]

# keep necessary columns for state

df_rcg_25_state = df_rcg_25_state[["RCDTS","# Student Enrollment","# Student Enrollment - White","# Student Enrollment - Black or African American", "# Student Enrollment - Hispanic or Latino","# Student Enrollment - Asian","# Student Enrollment - Native Hawaiian or Other Pacific Islander","# Student Enrollment - American Indian or Alaska Native","# Student Enrollment - IEP","# Student Enrollment - EL","# Student Enrollment - Former EL","# Student Enrollment - Never EL","# Student Enrollment - Low Income","# Student Enrollment - Homeless"]]
df_rcf_25_state = df_rcf_25_state[["RCDTS","District","EBF Tier","% EBF Capacity to Meet Expectations","$ Total Per-Pupil Expenditures - State/Local","$ Local Property Taxes","% Local Property Taxes","$ Other Local Funding","% Other Local Funding","$ Evidence-Based Funding","% Evidence-Based Funding","$ Other State Funding","% Other State Funding","$ Federal Funding","% Federal Funding","$ Total Revenue Source","$ EAV per Pupil","$ Total School Tax Rate per $100","$ Instructional Expenditure per Pupil"]]

print(df_rcg_25_district.columns)
print(df_rcf_25_district.columns)
print(df_rcf_25_district.shape)
print(df_rcg_25_district.shape)

# merge Report Card data

df_irc_25_district = df_rcf_25_district.merge(df_rcg_25_district,on="RCDTS",how="outer")
df_irc_25_state = df_rcf_25_state.merge(df_rcg_25_state,on="RCDTS",how="outer")

print(df_irc_25_district.columns)
print(df_irc_25_district.shape)
print(df_irc_25_state.columns)
print(df_irc_25_state.shape)


# Column creating funding level categories: 50-60%, 60-70, 70-80, and so on up to 357.1

df_irc_25_district['adequacy_level_category'] = pd.cut(df_irc_25_district['% EBF Capacity to Meet Expectations'], bins=[50, 60, 70, 80, 90, 100,400], labels=['50-60%', '60-70%', '70-80%', '80-90%', '90-100%', '100%+'])

df_irc_25_district.columns

# create a list of columns that start with #

demographic_columns = [col for col in df_irc_25_district.columns if col.startswith("# Student Enrollment")]

print(demographic_columns)

print(df_irc_25_district.dtypes)

# group by adequacy_level_category and count 

df = df_irc_25_district.groupby('adequacy_level_category').size()
#print(df.columns)
df.columns = ['adequacy_level_category', 'district_count']

df_dem_25 = df_irc_25_district.copy()

# replace "*" with None

df_dem_25 = df_dem_25.replace("*", None)

df_dem_25[demographic_columns] = df_dem_25[demographic_columns].apply(pd.to_numeric, errors='coerce')

df_dem_25 = df_dem_25.groupby('adequacy_level_category').agg({
    'adequacy_level_category':'count',    
    '$ Total Per-Pupil Expenditures - State/Local':'mean',
    '$ Local Property Taxes':'sum',
    '% Local Property Taxes':'mean',
    '$ Other Local Funding':'sum',
    '% Other Local Funding':'mean',
    '$ Evidence-Based Funding':'sum',
    '% Evidence-Based Funding':'mean',
    '$ Other State Funding':'sum',
    '% Other State Funding':'mean',
    '$ Federal Funding':'mean',
    '% Federal Funding':'mean',
    '$ Total Revenue Source':'mean',
    '$ EAV per Pupil':'mean',
    '$ Total School Tax Rate per $100':'mean',
    '$ Instructional Expenditure per Pupil':'mean',
    '# Student Enrollment':'sum',
    '# Student Enrollment - White':'sum',
    '# Student Enrollment - Black or African American':'sum',
    '# Student Enrollment - Hispanic or Latino':'sum',
    '# Student Enrollment - Asian':'sum',
    '# Student Enrollment - Native Hawaiian or Other Pacific Islander':'sum',
    '# Student Enrollment - American Indian or Alaska Native':'sum',
    '# Student Enrollment - IEP':'sum',
    '# Student Enrollment - EL':'sum',
    '# Student Enrollment - Former EL':'sum',
    '# Student Enrollment - Never EL':'sum',
    '# Student Enrollment - Low Income':'sum',
    '# Student Enrollment - Homeless':'sum'
})

df_dem_25 = df_dem_25.rename(columns={'adequacy_level_category': 'district_count'})

df_dem_25.reset_index(inplace=True)

# remove RCDTS, District, EBF Tier from df_irc_25_state
df_irc_25_state = df_irc_25_state.drop(columns=["RCDTS", "District", "EBF Tier"])
df_irc_25_state['adequacy_level_category'] = "State of Illinois"

for col in df_irc_25_state.columns:
    if col in df_dem_25.columns:
        print(f"{col} IS FOUND in df_dem_25")
        # replace df_dem_25 col with df_irc_25_state col
    else:
        print(f"{col} ***IS NOT*** FOUND in df_dem_25")

print(len(df_dem_25.columns))
print(len(df_irc_25_state.columns))

print(df_dem_25.dtypes)
print(df_irc_25_state.dtypes)

df_dem_25['$ Total Per-Pupil Expenditures - State/Local'] = df_dem_25['$ Total Per-Pupil Expenditures - State/Local'].astype(float)
df_dem_25['$ Local Property Taxes'] = df_dem_25['$ Local Property Taxes'].astype(float)
df_dem_25['% Local Property Taxes'] = df_dem_25['% Local Property Taxes'].astype(float)
df_dem_25['$ Other Local Funding'] = df_dem_25['$ Other Local Funding'].astype(float)
df_dem_25['% Other Local Funding'] = df_dem_25['% Other Local Funding'].astype(float)
df_dem_25['$ Evidence-Based Funding'] = df_dem_25['$ Evidence-Based Funding'].astype(float)
df_dem_25['% Evidence-Based Funding'] = df_dem_25['% Evidence-Based Funding'].astype(float)
df_dem_25['$ Other State Funding'] = df_dem_25['$ Other State Funding'].astype(float)
df_dem_25['% Other State Funding'] = df_dem_25['% Other State Funding'].astype(float)
df_dem_25['$ Federal Funding'] = df_dem_25['$ Federal Funding'].astype(float)
df_dem_25['% Federal Funding'] = df_dem_25['% Federal Funding'].astype(float)
df_dem_25['$ Total Revenue Source'] = df_dem_25['$ Total Revenue Source'].astype(float)
df_dem_25['$ EAV per Pupil'] = df_dem_25['$ EAV per Pupil'].astype(float)
df_dem_25['$ Total School Tax Rate per $100'] = df_dem_25['$ Total School Tax Rate per $100'].astype(float)
df_dem_25['$ Instructional Expenditure per Pupil'] = df_dem_25['$ Instructional Expenditure per Pupil'].astype(float)
df_dem_25['# Student Enrollment'] = df_dem_25['# Student Enrollment'].astype(float)
df_dem_25['# Student Enrollment - White'] = df_dem_25['# Student Enrollment - White'].astype(float)
df_dem_25['# Student Enrollment - Black or African American'] = df_dem_25['# Student Enrollment - Black or African American'].astype(float)
df_dem_25['# Student Enrollment - Hispanic or Latino'] = df_dem_25['# Student Enrollment - Hispanic or Latino'].astype(float)
df_dem_25['# Student Enrollment - Asian'] = df_dem_25['# Student Enrollment - Asian'].astype(float)
df_dem_25['# Student Enrollment - Native Hawaiian or Other Pacific Islander'] = df_dem_25['# Student Enrollment - Native Hawaiian or Other Pacific Islander'].astype(float)
df_dem_25['# Student Enrollment - American Indian or Alaska Native'] = df_dem_25['# Student Enrollment - American Indian or Alaska Native'].astype(float)
df_dem_25['# Student Enrollment - IEP'] = df_dem_25['# Student Enrollment - IEP'].astype(float)
df_dem_25['# Student Enrollment - EL'] = df_dem_25['# Student Enrollment - EL'].astype(float)
df_dem_25['# Student Enrollment - Former EL'] = df_dem_25['# Student Enrollment - Former EL'].astype(float)
df_dem_25['# Student Enrollment - Never EL'] = df_dem_25['# Student Enrollment - Never EL'].astype(float)
df_dem_25['# Student Enrollment - Low Income'] = df_dem_25['# Student Enrollment - Low Income'].astype(float)
df_dem_25['# Student Enrollment - Homeless'] = df_dem_25['# Student Enrollment - Homeless'].astype(float)


df_irc_25_state['% EBF Capacity to Meet Expectations']=df_irc_25_state['% EBF Capacity to Meet Expectations'].astype(float)
df_irc_25_state['$ Total Per-Pupil Expenditures - State/Local'] = df_irc_25_state['$ Total Per-Pupil Expenditures - State/Local'].astype(float)
df_irc_25_state['$ Local Property Taxes'] = df_irc_25_state['$ Local Property Taxes'].astype(float)
df_irc_25_state['% Local Property Taxes'] = df_irc_25_state['% Local Property Taxes'].astype(float)
df_irc_25_state['$ Other Local Funding'] = df_irc_25_state['$ Other Local Funding'].astype(float)
df_irc_25_state['% Other Local Funding'] = df_irc_25_state['% Other Local Funding'].astype(float)
df_irc_25_state['$ Evidence-Based Funding'] = df_irc_25_state['$ Evidence-Based Funding'].astype(float)
df_irc_25_state['% Evidence-Based Funding'] = df_irc_25_state['% Evidence-Based Funding'].astype(float)
df_irc_25_state['$ Other State Funding'] = df_irc_25_state['$ Other State Funding'].astype(float)
df_irc_25_state['% Other State Funding'] = df_irc_25_state['% Other State Funding'].astype(float)
df_irc_25_state['$ Federal Funding'] = df_irc_25_state['$ Federal Funding'].astype(float)
df_irc_25_state['% Federal Funding'] = df_irc_25_state['% Federal Funding'].astype(float)
df_irc_25_state['$ Total Revenue Source'] = df_irc_25_state['$ Total Revenue Source'].astype(float)
df_irc_25_state['$ EAV per Pupil'] = df_irc_25_state['$ EAV per Pupil'].astype(float)
df_irc_25_state['$ Total School Tax Rate per $100'] = df_irc_25_state['$ Total School Tax Rate per $100'].astype(float)
df_irc_25_state['$ Instructional Expenditure per Pupil'] = df_irc_25_state['$ Instructional Expenditure per Pupil'].astype(float)
df_irc_25_state['# Student Enrollment'] = df_irc_25_state['# Student Enrollment'].astype(float)
df_irc_25_state['# Student Enrollment - White'] = df_irc_25_state['# Student Enrollment - White'].astype(float)
df_irc_25_state['# Student Enrollment - Black or African American'] = df_irc_25_state['# Student Enrollment - Black or African American'].astype(float)
df_irc_25_state['# Student Enrollment - Hispanic or Latino'] = df_irc_25_state['# Student Enrollment - Hispanic or Latino'].astype(float)
df_irc_25_state['# Student Enrollment - Asian'] = df_irc_25_state['# Student Enrollment - Asian'].astype(float)
df_irc_25_state['# Student Enrollment - Native Hawaiian or Other Pacific Islander'] = df_irc_25_state['# Student Enrollment - Native Hawaiian or Other Pacific Islander'].astype(float)
df_irc_25_state['# Student Enrollment - American Indian or Alaska Native'] = df_irc_25_state['# Student Enrollment - American Indian or Alaska Native'].astype(float)
df_irc_25_state['# Student Enrollment - IEP'] = df_irc_25_state['# Student Enrollment - IEP'].astype(float)
df_irc_25_state['# Student Enrollment - EL'] = df_irc_25_state['# Student Enrollment - EL'].astype(float)
df_irc_25_state['# Student Enrollment - Former EL'] = df_irc_25_state['# Student Enrollment - Former EL'].astype(float)
df_irc_25_state['# Student Enrollment - Never EL'] = df_irc_25_state['# Student Enrollment - Never EL'].astype(float)
df_irc_25_state['# Student Enrollment - Low Income'] = df_irc_25_state['# Student Enrollment - Low Income'].astype(float)
df_irc_25_state['# Student Enrollment - Homeless'] = df_irc_25_state['# Student Enrollment - Homeless'].astype(float)

df_concat = pd.concat([df_irc_25_state, df_dem_25], axis=0)

df_irc_25_state.head()
df_dem_25.head()

# remove "# Student Enrollment" from demographic_columns
#demographic_columns_no_total = [col for col in demographic_columns if col != "# Student Enrollment"]

print(df_dem_25.columns)

# divide each item in demographic_columns_no_total by # Student Enrollment
# replace # in col with %
for col in demographic_columns:
    # add (within group) to the end of the column name
    col_per_within_group = col.replace("#", "%") + " (within group)"
    col_per_total_students = col.replace("#", "%") + " (of total students)"
    df_dem_25[col_per_within_group] = (df_dem_25[col] / df_dem_25[col].sum()) * 100
    df_dem_25[col_per_total_students] = (df_dem_25[col] / df_dem_25['# Student Enrollment'].sum()) * 100

# Transpose the table
df_dem_25_transposed = df_dem_25.transpose().reset_index()


#irc_file_26 = pd.ExcelFile(rf"{shared_folder}\peer_app_data\raw\####.xlsx")



# merge df
df = pd.merge(df_26, df_27, on="RCDTS", suffixes=("_fy2026", "_fy2027"))

# compare district count with IRC
# compare EBF adquacy level with IRC

# stats - 2027 and 2026.
# state: total adequacy need, resources, gap, adequacy level. total student race, low income, iep, el.
# sum: students below adequacy level, race, low-income, iep, and el.
# geography of adequacy - how to make an "accurate" map.
# notes: why we use below 100%. caveats of "adequate" funding.
# adequacy and resources are an "expression" of need based on formula set by state law and administrative choices. It does not reflect need perfectly.
 

# sum Student Enrollment (IRC) if Adequacy Level is less than 1 & RCDTS is not 6500000008000
df = df.loc[df['RCDTS'] != "6500000008000"]
sum_student_enrollment_irc = df.loc[df['Adequacy Level_fy2026'] < 1, 'Student Enrollment (IRC)_fy2026'].sum()
print(sum_student_enrollment_irc) #1509832.0


