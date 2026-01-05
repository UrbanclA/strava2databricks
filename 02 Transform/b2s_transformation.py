# Databricks notebook source
# MAGIC %md
# MAGIC ## Data Transformation - B2S

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS strava.bronze.initial_load;

# COMMAND ----------

from utils import current_timestamp, date_format

#json path
json_path = "/Volumes/strava/bronze/source_files/last60activities.json"

# create dataframe
df = spark.read.json(json_path)

#adding a timestamp of data load
df_date_load =(
    df.withColumn(
        "date",
        date_format(
            current_timestamp(),
            "dd-MM-yy"
        )
    )
)
display(df_date_load)
#display(df_date_load.columns)


# COMMAND ----------

#write to parquet file
parquet_path = "/Volumes/strava/bronze/initial_load"
df_date_load.write.mode("overwrite").parquet(parquet_path)

# COMMAND ----------

#load to delta table, with overwrite mode
df_date_load.write.format("delta").mode("overwrite").saveAsTable("strava.silver.strava")

# COMMAND ----------

# MAGIC %md
# MAGIC ## above, add a transformation to load everything in bronze delta table (append) 
# MAGIC ## below, next cell add that transfoirmation for ID = 142655309 = amadej and clean what columns you need in silver table

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog `strava`; select * from `silver`.`strava` limit 100;
