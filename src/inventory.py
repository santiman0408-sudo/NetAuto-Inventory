
#!/usr/bin/env python3
"""Automatizacion de inventario mediante una API REST segura."""

import csv
import json
import logging
import sys
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

API_URL = "https://jsonplaceholder.typicode.com/users"
TIMEOUT = 15

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def consultar_api():
    """Consulta la API y valida la respuesta JSON."""
    respuesta = requests.get(
        API_URL,
        headers={"Accept": "application/json"},
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()

    if "json" not in respuesta.headers.get("Content-Type", "").lower():
        raise ValueError("La respuesta no contiene JSON.")

    datos = respuesta.json()

    if not isinstance(datos, list):
        raise ValueError("Se esperaba una lista de registros.")

    for registro in datos:
        if not isinstance(registro, dict):
            raise ValueError("Se encontro un registro invalido.")

    return datos


def guardar_json(datos):
    """Guarda los datos originales recibidos."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    ruta = DATA_DIR / "inventory.json"
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)

    return ruta


def procesar_inventario(datos):
    """Extrae los campos necesarios para el reporte."""
    inventario = []

    for registro in datos:
        empresa = registro.get("company") or {}
        direccion = registro.get("address") or {}

        inventario.append({
            "id": registro.get("id", ""),
            "nombre": registro.get("name", ""),
            "usuario": registro.get("username", ""),
            "correo": registro.get("email", ""),
            "empresa": empresa.get("name", ""),
            "ciudad": direccion.get("city", ""),
            "estado": "DEMO",
        })

    return inventario


def guardar_csv(inventario):
    """Exporta el inventario a formato CSV."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ruta = REPORT_DIR / "inventory_report.csv"

    columnas = [
        "id", "nombre", "usuario", "correo",
        "empresa", "ciudad", "estado",
    ]

    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(inventario)

    return ruta


def main():
    try:
        logger.info("Consultando API mediante HTTPS...")
        datos = consultar_api()

        ruta_json = guardar_json(datos)
        inventario = procesar_inventario(datos)
        ruta_csv = guardar_csv(inventario)

        print("\n=== RESUMEN DEL INVENTARIO ===")
        print("Registros recibidos:", len(datos))
        print("Registros procesados:", len(inventario))
        print("Archivo JSON:", ruta_json)
        print("Archivo CSV:", ruta_csv)

        return 0

    except requests.exceptions.Timeout:
        logger.error("Tiempo de espera agotado.")
    except requests.exceptions.SSLError:
        logger.error("Error SSL/TLS al verificar la conexion.")
    except requests.exceptions.HTTPError as error:
        logger.error("Error HTTP: %s", error)
    except requests.exceptions.RequestException as error:
        logger.error("Error de conexion: %s", error)
    except (ValueError, json.JSONDecodeError) as error:
        logger.error("Error al procesar los datos: %s", error)
    except OSError as error:
        logger.error("Error al escribir archivos: %s", error)

    return 1


if __name__ == "__main__":
    sys.exit(main())
