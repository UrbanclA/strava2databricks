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

#load to delta table, with overwrite mode (later append)
df_date_load = spark.read.parquet(parquet_path)
df_date_load.write.format("delta").mode("overwrite").saveAsTable("strava.silver.activity")

# COMMAND ----------

# MAGIC %md
# MAGIC ## above, add a transformation to load everything in bronze delta table (append) 
# MAGIC ## below, clean what columns you need in silver table, e.g.;
# MAGIC activity (id, athlete_id, name, distance, moving_time, elev_high, elev_low, elevation_gain, type, sport_type, start_date, start_date_local, timezone, end_date(calculate start time + moving_time), max_heartrate, average_heartrate,athlete_count,kudos_count, comment_count, photo_count)

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog `strava`; select * from `silver`.`activity` limit 100;
