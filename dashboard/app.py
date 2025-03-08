import streamlit as st
from cassandra.cluster import Cluster
import pandas as pd
import plotly.express as px
import time

# Connexion à Cassandra
cluster = Cluster(['cassandra'], port=9042)
session = cluster.connect('random_user_keyspace')

# Fonctions pour récupérer les données
def get_latest_users():
    query = "SELECT user_id, full_name, country, age, gender, ingestion_time FROM random_user_table ORDER BY ingestion_time DESC LIMIT 10"
    rows = session.execute(query)
    return pd.DataFrame(rows)

def get_country_stats():
    query = "SELECT country, count_users, avg_age FROM country_stats"
    rows = session.execute(query)
    return pd.DataFrame(rows)

# Interface Streamlit
st.title("Random User Streaming Dashboard")

# Section pour les derniers utilisateurs
st.subheader("Derniers Utilisateurs")
users_df = get_latest_users()
st.dataframe(users_df)

# Section pour les statistiques agrégées
st.subheader("Statistiques par Pays")
stats_df = get_country_stats()

# Graphique du nombre d'utilisateurs par pays
fig_users = px.bar(stats_df, x="country", y="count_users", title="Nombre d'utilisateurs par pays")
st.plotly_chart(fig_users)

# Graphique de l'âge moyen par pays
fig_age = px.bar(stats_df, x="country", y="avg_age", title="Âge moyen par pays")
st.plotly_chart(fig_age)

# Rafraîchissement automatique
time.sleep(5)
st.experimental_rerun()
