CREATE KEYSPACE IF NOT EXISTS random_user_keyspace 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS random_user_keyspace.random_user_table (
    user_id text,
    ingestion_time timestamp,
    full_name text,
    country text,
    age int,
    gender text,
    PRIMARY KEY (user_id, ingestion_time)
) WITH CLUSTERING ORDER BY (ingestion_time DESC);

CREATE TABLE IF NOT EXISTS random_user_keyspace.country_stats (
    country text PRIMARY KEY,
    user_count bigint,  -- Changed from count_users to match PySpark
    avg_age double,
    last_update timestamp  -- Added to match PySpark and project needs
);