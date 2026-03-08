## Data Integration Build #1
This repository defines all source code for the ongoing 'strava2databricks' dataflow. This is build #1 of my Data Integration Portfolio (the DIP).

- `00 Analyze`: Ad-hoc notebooks used to explore the data processed by this pipeline, from start to finish
- `01 Extract`: KnowHow on how to import data from source. In this case, extraction is done with Postman. 
- `02 Transform`: All dataset definitions and transformations.
- `03 Load`: Visualized data via dashboards.

## Software Stack

* Strava - Source
* Postman - Extraction
* Databricks (Free Edition) - Transformations and Visualizations
* GitHub - Branching and Versioning, Code Vault, Documentation
* GoogleDrive - Administration, Notes, Ideas
* Gemini - Guidance
* Udemy - Python Course
* and loads of tutorials, blogs - gathered here [useful_links](https://github.com/UrbanclA/strava2databricks/blob/28721dddac559212841b1857996ceb8813dfd908/useful_links.md)


## Introduction
Looking at my own habbits, an active guy who uses Strava on a weekly basis, I thought to myself, what better way to learn something new with data I produce and am familiar with? 
Thats when the idea of extracting, transforming and visualizing data from my personal Strava account really came to life.

This dataflow is composed of restAPI setup to extract .json files with the help of Postman. The rest is done in Databricks platform with PySpark.

## 00 - Roadmap

![](https://github.com/UrbanclA/strava2databricks/blob/b8089600fb84b388a7187312f6600f5e98b69b8b/99%20Pictures/roadmap_step5.jpg)

Roadmap graphic design by Tilen from Uniq Agency [LinkedIn](https://www.linkedin.com/in/tilen-vogrinec-253537281/)

## 01 - extract from Strava with Postman

Read the detailed description of the process in a seperate [markdown file](https://github.com/UrbanclA/strava2databricks/blob/348ec73f52e027056d8c3ecd4e339fbbdf17455d/01%20Extract/README_postman.md) 

## 02 - bronze - Import json file to Databricks Volume

utils file to add dataframe, add timestamp

### Creating a Parquet file
Creatinh a delta file following databricks recommendations [useful_links](https://github.com/UrbanclA/strava2databricks/blob/28721dddac559212841b1857996ceb8813dfd908/useful_links.md)

`HotTip`
Initially, when I was importing the .json file to the Databricks volume, there was an error. After some research, it seemed like an issue with Serverless cluster and the file being too big to process. Probably Databricks free edition has some limitations in that regard, so I managed to fix it, setting environment memory from standard (16GB) to High (32 GB)

<img width="350" height="455" alt="image" src="https://github.com/user-attachments/assets/20d5bc64-a079-41c8-8181-bd00606c46ea" />

### 02 - silver - transform and load to delta table

Clean the data, add hashkeys and hashdiffs - soon

### 02 - gold - create dimensions and fact tables

transform, calculate, filter, round the numbers, mready for dashboard ingestion

## 3 - Visualize data in dashboard

Simple dashboard to start, upgrade later in the process
