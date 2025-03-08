import requests
import json
from confluent_kafka import Producer
import time
import logging

# Configuration du logging pour voir ce qui se passe
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration Kafka
kafka_config = {
    'bootstrap.servers': 'localhost:29092',  # Adresse du broker Kafka (port externe)
    'client.id': 'random-user-producer'
}
producer = Producer(kafka_config)
topic = 'random_user_data'  # Le topic où les données seront envoyées

# URL de l'API Random User
API_URL = "https://randomuser.me/api/?results=10"  # Retourne 10 utilisateurs fictifs

def delivery_report(err, msg):
    """Callback pour confirmer si le message a été envoyé à Kafka."""
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def fetch_and_produce():
    """Récupère les données de l'API et les envoie à Kafka."""
    retries = 3  # Nombre maximum de tentatives en cas d'échec
    for attempt in range(retries):
        try:
            # Appel à l'API Random User
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()  # Lève une exception si le code HTTP n'est pas 200
            data = response.json()  # Convertit la réponse en JSON

            # Envoie les données brutes à Kafka sous forme de chaîne JSON
            producer.produce(
                topic,
                value=json.dumps(data).encode('utf-8'),  # Sérialisation en UTF-8
                callback=delivery_report
            )
            producer.poll(0)  # Traite les événements en attente
            logger.info("Batch of 10 users sent to Kafka")
            break  # Sort de la boucle si succès
        except requests.RequestException as e:
            logger.error(f"API call failed: {e}")
            if attempt < retries - 1:
                logger.info(f"Retrying in 5 seconds... ({attempt + 1}/{retries})")
                time.sleep(5)  # Attend avant de réessayer
            else:
                logger.error("Max retries reached. Skipping this batch.")

if __name__ == "__main__":
    logger.info("Starting Random User Producer...")
    while True:
        fetch_and_produce()  # Récupère et envoie un batch
        time.sleep(10)  # Attend 10 secondes avant le prochain appel