import random
import time
from kafka import KafkaProducer
from sensor_utils import generate_measurement, encode_measurement_to_bytes

# ⚠️ CAMBIA ESTO POR TU CARNÉ
TOPIC = "2020xxxx"

# Servidor de Kafka proporcionado en el laboratorio
BOOTSTRAP_SERVERS = ["lab9.alumchat.lol:9092"]


def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
    )

    print(f"Producer compacto listo. Topic = {TOPIC}")
    print("Enviando mediciones codificadas (3 bytes) cada 15 a 30 segundos. Ctrl+C para detener.\n")

    try:
        while True:
            measurement = generate_measurement()
            payload_bytes = encode_measurement_to_bytes(measurement)

            future = producer.send(
                TOPIC,
                key=b"sensor1",
                value=payload_bytes,
            )
            result = future.get(timeout=10)

            print(
                f"[{time.strftime('%H:%M:%S')}] Enviado -> "
                f"partición {result.partition}, offset {result.offset}, "
                f"original={measurement}, bytes={payload_bytes.hex()}"
            )

            delay = random.randint(15, 30)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario. Cerrando producer compacto...")
    finally:
        producer.flush()
        producer.close()
        print("Producer compacto cerrado.")


if __name__ == "__main__":
    main()
