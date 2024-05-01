import json
from kafka import KafkaConsumer
import streamlit as st
import pandas as pd
from environment import KAFKA_BROKER, CDC_TOPIC
from dashboards import dashboard


def consume_kafka_messages():
    consumer = KafkaConsumer(
        CDC_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset='latest',
        security_protocol="SSL",
        ssl_cafile=".certificates/ca-certificate.crt",
        ssl_certfile=".certificates/user-access-certificate.crt",
        ssl_keyfile=".certificates/user-access-key.key",
    )

    for msg in consumer:
        data = msg.value
        st.write(msg['last_updated'])

# Update the Streamlit app with data from the background thread
if __name__ == '__main__':

    # Streamlit dashboard
    sidebar = """
        This dashboard uses a consumer to fetch Kafka messages payloaded with CDC data.
        """

    dashboard(CDC_TOPIC, sidebar)

    # Consume Kafka messages
    consume_kafka_messages()
