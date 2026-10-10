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

# read in fy 2026 data
app_data_wide_fy2026 = pd.read_parquet(rf"{app_path}\app_data_wide_fy2026.parquet")

# display chart of Adequacy Level by Black (%)

import matplotlib.pyplot as plt

plt.scatter(app_data_wide_fy2026['Black (%)'], app_data_wide_fy2026['Adequacy Level'])
plt.xlabel('Black (%)')
plt.ylabel('Adequacy Level')
plt.title('Adequacy Level by Black (%)')
plt.show()

plt.scatter(app_data_wide_fy2026['Latine (%)'], app_data_wide_fy2026['Adequacy Level'])
plt.xlabel('Low Income (%)')
plt.ylabel('Adequacy Level')
plt.title('Adequacy Level by Black (%)')
plt.show()

# run a bivariate regression of low income on adequacy level
import statsmodels.api as sm

# remove missing data from Low Income (%)
app_data_wide_fy2026_regression = app_data_wide_fy2026.dropna(subset=['Low Income (%)', 'Adequacy Level'])

X = app_data_wide_fy2026_regression['Low Income (%)']
y = app_data_wide_fy2026_regression['Adequacy Level']
X = sm.add_constant(X)  # add a constant for the intercept
model = sm.OLS(y, X).fit()
print(model.summary())