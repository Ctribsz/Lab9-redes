import json
from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from sensor_utils import WIND_DIRECTIONS

# ⚠️ CAMBIA ESTO POR TU CARNÉ (igual que en el producer)
TOPIC = "2020xxxx"

# Servidor de Kafka proporcionado en el laboratorio
BOOTSTRAP_SERVERS = ["lab9.alumchat.lol:9092"]


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",  # para ver datos históricos también
        enable_auto_commit=True,
        group_id="grupo_estacion_json",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    print(f"Consumer JSON escuchando el topic {TOPIC}... Ctrl+C para detener.\n")

    # Listas para ir acumulando datos
    all_temp = []
    all_hume = []
    all_wind = []

    # Preparar figura
    plt.ion()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    while True:
        try:
            for msg in consumer:
                payload = msg.value  # dict con temperatura, humedad, direccion_viento
                temp = payload["temperatura"]
                hum = payload["humedad"]
                wind = payload["direccion_viento"]

                all_temp.append(temp)
                all_hume.append(hum)
                all_wind.append(wind)

                print(
                    f"Recibido offset={msg.offset}: "
                    f"T={temp} °C, H={hum} %, Viento={wind}"
                )

                # Actualizar la gráfica
                x = list(range(1, len(all_temp) + 1))

                # Temperatura
                ax1.clear()
                ax1.plot(x, all_temp, marker="o")
                ax1.set_ylabel("Temp (°C)")
                ax1.set_title("Temperatura vs muestras")
                ax1.grid(True)

                # Humedad
                ax2.clear()
                ax2.plot(x, all_hume, marker="o")
                ax2.set_ylabel("Humedad (%)")
                ax2.set_title("Humedad vs muestras")
                ax2.grid(True)

                # Dirección del viento (codificada como entero)
                ax3.clear()
                wind_codes = [WIND_DIRECTIONS.index(w) for w in all_wind]
                ax3.step(x, wind_codes, where="mid")
                ax3.set_yticks(range(len(WIND_DIRECTIONS)))
                ax3.set_yticklabels(WIND_DIRECTIONS)
                ax3.set_ylabel("Viento")
                ax3.set_xlabel("Muestra")
                ax3.set_title("Dirección del viento")
                ax3.grid(True)

                plt.tight_layout()
                plt.pause(0.1)

        except KeyboardInterrupt:
            print("\nConsumer interrumpido por el usuario.")
            break

    plt.ioff()
    plt.show()
    consumer.close()
    print("Consumer cerrado.")


if __name__ == "__main__":
    main()
