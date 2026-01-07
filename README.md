## Strava personal dashboard
This folder defines all source code for the 'strava2databricks' pipeline:

- `00 Analyze`: Ad-hoc notebooks used to explore the data processed by this pipeline, from start to finish
- `01 Extract`: KnowHow on how to import data from source. In this case, extraction is done with Postman.
- `02 Transform`: All dataset definitions and transformations.
- `03 Transform`: All dataset definitions and transformations.

## Getting Started

To get started, go to the `00 Analyze` folder -- there you can explore data through prepared notebooks:

* By convention, every dataset under `02 Transform` is in a separate file.
* Take a look at the sample under "to-be-added" to get familiar with the syntax.
  Read more about the syntax at https://docs.databricks.com/dlt/sql-ref.html.


## 0 Introduction
Extracting, transforming and visualizing data from Strava using Postman and DataBricks. 

Tools that were used and documentation (tutorials, links etc) - in another .md file, ADD EVERYTHING from gdrive notes

## 1 - extract from Strava with Postman

## 2 - Importing json file to DataBricks Volume (bronze)
utils file to add dataframe, add timestamp
### Creating a Parquet file
create delta file

- https://docs.databricks.com/aws/en/files/files-recommendations

Error from my research had to only do with Serverless cluster and file being to big to process, that is why I changed environment memory from standard (16GB) to High (32 GB)
<img width="493" height="647" alt="image" src="https://github.com/user-attachments/assets/20d5bc64-a079-41c8-8181-bd00606c46ea" />
### transform and load to delta table (silver)
## 3 - Visualizing in dashboard
