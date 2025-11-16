# Illinois School District Resource Inequality App


### <i> Authors: 

- Chris D. Poulos (Public Finance and Education Policy Analyst at the Chicago Teachers Union) cdpoulos@gmail.com

- Erykah Nava (PEER Illinois Lead Organizer), erykah@ilraiseyourhand.org
</i>

<b>Purpose:</b>

A web app created for [Partnership for Equity and Education Rights Illinois](https://www.peerillinois.org/) designed to provide easy and intuitive access to statewide and district-level information on resource inequality and Illinois' K-12 Evidence-Based Funding formula for public schools.

See todo.md for tasks

---

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
<summary><strong>\peer_streamlit_app<br></br></strong></summary>

> Root folder

\.gitignore

> Setting parameters around what git can commit.

\app_data_wide.parquet

> Data for streamlit app. In parquet form for efficiency.

\peer_app.py

> Streamlit web app

\peer_hex_codes.txt

> PEER brand colors

\peer_logo.png

> Peer logo image

\README.md

> The very file you are looking at at this very moment!

\requirements.txt

> Packages used in the appliction

\todo.md

> list of tasks


</details>
