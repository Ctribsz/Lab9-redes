import json
import random
import time
from kafka import KafkaProducer
from sensor_utils import generate_measurement

# ⚠️ CAMBIA ESTO POR TU CARNÉ
TOPIC = "2020xxxx"  # por ejemplo "20201234"

# Servidor de Kafka proporcionado en el laboratorio
BOOTSTRAP_SERVERS = ["lab9.alumchat.lol:9092"]


def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
    )

    print(f"Producer JSON listo. Topic = {TOPIC}")
    print("Enviando una medición cada 15 a 30 segundos. Ctrl+C para detener.\n")

    try:
        while True:
            measurement = generate_measurement()
            key = "sensor1"

            # Enviar al broker
            future = producer.send(
                TOPIC,
                key=key,
                value=measurement,
            )
            result = future.get(timeout=10)

            print(
                f"[{time.strftime('%H:%M:%S')}] Enviado -> "
                f"partición {result.partition}, offset {result.offset}, "
                f"payload={measurement}"
            )

            # Espera aleatoria entre 15 y 30 segundos
            delay = random.randint(15, 30)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario. Cerrando producer...")
    finally:
        producer.flush()
        producer.close()
        print("Producer cerrado.")


if __name__ == "__main__":
    main()
