# Databricks notebook source
# MAGIC %md
# MAGIC ## Data Transformation - B2S - ACTIVITY

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

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from strava.silver.activity

# COMMAND ----------

# DBTITLE 1,Select and clean columns, calculate end_date
from utils import col, expr, date_format

spark.sql("DROP TABLE IF EXISTS strava.gold.fact_activity")

df_fact_activity = (
    spark.table("strava.silver.activity")
    .select(
        col("id").alias("activity_id"),
        col("athlete.id").alias("athlete_id"), #picks out only id for json object inside athlete column
        col("name").alias("activity_name"),
        col("distance").alias("distance_m"),
        col("elapsed_time").alias("elapsed_time_s"),
        col("moving_time").alias("moving_time_s"),
        col("average_speed").alias("average_speed_kmh"),
        col("elev_high"),
        col("elev_low"),
        col("total_elevation_gain").alias("elevation_gain_m"),
        col("type").alias("activity_type"),
        col("sport_type"),
        date_format(col("start_date_local"), "dd-MM-yyyy").alias("activity_date"),
        date_format(col("start_date_local"), "HH:mm:ss").alias("activity_start_time"),
        col("max_heartrate"),
        col("average_heartrate"),
        (col("kilojoules")/4).alias("calories"), #conversion from kj to calories
        col("average_temp").alias("average_temp_c"),
        col("athlete_count"),
        col("kudos_count"),
        col("comment_count"),
        col("total_photo_count"),
        col("date")
    )
)

df_fact_activity.write.format("delta").mode("overwrite").saveAsTable("strava.gold.fact_activity")

# COMMAND ----------

df = spark.read.table("strava.gold.fact_activity")
display(df)
