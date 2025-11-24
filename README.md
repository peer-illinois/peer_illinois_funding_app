# Illinois School District Resource Inequality App


### <i> Authors: 

- Chris D. Poulos (Public Finance and Education Policy Analyst at the Chicago Teachers Union) cdpoulos@gmail.com

- Erykah Nava (PEER Illinois Lead Organizer), erykah@ilraiseyourhand.org
</i>

<b>Purpose:</b>

A web app created for [Partnership for Equity and Education Rights Illinois](https://www.peerillinois.org/) designed to provide easy and intuitive access to statewide and district-level information on resource inequality and Illinois' K-12 school districts.

<details>
<summary><strong>Data sources</strong></summary>

[Directorty of Educaitonal Entities data (DEE)](https://www.isbe.net/pages/data-analysis-directories.aspx)

> Used to join legislative districts.

[EBF distribution calculation (EBF)](https://www.isbe.net/ebfdist)

> FY25. Used for adequacy targets and gaps (both total dollars and positions).

[Employment Information System teacher salary dataset (EIS)](https://www.isbe.net/Pages/Educator-Employment-Information.aspx)

> Using for position counts. See Isbe_CleanJoin_20250515.ipynb for calculations to match EIS with EBF definitions.

[Illinois Report Card (IRC)](https://www.isbe.net/Pages/Illinois-State-Report-Card-Data.aspx)

> SY24. Used for demographic data, revenue by source data, and for specific actual position FTE counts.

[School Support Personnel Report (SSP)](https://www.isbe.net/Pages/Data-Analysis-Reports.aspx)

> No longer using SSP, because of the lack of documentations. instead using EIS and IRC for position counts. I am keeping the SSP cleaning in the script in case it is useful in the future.

</details>

----

<h3>Folder contents:</h3>

<details>
<summary><strong>\peer_illinois_funding_app<br></br></strong></summary>

> Root folder

\.streamlit\config.toml

> Used for design.

\README.md

> This file.

\app_data_wide.parquet

> Data for streamlit app.

\leg_dist_coverage.csv

> A legislative district to ISBE school district crosswalk that contains the legislative district's students as a percent of total students in the respective school district. This was created using the Illinois State Board of Education's Directorty of Educaitonal Entities. This data is loaded into the peer_app.py.

\logo.jpg

> Peer logo image loaded into the peer_app.py

\peer_app.py

> Streamlit web app

\peer_app_data_cleaning_script.ipynb

> A Jupyter Notebook that shows how we clean our data.

\requirements.txt

> Packages used in the appliction


</details>
