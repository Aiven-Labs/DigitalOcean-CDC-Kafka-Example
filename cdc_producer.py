import json
from kafka import KafkaProducer
import streamlit as st
from environment import KAFKA_BROKER, CDC_TOPIC, PG_CONNECT
from dashboards import dashboard

import psycopg2
from psycopg2.extras import LogicalReplicationConnection


# Kafka producer
def produce_kafka_messages(message):
    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        security_protocol="SSL",
        ssl_cafile=".certificates/ca-certificate.crt",
        ssl_certfile=".certificates/user-access-certificate.crt",
        ssl_keyfile=".certificates/user-access-key.key",
        )

    res = json.dumps(message).encode("utf-8")
    producer.send(CDC_TOPIC, res)
    return res
    

if __name__ == '__main__':
    sidebar = """
        This producer generates Kafka messages using Postgres CDC using a replication slot.
        """
    
    dashboard("producer: postgres cdc", sidebar)

    conn = psycopg2.connect(
        PG_CONNECT,
        connection_factory=LogicalReplicationConnection
    )
    cur = conn.cursor()

    replication_options = {
      'include-xids':'1',
      'include-timestamp':'1',
      'pretty-print':'1'
    }

    try:
        cur.start_replication(slot_name='py_subscriber', decode=True, options=replication_options)
    except psycopg2.ProgrammingError:
        cur.create_replication_slot('py_subscriber', output_plugin='wal2json')
        cur.start_replication(slot_name='py_subscriber', decode=True, options=replication_options)


    class LogicalStreamConsumer(object):
        def __call__(self, msg):
          message = produce_kafka_messages(msg.payload)
          if message:
              st.success("Weather data produced to Kafka.")
          else:
              st.error("Error producing data to Kafka.")

          msg.cursor.send_feedback(flush_lsn=msg.data_start)

    logicalstreamconsumer = LogicalStreamConsumer()
  
    try:
      cur.consume_stream(logicalstreamconsumer)
    except KeyboardInterrupt:
      cur.close()
      conn.close()