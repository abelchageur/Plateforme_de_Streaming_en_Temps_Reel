# from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json, explode, col, current_timestamp, concat_ws
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType

# # Initialisation de Spark
# spark = SparkSession.builder \
#     .appName("RandomUserStreaming") \
#     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
#     .getOrCreate()

# # Schéma des données Random User
# schema = StructType([
#     StructField("results", ArrayType(StructType([
#         StructField("name", StructType([
#             StructField("first", StringType()),
#             StructField("last", StringType())
#         ])),
#         StructField("location", StructType([
#             StructField("country", StringType())
#         ])),
#         StructField("dob", StructType([
#             StructField("age", IntegerType())
#         ])),
#         StructField("gender", StringType()),
#         StructField("login", StructType([
#             StructField("uuid", StringType())
#         ]))
#     ])))
# ])

# # Lecture depuis Kafka
# df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:9092") \
#     .option("subscribe", "random_user_data") \
#     .option("startingOffsets", "latest") \
#     .load()

# # Conversion du JSON et explosion du tableau
# parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
#     .select(explode("data.results").alias("user"))

# # Enrichissement des données
# enriched_df = parsed_df.select(
#     col("user.login.uuid").alias("user_id"),
#     concat_ws(" ", col("user.name.first"), col("user.name.last")).alias("full_name"),
#     col("user.location.country").alias("country"),
#     col("user.dob.age").alias("age"),
#     col("user.gender").alias("gender"),
#     current_timestamp().alias("ingestion_time")
# )

# # Affichage des données dans la console
# console_query = enriched_df.writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .trigger(processingTime="10 seconds") \
#     .start()

# cassandra_query = enriched_df.writeStream \
#     .format("org.apache.spark.sql.cassandra") \
#     .option("keyspace", "random_user_keyspace") \
#     .option("table", "random_user_table") \
#     .option("spark.cassandra.connection.host", "cassandra") \
#     .option("checkpointLocation", "/tmp/checkpoint/cassandra") \
#     .outputMode("append") \
#     .trigger(processingTime="10 seconds") \
#     .start()

# # Attendre la fin du stream
# console_query.awaitTermination()


# from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json, explode, col, current_timestamp, concat_ws
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType

# # Initialisation de Spark avec les dépendances explicites
# spark = SparkSession.builder \
#     .appName("RandomUserStreaming") \
#     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
#     .getOrCreate()

# # Schéma des données Random User
# schema = StructType([
#     StructField("results", ArrayType(StructType([
#         StructField("name", StructType([
#             StructField("first", StringType()),
#             StructField("last", StringType())
#         ])),
#         StructField("location", StructType([
#             StructField("country", StringType())
#         ])),
#         StructField("dob", StructType([
#             StructField("age", IntegerType())
#         ])),
#         StructField("gender", StringType()),
#         StructField("login", StructType([
#             StructField("uuid", StringType())
#         ]))
#     ])))
# ])

# # Lecture depuis Kafka
# df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:9092") \
#     .option("subscribe", "random_user_data") \
#     .option("startingOffsets", "latest") \
#     .load()

# # Conversion du JSON et explosion du tableau
# parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
#     .select(explode("data.results").alias("user"))

# # Enrichissement des données
# enriched_df = parsed_df.select(
#     col("user.login.uuid").alias("user_id"),
#     concat_ws(" ", col("user.name.first"), col("user.name.last")).alias("full_name"),
#     col("user.location.country").alias("country"),
#     col("user.dob.age").alias("age"),
#     col("user.gender").alias("gender"),
#     current_timestamp().alias("ingestion_time")
# )

# # Affichage des données dans la console
# console_query = enriched_df.writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .trigger(processingTime="10 seconds") \
#     .start()

# # Écriture des données dans MongoDB
# mongo_query = enriched_df.writeStream \
#     .format("mongodb") \
#     .option("uri", "mongodb://admin:password@mongodb:27017/randomUserDB.randomUserCollection?authSource=admin") \
#     .option("checkpointLocation", "/tmp/checkpoint/mongo") \
#     .outputMode("append") \
#     .start()

# # Attendre toutes les queries en parallèle
# spark.streams.awaitAnyTermination()

#######################################################################################
#######################################################################################

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, explode, col, current_timestamp, concat_ws, count, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType

# Initialisation de Spark avec les dépendances explicites
spark = SparkSession.builder \
    .appName("RandomUserStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
            "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0,"
            "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0") \
    .getOrCreate()

# Schéma des données Random User
schema = StructType([
    StructField("results", ArrayType(StructType([
        StructField("name", StructType([
            StructField("first", StringType()),
            StructField("last", StringType())
        ])),
        StructField("location", StructType([
            StructField("country", StringType())
        ])),
        StructField("dob", StructType([
            StructField("age", IntegerType())
        ])),
        StructField("gender", StringType()),
        StructField("login", StructType([
            StructField("uuid", StringType())
        ]))
    ])))
])

# Lecture depuis Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "random_user_data") \
    .option("startingOffsets", "latest") \
    .load()

# Conversion du JSON et explosion du tableau
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select(explode("data.results").alias("user"))

# Enrichissement des données
enriched_df = parsed_df.select(
    col("user.login.uuid").alias("user_id"),
    concat_ws(" ", col("user.name.first"), col("user.name.last")).alias("full_name"),
    col("user.location.country").alias("country"),
    col("user.dob.age").alias("age"),
    col("user.gender").alias("gender"),
    current_timestamp().alias("ingestion_time")
)

# Affichage des données brutes dans la console
console_query = enriched_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .trigger(processingTime="10 seconds") \
    .start()

# Écriture des données brutes dans MongoDB
mongo_query = enriched_df.writeStream \
    .format("mongodb") \
    .option("uri", "mongodb://admin:password@mongodb:27017/randomUserDB.randomUserCollection?authSource=admin") \
    .option("checkpointLocation", "/tmp/checkpoint/mongo") \
    .outputMode("append") \
    .start()

# Écriture des données brutes dans Cassandra (random_user_table)
cassandra_raw_query = enriched_df.writeStream \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "random_user_keyspace") \
    .option("table", "random_user_table") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("checkpointLocation", "/tmp/checkpoint/cassandra_raw") \
    .outputMode("append") \
    .trigger(processingTime="10 seconds") \
    .start()

# Agrégation : Nombre d'utilisateurs et âge moyen par pays
aggregated_df = enriched_df \
    .groupBy("country") \
    .agg(
        count("*").alias("user_count"),
        avg("age").alias("avg_age")
    ) \
    .select(
        col("country"),
        col("user_count"),
        col("avg_age"),
        current_timestamp().alias("last_update")
    )

# Écriture des données agrégées dans Cassandra (country_stats)
cassandra_agg_query = aggregated_df.writeStream \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "random_user_keyspace") \
    .option("table", "country_stats") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("checkpointLocation", "/tmp/checkpoint/cassandra_agg") \
    .outputMode("update") \
    .trigger(processingTime="10 seconds") \
    .start()

# Affichage des données agrégées dans la console (optionnel)
agg_console_query = aggregated_df.writeStream \
    .format("console") \
    .outputMode("update") \
    .trigger(processingTime="10 seconds") \
    .start()

# Attendre toutes les queries en parallèle
spark.streams.awaitAnyTermination()