import json
from kafka import KafkaProducer
import streamlit as st
from environment import KAFKA_BROKER, WEATHTER_TOPIC
from weather import fetch_weather_data
from dashboards import dashboard

# Kafka producer
def produce_kafka_messages(loc):
    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        security_protocol="SSL",
        ssl_cafile=".certificates/ca-certificate.crt",
        ssl_certfile=".certificates/user-access-certificate.crt",
        ssl_keyfile=".certificates/user-access-key.key",
        )

    weather_data = fetch_weather_data(loc)

    if weather_data:
        res = json.dumps(weather_data).encode("utf-8")

        # Send weather data to Kafka topic
        producer.send(WEATHTER_TOPIC, res)
        return res
    
    return False


if __name__ == '__main__':
    sidebar = """
        This producer generates Kafka messages from weather data using Accuweather APIs.
        """
    
    dashboard("producer: weather data", "Generate Report", sidebar)

    # Display input field
    location = st.text_input('Location')

    # Display call-to-action button
    action = st.button('Produce weather data to Kafka')

    if action:
        message = produce_kafka_messages(location)
        if message:
            st.success("Weather data produced to Kafka.")
        else:
            st.error("Error producing data to Kafka.")
