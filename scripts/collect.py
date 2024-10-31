import pika
from time import sleep
import adafruit_dht
import board
import datetime
import json
from statistics import mean
from dotenv import load_dotenv
import os

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def record(readings=10):
    dht_device = adafruit_dht.DHT11(board.D4)

    creds = pika.PlainCredentials(username=os.getenv("RABBITMQ_USER"), password=os.getenv("RABBITMQ_PASSWORD"))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=creds))
    channel = connection.channel()

    channel.queue_declare(queue='dht11_data', durable=True)

    now = datetime.datetime.now()

    temp_array = []
    humidity_array = []
    for _ in range(1,readings+1):
        try:
            temp_array.append(dht_device.temperature)
            humidity_array.append(dht_device.humidity)
        except RuntimeError as err:
            # TODO - add retry functionality here if err.args[0] == "Checksum did not validate. Try again.", or maybe retry for any RuntimeError, with limit
            print(err.args[0])
        sleep(3)

    data = {"temp": mean(temp_array), "humidity": mean(humidity_array), "time_recorded": str(now)}
    message = json.dumps(data)
    channel.basic_publish(exchange='', 
                    routing_key='dht11_data', 
                    body=message, 
                    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
                    )
    print(f"[x] message: {message} sent.")
    connection.close()
    dht_device.exit()

if __name__ == '__main__':
    record()