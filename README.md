## Strava personal dashboard
This folder defines all source code for the 'strava2databricks' pipeline:

- `00 Analyze`: Ad-hoc notebooks used to explore the data processed by this pipeline, from start to finish
- `01 Extract`: KnowHow on how to import data from source. In this case, extraction is done with Postman. 
- `02 Transform`: All dataset definitions and transformations.
- `03 Load`: Visualized data via dashboards.

## Getting Started

To get started, go to the `00 Analyze` folder -- there you can explore data through prepared notebooks:

* By convention, every dataset under `02 Transform` is in a separate file.
* Take a look at the sample under "to-be-added" to get familiar with the syntax.
  Read more about the syntax at https://docs.databricks.com/dlt/sql-ref.html.


## Introduction
Extracting, transforming and visualizing data from personal Strava account. 
This dataflow is composed of restAPI to get .json filesPostman and processing through Databricks platform. 

Tools that were used and documentation (tutorials, links etc) - in another .md file, ADD EVERYTHING from gdrive notes
## 00 Roadmap - soon to be added, draft is done

## 01 - extract from Strava with Postman

Added description of the process in a seperate [markdown file](https://github.com/UrbanclA/strava2databricks/blob/348ec73f52e027056d8c3ecd4e339fbbdf17455d/01%20Extract/README_postman.md) 

## 02 - bronze - Import json file to DataBricks Volume
utils file to add dataframe, add timestamp
### Creating a Parquet file
create delta file following databricks recommendations [useful_links](https://github.com/UrbanclA/strava2databricks/blob/28721dddac559212841b1857996ceb8813dfd908/useful_links.md)

`HotTip`
Initially, when I was importing the .json file to the Databricks volume, there was an error. After some research, it seemed like an issue with Serverless cluster and the file being too big to process. Probably Databricks free edition has some limitations in that regard, so I managed to fix it, setting environment memory from standard (16GB) to High (32 GB)

<img width="350" height="455" alt="image" src="https://github.com/user-attachments/assets/20d5bc64-a079-41c8-8181-bd00606c46ea" />

### 02 - silver - transform and load to delta table

Clean the data, add hashkeys and hashdiffs - soon

### 02 - gold - create dimensions and fact tables

transform, calculate, filter, round the numbers, mready for dashboard ingestion

## 3 - Visualize data in dashboard

Simple dashboard to start, upgrade later in the process
