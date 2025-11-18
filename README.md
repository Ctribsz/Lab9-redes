# Laboratorio 9 - Estación Meteorológica (Kafka + IoT)

Este proyecto contiene una solución completa en Python para el Laboratorio 9 de Redes:
simulación de una estación meteorológica usando Apache Kafka como broker de mensajes.

## Estructura

- `sensor_utils.py`
  - Generación de mediciones simuladas (temperatura, humedad, dirección del viento).
  - Funciones de codificación/decodificación a un payload compacto de 3 bytes.

- `producer_json.py`
  - Producer que envía mediciones en formato JSON al servidor Kafka.

- `consumer_json_plot.py`
  - Consumer que lee mediciones JSON, las acumula y genera gráficas en vivo.

- `producer_compacto.py`
  - Producer que envía las mismas mediciones pero codificadas en un payload de 3 bytes.

- `consumer_compacto_plot.py`
  - Consumer que lee los 3 bytes, decodifica y vuelve a graficar los datos.

- `requirements.txt`
  - Dependencias de Python para instalar con `pip`.

## Configuración del servidor Kafka

El laboratorio ya provee un servidor Kafka:

- Host: `lab9.alumchat.lol`
- Puerto: `9092` (estándar de Kafka)

En todo el código, esto se refleja en:

```python
BOOTSTRAP_SERVERS = ["lab9.alumchat.lol:9092"]
```

## Antes de correr

1. Instalar dependencias (se recomienda un entorno virtual):

   ```bash
   pip install -r requirements.txt
   ```

2. Editar los archivos:
   - `producer_json.py`
   - `consumer_json_plot.py`
   - `producer_compacto.py`
   - `consumer_compacto_plot.py`

   y reemplazar la línea:

   ```python
   TOPIC = "2020xxxx"
   ```

   por tu número de carné, por ejemplo:

   ```python
   TOPIC = "20201234"
   ```

   Cada pareja debe usar un topic único (el carné de alguno de los integrantes).

## Ejecución (versión JSON)

1. En una terminal:

   ```bash
   python producer_json.py
   ```

2. En otra terminal:

   ```bash
   python consumer_json_plot.py
   ```

Verás en consola los mensajes enviados/recibidos y una ventana con gráficas de:
- Temperatura vs muestras
- Humedad vs muestras
- Dirección del viento vs muestras

Toma capturas de:
- Consola del producer
- Consola del consumer
- Gráfica

para tu reporte.

## Ejecución (versión compacta, payload de 3 bytes)

1. En una terminal:

   ```bash
   python producer_compacto.py
   ```

2. En otra terminal:

   ```bash
   python consumer_compacto_plot.py`
   ```

En esta versión, el producer envía solo 3 bytes por mensaje y el consumer los decodifica
de regreso a temperatura, humedad y dirección del viento usando `sensor_utils.py`.

También deberás tomar capturas de:
- Consola del producer compacto (se ven los bytes en hex)
- Consola del consumer compacto
- Gráfica de la versión compacta

## Notas para el informe

- Explica cómo se generan los datos (distribuciones, rangos, etc.).
- Describe la arquitectura: Producer → Kafka (Edge) → Consumer + gráfica.
- Justifica el diseño del payload de 24 bits (14 bits temp, 7 bits humedad, 3 bits viento).
- Incluye las respuestas teóricas que pide el enunciado.
