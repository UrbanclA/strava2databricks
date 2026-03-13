This is a part of my [Data Integration Portfolio](https://github.com/UrbanclA/strava2databricks/blob/main/DIP.md)

## Data Integration Build #1
This repository defines all source code for the ongoing 'strava2databricks' dataflow. 

- `00 Analyze`: Ad-hoc notebooks used to explore the data processed by this dataflow, from start to finish.
- `01 Extract`: KnowHow on how to import data from source. In this case, extraction is done with Postman. 
- `02 Transform`: All dataset definitions and transformations.
- `03 Load`: Visualized data via dashboards.

`NOTE`: Sections marked with `WIP` are a Work-In-Progress. The descriptions will be added along the way!

## Software Stack

* Strava - Source
* Postman - Extraction
* Databricks (Free Edition) - Transformations and Visualizations
* GitHub - Branching and Versioning, Code Vault, Documentation
* GoogleDrive - Administration, Notes, Ideas
* Gemini - Guidance
* Udemy - Python Course
* and loads of tutorials, blogs - gathered here [useful_links](https://github.com/UrbanclA/strava2databricks/blob/main/useful_links.md)


# Introduction
Looking at my own habits, an active guy who uses Strava on a weekly basis, I thought to myself, what better way to learn something new with data I produce and am familiar with? 
Thats when the idea of extracting, transforming and visualizing data from my personal Strava account really came to life.

This dataflow is composed of restAPI setup to extract .json files with the help of Postman. The rest is done in Databricks platform with PySpark.

## 00 - Roadmap

![](https://github.com/UrbanclA/strava2databricks/blob/main/99%20Pictures/Roadmap_step_5.jpg)

Roadmap graphic design by Tilen from Uniq Agency [LinkedIn](https://www.linkedin.com/in/tilen-vogrinec-253537281/)

# Catalog setup
Following Medallion architecture, here's how I setup my databricks catalog. 

The name of my database will be strava, with bronze, silver and gold layers ready as schemas. 
Information_schema is default and may be used in the future for user permissions and audit.

![](https://github.com/UrbanclA/strava2databricks/blob/main/99%20Pictures/catalog-strava.png)

## 01 - extraction via Postman

Read the detailed description and step-by-step guide of the process in a seperate [markdown file](https://github.com/UrbanclA/strava2databricks/blob/main/01%20Extract/README_postman.md) 

For the first export, we are looking at only 1 table (activities) and extracting only last 60 activities at the time. Hence the name of the file is
`last60activities.json`

## 02 - bronze - Import json file to Databricks Volume

For now, I'm uploading the extracted .json file manually to databricks volume into source_files folder.

![](https://github.com/UrbanclA/strava2databricks/blob/main/99%20Pictures/bronze-sourcefiles.png)

The utils.py notebook holds some of the most referenced functions in other notebooks, such as add timestamp.

### Creating a Parquet file
Once we imported .json file in bronze schema, we start our transformation flow. 
With notebook [t_activity](https://github.com/UrbanclA/strava2databricks/blob/main/02%20Transform/t_activity.py) we are creating a delta parquet file following databricks recommendations found in [useful_links](https://github.com/UrbanclA/strava2databricks/blob/main/useful_links.md)

Under `initial_load` folder now lives our delta parquet file, ready to be ingested in silver table


![](https://github.com/UrbanclA/strava2databricks/blob/main/99%20Pictures/bronze-parquetfile.png)

`Important` to note is, in this step we are adding a timestamp to the dataset as new column, so we know when the file was processed. It will come in handy in the future once we start appending new data.

`HotTip`
Initially, when I was importing the .json file to the Databricks volume, there was an error. After some research, it seemed like an issue with Serverless cluster and the file being too big to process. Probably Databricks free edition has some limitations in that regard, so I managed to fix it, setting environment memory from standard (16GB) to High (32 GB)

<img width="350" height="455" alt="image" src="https://github.com/user-attachments/assets/20d5bc64-a079-41c8-8181-bd00606c46ea" />

### 02 - silver - transform and load to delta table

`WIP`
Clean the data, add hashkeys and hashdiffs - soon

![](https://github.com/UrbanclA/strava2databricks/blob/main/99%20Pictures/silver_activity.png)

### 02 - gold - create dimensions and fact tables

`WIP`
transform, calculate, filter, round the numbers, ready for dashboard ingestion

## 3 - Visualize data in dashboard

`WIP`
Simple dashboard to start, upgrade later in the process
