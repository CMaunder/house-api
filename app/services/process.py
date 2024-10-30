import pika
from time import sleep, strftime
import json
import mariadb
import sys
from dotenv import load_dotenv
import os

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def pull_and_save(continuous=False):
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host="localhost",
            port=3306,
            database="telegraphhouse"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()

    creds = pika.PlainCredentials(
            username=os.getenv("RABBITMQ_USER"), 
            password=os.getenv("RABBITMQ_PASSWORD")
        )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', credentials=creds))

    channel = connection.channel()
    q = channel.queue_declare('dht11_data', durable=True)

    def save_data(ch, method, properties, body):
        message = body.decode()
        data = json.loads(message)
        print(f"[x] message received:")
        print(data)
        cur.execute("INSERT INTO dht11_data (temp, humidity, room, recorded_at, inserted_at) VALUES (?, ?, ?, ?, ?)",
                    (data.get("temp"), data.get("humidity"), "Charlie_Office", data.get("time_recorded"), strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    if continuous:
        print("In continuous mode, waiting for messages...")
        channel.basic_consume(queue="dht11_data", on_message_callback=save_data)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("\nClosing the db connection.")
            conn.close()
    else:
        message_count = q.method.message_count
        for _ in range(1, message_count+1):
            method, properties, body = channel.basic_get(queue='dht11_data')
            save_data(channel, method, properties, body)
        conn.close()
        return message_count

if __name__ == '__main__':
    pull_and_save(continuous=True)