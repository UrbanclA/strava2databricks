# Databricks notebook source
# MAGIC %md
# MAGIC ## Data Transformation - B2S2G - ACTIVITY

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS strava.bronze.initial_load;

# COMMAND ----------

# DBTITLE 1,Load JSON, add commit_date and athlete_id, drop athlete column
from utils import current_timestamp, date_format, col

#json path
json_path = "/Volumes/strava/bronze/source_files/last60activities.json"

# create dataframe
df = spark.read.json(json_path)

#adding a timestamp of data load and extracting athlete_id, then dropping athlete column
df_date_load =(
    df.withColumn(
        "commit_date",
            current_timestamp()
        )
    .withColumn(
        "athlete_id",
        col("athlete.id")
    )
    .drop("athlete")
)
display(df_date_load)
#display(df_date_load.columns)

# COMMAND ----------

#write to parquet file
parquet_path = "/Volumes/strava/bronze/initial_load"
df_date_load.write.mode("overwrite").parquet(parquet_path)

# COMMAND ----------

# DBTITLE 1,Load to delta table with reordered columns
#load to delta table, with overwrite mode (later append)
# Move 'id' and 'athlete_id' to the start of the table
cols = ["id", "athlete_id"] + [c for c in df_date_load.columns if c not in ["id", "athlete_id"]]
df_date_load = df_date_load.select(*cols)
df_date_load.write.format("delta").mode("overwrite").saveAsTable("strava.silver.activity")

# COMMAND ----------

# MAGIC %md
# MAGIC ## SelfNote1: add a transformation to load everything in bronze delta table (append)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from strava.silver.activity

# COMMAND ----------

# MAGIC %md
# MAGIC The following scripts will handle business logic, prepare data for star schema, and will include new transformations and columns once we decide to upgrade our model

# COMMAND ----------

# DBTITLE 1,Select and clean columns, calculate end_date
from utils import col, expr, to_date, round

spark.sql("DROP TABLE IF EXISTS strava.gold.fact_activity")
kmh_coeficient = 3.6
cal_coeficient = 4.184
dist_coeficient = 1000

df_fact_activity = (
    spark.table("strava.silver.activity")
    .select(
        col("id").alias("activity_id"),
        col("athlete_id"),
        col("name").alias("activity_name"),
        col("distance").alias("distance_m"),
        round(
            (col("distance")/dist_coeficient),
            2).alias("distance_km"),
        col("elapsed_time").alias("elapsed_time_s"),
        col("moving_time").alias("moving_time_s"),
        round(
            (col("average_speed")*kmh_coeficient),
            1).alias("average_speed_kmh"), #meters per second via strava api documentation
        round(
            (col("max_speed")*kmh_coeficient),
            1).alias("max_speed_kmh"), #meters per second via strava api documentation
        col("elev_high"),
        col("elev_low"),
        col("total_elevation_gain").alias("elevation_gain_m"),
        col("type").alias("activity_type"),
        col("sport_type"),
        to_date(col("start_date_local")).alias("activity_date"),
        date_format(col("start_date_local"), "HH:mm:ss").alias("activity_start_time"),
        col("max_heartrate"),
        col("average_heartrate"),
        round(
            (col("kilojoules")/cal_coeficient),
            1).alias("calories"), #conversion from kj to calories
        col("average_temp").alias("average_temp_c"),
        col("athlete_count"),
        col("kudos_count"),
        col("comment_count"),
        col("total_photo_count"),
        col("commit_date").cast("date")
        )
)
df_fact_activity.write.format("delta").mode("overwrite").saveAsTable("strava.gold.fact_activity")


# COMMAND ----------

df = spark.read.table("strava.gold.fact_activity")
display(df)
