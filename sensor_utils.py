import random

# Direcciones de viento posibles
WIND_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]

# Mapas para codificar/decodificar direcciones en 3 bits
WIND_TO_CODE = {d: i for i, d in enumerate(WIND_DIRECTIONS)}
CODE_TO_WIND = {i: d for d, i in WIND_TO_CODE.items()}


def generate_measurement():
    """Genera una medición simulada de la estación meteorológica.

    - temperatura: float [0, 110] °C, con distribución aproximadamente normal
    - humedad: int [0, 100] %
    - dirección del viento: una de las 8 direcciones posibles
    """
    # Temperatura: media 25°C, desviación 10°C, recortado al rango [0, 110]
    temp = random.gauss(25.0, 10.0)
    temp = max(0.0, min(110.0, temp))

    # Humedad: media 60%, desviación 20%, recortado a [0, 100]
    hum = int(round(random.gauss(60.0, 20.0)))
    hum = max(0, min(100, hum))

    # Dirección de viento uniforme sobre las 8 opciones
    wind = random.choice(WIND_DIRECTIONS)

    return {
        "temperatura": round(temp, 2),
        "humedad": hum,
        "direccion_viento": wind,
    }


def encode_measurement_to_bytes(measurement):
    """Codifica una medición (temperatura, humedad, dirección) en 3 bytes (24 bits).

    Diseño de los 24 bits (de más significativo a menos significativo):

    - 14 bits: temperatura * 100  (0.00 a 110.00 -> 0 a 11000)
    - 7 bits: humedad (0 a 100)
    - 3 bits: dirección del viento (0 a 7)

    Estructura (bit 23 = MSB, bit 0 = LSB):

    [ temp(14 bits) ][ hum(7 bits) ][ wind(3 bits) ]
    """
    temp = float(measurement["temperatura"])
    hum = int(measurement["humedad"])
    wind = measurement["direccion_viento"]

    # Asegurar rangos
    temp = max(0.0, min(110.0, temp))
    hum = max(0, min(100, hum))
    wind_code = WIND_TO_CODE.get(wind, 0)

    # Escalar temperatura a centésimas para conservar dos decimales
    temp_code = int(round(temp * 100))  # 0 .. 11000
    # 14 bits permiten hasta 2^14 - 1 = 16383, suficiente para 11000

    # Empaquetar en un entero de 24 bits
    code = (temp_code << (7 + 3)) | (hum << 3) | wind_code

    # Convertir a 3 bytes (big-endian)
    return code.to_bytes(3, byteorder="big")


def decode_bytes_to_measurement(payload_bytes):
    """Decodifica los 3 bytes (24 bits) a un diccionario con:

    - temperatura (float con 2 decimales)
    - humedad (int)
    - direccion_viento (str)
    """
    if len(payload_bytes) != 3:
        raise ValueError(f"Se esperaban 3 bytes, se recibieron {len(payload_bytes)}")

    code = int.from_bytes(payload_bytes, byteorder="big")

    # Extraer campos
    wind_code = code & 0b111  # últimos 3 bits
    hum = (code >> 3) & 0b1111111  # siguientes 7 bits
    temp_code = code >> 10  # los 14 bits restantes

    temp = temp_code / 100.0
    wind = CODE_TO_WIND.get(wind_code, "N")

    return {
        "temperatura": round(temp, 2),
        "humedad": hum,
        "direccion_viento": wind,
    }


if __name__ == "__main__":
    # Pequeña prueba local
    m = generate_measurement()
    print("Medición original:", m)
    b = encode_measurement_to_bytes(m)
    print("Bytes codificados:", b, " (hex:", b.hex(), ")")
    dec = decode_bytes_to_measurement(b)
    print("Medición decodificada:", dec)
