#display(spark.sql("SELECT * FROM samples.taxis.trips"))
from pyspark.sql.functions import current_timestamp, date_format

#json path
json_path = "/Volumes/workspace/default/testjson/last60activities.json"

# create dataframe
df = spark.read.json(json_path)


#add a timestamp
df1 = df.withColumn("date", date_format(current_timestamp(), "dd-MM-yy"))

#write to parquet file
df1.write.mode("overwrite").parquet("/Volumes/workspace/default/output")
