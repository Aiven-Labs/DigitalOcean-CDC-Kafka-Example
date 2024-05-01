from dotenv import load_dotenv
import os

# take environment variables from .env
load_dotenv()

# AccuWeather API key
WEATHER_API_KEY   = os.getenv("WEATHER_API_KEY")

# Kafka
KAFKA_BROKER      = os.getenv("KAFKA_BROKER")
WEATHTER_TOPIC    = os.getenv("WEATHER_TOPIC")
CDC_TOPIC         = os.getenv("CDC_TOPIC")

# Postgres
PG_CONNECT        = os.getenv("PG_CONNECT")
