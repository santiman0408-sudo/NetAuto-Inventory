# NetAuto-Inventory

**Automatización de inventario mediante Python y API REST segura (HTTPS)**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![API REST](https://img.shields.io/badge/API-REST-green.svg)](https://jsonplaceholder.typicode.com/)
[![HTTPS](https://img.shields.io/badge/Conexi%C3%B3n-HTTPS-brightgreen.svg)](https://developer.mozilla.org/es/docs/Web/HTTP/Overview)

## 1. Descripción del proyecto

NetAuto-Inventory es un proyecto académico de automatización desarrollado en Python para consultar información desde una API REST mediante una conexión HTTPS, procesar los datos recibidos en formato JSON y generar reportes en formatos JSON y CSV.

El proyecto permite practicar conceptos fundamentales de automatización, administración de archivos en Linux, integración con servicios web, control de versiones con Git y validación del funcionamiento mediante pruebas automatizadas.

Para las pruebas se utiliza la API pública JSONPlaceholder. Los registros obtenidos son datos de demostración y no representan dispositivos reales de una infraestructura de red.

## 2. Objetivos

### Objetivo general

Desarrollar una solución de automatización con Python que consulte una API REST segura, procese información estructurada y genere reportes reutilizables.

### Objetivos específicos

- Consumir una API REST mediante HTTPS.
- Procesar respuestas en formato JSON.
- Generar archivos JSON y CSV.
- Implementar validaciones y manejo de errores HTTP y de conexión.
- Aplicar buenas prácticas de organización del código.
- Gestionar versiones y cambios mediante Git y GitHub.
- Ejecutar pruebas automatizadas para validar el procesamiento de datos.

## 3. Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python | Desarrollo del script de automatización |
| Requests | Consumo de la API REST |
| JSON | Almacenamiento de la respuesta recibida |
| CSV | Generación del reporte tabular |
| Linux / Ubuntu | Entorno de ejecución |
| Git | Control de versiones |
| GitHub | Alojamiento del repositorio |
| unittest | Pruebas automatizadas |
| DEVASC VM | Entorno de laboratorio |

## 4. Requisitos previos

- Python 3.8 o superior.
- Git.
- Acceso a Internet.
- Una terminal Linux o un entorno compatible.
- La dependencia `requests`.

El proyecto se desarrolló y probó en DEVASC VM, utilizando Python 3.8.2.

## 5. Estructura del proyecto

```text
NetAuto-Inventory/
├── src/
│   └── inventory.py
├── tests/
│   └── test_inventory.py
├── data/
│   └── inventory.json
├── reports/
│   └── inventory_report.csv
├── .gitignore
├── requirements.txt
└── README.md
```

**Descripción de los componentes:**

- `src/inventory.py`: consulta la API, valida la respuesta y genera los archivos.
- `tests/test_inventory.py`: contiene las pruebas automatizadas.
- `data/inventory.json`: almacena los datos JSON recibidos.
- `reports/inventory_report.csv`: contiene el reporte tabular.
- `.gitignore`: evita versionar el entorno virtual y los archivos generados.
- `requirements.txt`: registra las dependencias de Python.
- `README.md`: documenta la instalación, ejecución y funcionamiento.

Los directorios y archivos de resultados pueden crearse al ejecutar el programa. Los archivos generados están excluidos del control de versiones mediante `.gitignore`.

## 6. Instalación y configuración

### 6.1. Clonar el repositorio

```bash
git clone https://github.com/santiman0408-sudo/NetAuto-Inventory.git
cd NetAuto-Inventory
```

### 6.2. Crear un entorno virtual

```bash
python3 -m venv .venv
```

Activar el entorno virtual:

```bash
source .venv/bin/activate
```

### 6.3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

Si necesitas instalar únicamente la dependencia principal en un entorno compatible con Python 3.8:

```bash
python -m pip install "requests<2.32"
```

### 6.4. Verificar la instalación

```bash
python --version
python -m pip show requests
git --version
```

## 7. Ejecución del programa

Desde la raíz del repositorio, con el entorno virtual activado, ejecutar:

```bash
python -m py_compile src/inventory.py
python src/inventory.py
```

El programa realiza las siguientes operaciones:

1. Verifica que la URL configurada utilice HTTPS.
2. Envía una solicitud GET a la API REST.
3. Comprueba el estado de la respuesta HTTP.
4. Valida que la respuesta contenga datos JSON con la estructura esperada.
5. Guarda los datos originales en `data/inventory.json`.
6. Procesa los registros para obtener los campos del reporte.
7. Genera `reports/inventory_report.csv`.
8. Muestra un resumen de la ejecución.

### Cambiar la URL de la API

La URL se puede configurar mediante la variable de entorno `INVENTORY_API_URL`. Si no se define, el programa utiliza:

```text
https://jsonplaceholder.typicode.com/users
```

Para probar un recurso inexistente y comprobar el manejo del error HTTP 404:

```bash
INVENTORY_API_URL="https://jsonplaceholder.typicode.com/recurso-inexistente" python src/inventory.py
```

Esta prueba debe registrar el error HTTP y terminar con un código de salida distinto de cero.

## 8. Formatos de datos

### JSON

El archivo `data/inventory.json` conserva la respuesta recibida de la API en formato JSON, facilitando su consulta y reutilización.

### CSV

El archivo `reports/inventory_report.csv` contiene las siguientes columnas:

| Campo | Descripción |
|---|---|
| `id` | Identificador del registro |
| `nombre` | Nombre del usuario de demostración |
| `usuario` | Nombre de usuario |
| `correo` | Correo electrónico de demostración |
| `empresa` | Nombre de la empresa indicada en la respuesta |
| `ciudad` | Ciudad indicada en la dirección |
| `estado` | Estado fijo de demostración (`DEMO`) |

**Importante:** el campo `estado` tiene valor `DEMO`. No representa el estado operativo de un router, switch, servidor u otro dispositivo real.

## 9. Manejo de errores

El programa contempla diferentes situaciones de error:

- **Timeout:** la API no responde dentro del tiempo establecido.
- **Error TLS/SSL:** problemas relacionados con la conexión segura.
- **Error HTTP:** respuestas como 404 u otros estados HTTP no exitosos.
- **Error de conexión:** fallos de comunicación con el servicio.
- **Error de validación:** respuesta con formato o estructura inesperados.
- **Error de archivos:** problemas al crear o escribir los reportes.

Los errores se registran mediante el módulo `logging`, y el programa devuelve un código de salida distinto de cero cuando la ejecución falla.

## 10. Pruebas automatizadas

Para ejecutar las pruebas:

```bash
python -m unittest discover -s tests -v
```

Las pruebas implementadas verifican:

1. El procesamiento correcto de un registro.
2. El comportamiento ante una lista vacía.
3. El procesamiento de registros con campos ausentes.

En la ejecución documentada durante el desarrollo, las tres pruebas finalizaron correctamente.

## 11. Control de versiones con Git

Consultar el estado del repositorio:

```bash
git status
```

Consultar el historial de cambios:

```bash
git log --oneline
```

Consultar las ramas y su seguimiento remoto:

```bash
git branch -vv
```

El repositorio remoto se encuentra disponible en:

**https://github.com/santiman0408-sudo/NetAuto-Inventory**

Para publicar cambios posteriores:

```bash
git add README.md
git commit -m "Agregar documentacion del proyecto"
git push
```

## 12. Seguridad y buenas prácticas

- Utilizar HTTPS para la comunicación con la API.
- Establecer un tiempo máximo de espera en las solicitudes.
- Validar las respuestas HTTP y la estructura de los datos.
- Mantener las dependencias registradas en `requirements.txt`.
- Utilizar un entorno virtual para aislar las dependencias.
- Excluir `.venv/`, archivos temporales y resultados generados del repositorio.
- No almacenar contraseñas, tokens de acceso ni credenciales en el código fuente.
- No compartir tokens personales de GitHub en capturas, documentos o repositorios.
- Utilizar datos de demostración cuando no se disponga de una API de inventario real.

## 13. Limitaciones y mejoras futuras

La versión actual utiliza JSONPlaceholder como fuente de datos de prueba. Por tanto, demuestra la integración con una API REST y el procesamiento automatizado de información, pero todavía no consulta directamente dispositivos de red.

Como mejoras futuras se propone:

- Integrar una API de gestión de infraestructura de red real.
- Incorporar campos específicos de routers, switches, interfaces y direcciones IP.
- Añadir pruebas automatizadas para la consulta HTTP y la generación de archivos.
- Incorporar validaciones adicionales de datos.
- Añadir ejecución automatizada mediante un flujo de integración continua.
- Implementar mecanismos de autenticación cuando la API real los requiera.

## 14. Conclusiones

NetAuto-Inventory demuestra la aplicación de Python para automatizar la consulta y transformación de datos obtenidos desde una API REST segura. La generación de archivos JSON y CSV facilita el almacenamiento y análisis de la información, mientras que las validaciones, el registro de errores y las pruebas automatizadas mejoran la confiabilidad del programa.

El uso de DEVASC VM, Linux, Git y GitHub permite integrar prácticas de desarrollo y administración de sistemas en un entorno de laboratorio.

**Repositorio:** https://github.com/santiman0408-sudo/NetAuto-Inventory
