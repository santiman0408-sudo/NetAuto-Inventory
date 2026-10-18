
#!/usr/bin/env python3
"""Automatizacion de inventario mediante una API REST segura."""

import csv
import json
import logging
import sys
import os
#!/usr/bin/env python3
"""
Automatizacion de inventario mediante una API REST segura.
Consulta datos JSON y genera reportes JSON y CSV.
"""

import csv
import json
import logging
import os
import sys
from pathlib import Path

import requests


# ============================================================
# CONFIGURACION GENERAL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Permite cambiar la URL durante las pruebas sin editar el codigo.
API_URL = os.getenv(
    "INVENTORY_API_URL",
    "https://jsonplaceholder.typicode.com/users",
)

TIMEOUT = 15

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# CONSULTA DE LA API REST
# ============================================================

def consultar_api():
    """Consulta la API mediante HTTPS y valida la respuesta."""

    if not API_URL.lower().startswith("https://"):
        raise ValueError("La URL de la API debe utilizar HTTPS.")

    logger.info("Consultando API mediante HTTPS: %s", API_URL)

    respuesta = requests.get(
        API_URL,
        headers={"Accept": "application/json"},
        timeout=TIMEOUT,
    )

    # Genera una excepcion si la respuesta HTTP indica un error.
    respuesta.raise_for_status()

    # Verifica que el servidor haya respondido con JSON.
    content_type = respuesta.headers.get("Content-Type", "")

    if "json" not in content_type.lower():
        raise ValueError("La respuesta no contiene JSON.")

    datos = respuesta.json()

    if not isinstance(datos, list):
        raise ValueError("Se esperaba una lista de registros JSON.")

    for registro in datos:
        if not isinstance(registro, dict):
            raise ValueError("Se encontro un registro JSON invalido.")

    logger.info("Registros recibidos: %d", len(datos))

    return datos


# ============================================================
# ALMACENAMIENTO DE DATOS JSON
# ============================================================

def guardar_json(datos):
    """Guarda los datos originales recibidos desde la API."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    ruta_json = DATA_DIR / "inventory.json"

    with ruta_json.open("w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=2,
        )

    logger.info("Archivo JSON generado: %s", ruta_json)

    return ruta_json


# ============================================================
# PROCESAMIENTO DEL INVENTARIO
# ============================================================

def procesar_inventario(datos):
    """Extrae y organiza los campos necesarios para el reporte."""

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


# ============================================================
# EXPORTACION A CSV
# ============================================================

def guardar_csv(inventario):
    """Exporta los registros procesados a un archivo CSV."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    ruta_csv = REPORT_DIR / "inventory_report.csv"

    columnas = [
        "id",
        "nombre",
        "usuario",
        "correo",
        "empresa",
        "ciudad",
        "estado",
    ]

    with ruta_csv.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas,
        )

        escritor.writeheader()
        escritor.writerows(inventario)

    logger.info("Archivo CSV generado: %s", ruta_csv)

    return ruta_csv


# ============================================================
# EJECUCION PRINCIPAL Y GESTION DE ERRORES
# ============================================================

def main():
    """Ejecuta el proceso completo de automatizacion."""

    try:
        datos = consultar_api()

        ruta_json = guardar_json(datos)

        inventario = procesar_inventario(datos)

        ruta_csv = guardar_csv(inventario)

        print("\n=== RESUMEN DEL INVENTARIO ===")
        print("------------------------------")
        print("Registros recibidos:", len(datos))
        print("Registros procesados:", len(inventario))
        print("Archivo JSON:", ruta_json)
        print("Archivo CSV:", ruta_csv)
        print("Estado de los registros: DEMO")

        return 0

    except requests.exceptions.Timeout:
        logger.error("Tiempo de espera agotado al consultar la API.")
        return 1

    except requests.exceptions.SSLError:
        logger.error(
            "Error TLS/SSL: verifica certificados y fecha del sistema."
        )
        return 1

    except requests.exceptions.HTTPError as error:
        codigo = error.response.status_code
        logger.error("Error HTTP %s: %s", codigo, error)
        return 1

    except requests.exceptions.RequestException as error:
        logger.error("Error de conexion con la API: %s", error)
        return 1

    except (ValueError, json.JSONDecodeError) as error:
        logger.error("Error de validacion de datos: %s", error)
        return 1

    except OSError as error:
        logger.error("Error de acceso a archivos: %s", error)
        return 1


if __name__ == "__main__":
    sys.exit(main())

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
