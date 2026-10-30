# Create legislative district coverage data

import pandas as pd

shared_folder = r"C:\Users\cdpou\Documents\Projects\peer_app_data"

data_file_path = rf"{shared_folder}" # Change this to the directory with the data

file_path = rf"{data_file_path}"

# Method:

# Join directory of entities school data with with report card data and calculate district totals by school level student count

# Read in old legislative coverage file
df_old = pd.read_csv(r"C:\Users\cdpou\Documents\Projects\peer_illinois_funding_app\leg_dist_coverage.csv")

# group by legislator and keep first Chamber and District Number
df_old = df_old.groupby('Legislator Name').agg({'Chamber':'first', 'District Number':'first'}).reset_index()

# read new directory of education entities
dir_entities_df = pd.read_excel(rf"{file_path}\raw\dir_ed_entities_2026_10-30.xls",sheet_name="1 Public Dist & Sch")

# rename Region-2\nCounty-3\nDistrict-4 RCD

dir_entities_df.rename(columns={'Region-2\nCounty-3\nDistrict-4':'RCD'}, inplace=True)
# Create RCDTS column for EBF by concatenating RCD with Type and the first 2 digits of School
# make sure T is 2 padded with 0
dir_entities_df['RCDTS_revised'] = dir_entities_df['RCD'].astype(str) + dir_entities_df['Type'].astype(str).str.zfill(2) + dir_entities_df['School'].astype(str).str.zfill(4).str[:2]
dir_entities_df['RCDTS'] = dir_entities_df['RCD'].astype(str) + dir_entities_df['Type'].astype(str).str.zfill(2) + dir_entities_df['School'].astype(str).str.zfill(4)
print(dir_entities_df['RecType'].unique())

df_sch = dir_entities_df[dir_entities_df['RecType'] == "Sch"]

df_sch = df_sch[["RCDTS","RCDTS_revised","FacilityName","StRep","StSen"]]
# rename FacilityName to School District
df_sch.rename(columns={'FacilityName':'School District'}, inplace=True)

df_old_house = df_old[df_old['Chamber'] == 'House']
house_merge = df_sch[["RCDTS","RCDTS_revised","School District","StRep"]].merge(df_old_house, left_on="StRep", right_on="District Number", how="left")

df_old_senate = df_old[df_old['Chamber'] == 'Senate']
senate_merge = df_sch[["RCDTS","RCDTS_revised","School District","StSen"]].merge(df_old_senate, left_on="StSen", right_on="District Number", how="left")

# read in report card data to merge student count
report_card_df = pd.read_excel(rf"{file_path}\raw\2026-RC-Public-Data-Set.xlsx", sheet_name = "General")

# keep only relevant columns
report_card_df = report_card_df[['RCDTS', '# Student Enrollment']]
# remove - from RCDTS
report_card_df['RCDTS'] = report_card_df['RCDTS'].str.replace('-', '', regex=False)

# merge report card data with house_ and senate merges
house_merge_irc = house_merge.merge(report_card_df, on='RCDTS', how='left')
senate_merge_irc = senate_merge.merge(report_card_df, on='RCDTS', how='left')

# create RCDT by removing last 4 characters of RCDTS
house_merge_irc['RCDT'] = house_merge_irc['RCDTS'].str[:-4]
senate_merge_irc['RCDT'] = senate_merge_irc['RCDTS'].str[:-4]

# Create a summed student column grouped by RCDT
house_merge_irc_grouped = house_merge_irc.groupby('RCDT').agg({'# Student Enrollment':'sum'}).reset_index()
senate_merge_irc_grouped = senate_merge_irc.groupby('RCDT').agg({'# Student Enrollment':'sum'}).reset_index()

house_merge_irc_grouped = house_merge_irc_grouped[["RCDT", "# Student Enrollment"]]
senate_merge_irc_grouped = senate_merge_irc_grouped[["RCDT", "# Student Enrollment"]]
# rename # Student Enrollment to District Enrollment
house_merge_irc_grouped.rename(columns={'# Student Enrollment':'District Enrollment'}, inplace=True)
senate_merge_irc_grouped.rename(columns={'# Student Enrollment':'District Enrollment'}, inplace=True)

# merge with house_merge_irc and senate_merge_irc to include summed student enrollment by RCDT
house_merge_irc = house_merge_irc.merge(house_merge_irc_grouped, on='RCDT', how='left', suffixes=('', '_sum'))
senate_merge_irc = senate_merge_irc.merge(senate_merge_irc_grouped, on='RCDT', how='left', suffixes=('', '_sum'))

house_merge_irc['Share of Students'] = house_merge_irc['# Student Enrollment'] / house_merge_irc['District Enrollment']
senate_merge_irc['Share of Students'] = senate_merge_irc['# Student Enrollment'] / senate_merge_irc['District Enrollment']

# Sum Share of Students by RCDT and District Number

house_merge_irc_sum = house_merge_irc.groupby(['RCDT', 'StRep']).agg({'Share of Students':'sum','# Student Enrollment':'sum'}).reset_index()
senate_merge_irc_sum = senate_merge_irc.groupby(['RCDT', 'StSen']).agg({'Share of Students':'sum','# Student Enrollment':'sum'}).reset_index()

# merge df_old with the summed house and senate data
df_old_house_sum = df_old_house.merge(house_merge_irc_sum, left_on="District Number", right_on="StRep", how="left")
df_old_senate_sum = df_old_senate.merge(senate_merge_irc_sum, left_on="District Number", right_on="StSen", how="left")

# add 2 0s on RCDT

df_old_house_sum['RCDT'] = df_old_house_sum['RCDT'] + '00'
df_old_senate_sum['RCDT'] = df_old_senate_sum['RCDT'] + '00'

print(df_old_house_sum.columns)
print(df_old_senate_sum.columns)

keep_cols =['Legislator Name', 'Chamber', 'District Number', 'RCDT',
       'Share of Students', '# Student Enrollment']

df_old_house_sum = df_old_house_sum[keep_cols]
df_old_senate_sum = df_old_senate_sum[keep_cols]

print(dir_entities_df.columns)

district_names = dir_entities_df[dir_entities_df['RecType'] == "Dist"]

district_names = district_names[['RCDTS_revised','FacilityName']]

district_names.rename(columns={'RCDTS_revised':'RCDT','FacilityName':'School District'}, inplace=True)

# merge with df_old_house_sum and df_old_senate_sum to include school district information
df_old_house_sum = df_old_house_sum.merge(district_names, on='RCDT', how='left')
df_old_senate_sum = df_old_senate_sum.merge(district_names, on='RCDT', how='left')

# Change column names RCDT to RCDTS, # Student Enrollment to Total Students, Share of Students remains the same
df_old_house_sum.rename(columns={'RCDT':'RCDTS','# Student Enrollment':'Total Students'}, inplace=True)
df_old_senate_sum.rename(columns={'RCDT':'RCDTS','# Student Enrollment':'Total Students'}, inplace=True)

# stack
df_old_stacked = pd.concat([df_old_house_sum, df_old_senate_sum], ignore_index=True)

# save as csv_file in app folder C:\Users\cdpou\Documents\Projects\peer_illinois_funding_app
df_old_stacked.to_csv(r"C:\Users\cdpou\Documents\Projects\peer_illinois_funding_app\leg_dist_coverage_2026-10-30.csv", index=False)