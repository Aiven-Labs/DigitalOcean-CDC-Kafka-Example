from kafka import KafkaConsumer
from environment import KAFKA_BROKER, CDC_TOPIC
from dashboards import dashboard

import streamlit as st
import json
import pandas as pd

# Update the Streamlit app with data from the background thread
if __name__ == '__main__':

    # Streamlit dashboard
    sidebar = """
        This dashboard uses a consumer to fetch Kafka messages payloaded with CDC data.
        """

    dashboard(CDC_TOPIC, "Sales Transactions Real-Time ▁ ▂ ▃ ▄ ▅ ▆ █", sidebar)

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


    df = pd.DataFrame(
        {
            "sale price": [0.00],
            "average sale": [0.00],
        }
    )
    line_chart = st.line_chart(df)

    rolling = []
    for message in consumer:
        
        rolling.append(message.value["after"]["salesamount"])
        add_df = pd.DataFrame(
            {
                "sale price": [message.value["after"]["salesamount"]],
                "average sale": [sum(rolling)/len(rolling)],
            }
        )

        line_chart.add_rows(add_df)

# OK 
#                         Table "public.sales"
#       Column       |       Type       | Collation | Nullable | Default 
# -------------------+------------------+-----------+----------+---------
#  totalproductcost  | double precision |           |          | 
#  salesamount       | double precision |           |          | 

# Fail
#  totalproductcost  | numeric(36,6)               |           |          | 
#  salesamount       | numeric(36,6)               |           |          | 
