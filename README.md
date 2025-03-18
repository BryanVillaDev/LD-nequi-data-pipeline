# LD-nequi-data-pipeline

Este repositorio implementa un pipeline de datos moderno utilizando AWS, Airflow, AWS Glue (PySpark) y Terraform, aplicando buenas prácticas como TDD, SOLID y Clean Architecture.

## Estructura del Proyecto

```bash
Proyecto/
├── README.md                # Este documento
├── docs/                    # Documentación, diagramas y modelo operativo
│   ├── draft_prueba_concepto.md
│   └── modelo_operativo.md
├── airflow/                 # Código y configuración de Airflow
│   ├── dags/                # DAGs (e.g., transactions_etl.py)
│   └── plugins/             # Operadores y hooks personalizados
├── glue/                    # Scripts de AWS Glue y tests
│   ├── scripts/             # Script de ETL en PySpark (script_pyspark.py)
│   └── tests/               # Tests del proceso ETL (test_script_pyspark.py)
├── notifications/           # Módulo de notificaciones (notifier.py)
├── terraform/               # Infraestructura como código (Terraform)
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ci/                      # Pipelines de CI/CD para despliegue
│   └── workflows/
│       ├── deploy_dag_to_s3.yml
│       ├── deploy_glue_job.yml
│       └── terraform.yml
└── data/                   # Archivos de datos (e.g., transactions.csv)
```

## Componentes Principales

### Airflow
- **DAGs**  
  El DAG principal se encuentra en [airflow/dags/transactions_etl.py](airflow\dags\transactions_etl.py) y orquesta el proceso ETL mediante AWS Glue. Incluye notificaciones por email en caso de falla.

### AWS Glue (PySpark)
- **Script ETL**  
  El proceso ETL se implementa en [glue/scripts/script_pyspark.py](glue\scripts\script_pyspark.py), donde se cargan, transforman y guardan los datos.  
- **Tests**  
  Los tests para validar las transformaciones se encuentran en [glue/tests/test_script_pyspark.py](glue\tests\test_script_pyspark.py).

### Notificaciones
- **Notifier**  
  El modulo en [notifications/notifier.py](notifications\notifier.py) gestiona el envo de alertas (por email, Slack, Teams) ante incidencias.

### Infraestructura
- **Terraform**  
  Los archivos de Terraform para crear y gestionar la infraestructura están en [terraform/main.tf](terraform\main.tf), [terraform/variables.tf](terraform\variables.tf) y [terraform/outputs.tf](terraform\outputs.tf).

### CI/CD
- **Workflows de GitHub Actions**  
  Se han definido pipelines de CI/CD para:
  - Desplegar DAGs en S3: [ci/workflows/deploy_dag_to_s3.yml](ci\workflows\deploy_dag_to_s3.yml)
  - Desplegar jobs de Glue: [ci/workflows/deploy_glue_job.yml](ci\workflows\deploy_glue_job.yml)
  - Gestionar despliegues de Terraform: [ci/workflows/terraform.yml](ci\workflows\terraform.yml)

## Modelo Operativo

El [modelo operativo](docs\modelo_operativo.md) define los procesos, roles y flujos de trabajo para la ingesta, procesamiento, análisis y despliegue de datos en el pipeline.

## Uso y Ejecución

1. **Airflow**: Ejecuta los DAGs para orquestar las tareas ETL.
2. **AWS Glue**: Actualiza y testea los scripts ETL en PySpark.
3. **Terraform**: Despliega y actualiza la infraestructura mediante GitHub Actions.
4. **Notificaciones**: Configura el módulo notifier para recibir alertas sobre fallos en el pipeline.

## Configuración del Entorno de Python

Para configurar un entorno virtual y gestionar las dependencias, sigue estos pasos:

1. Abre una terminal en la raíz del proyecto.
2. Crea un entorno virtual:
    ```sh
    python -m venv venv
    ```
3. Activa el entorno virtual:
    En Windows:
    ```sh
    venv\Scripts\activate
    ```
4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

`requirements.txt` con las librerías necesarias.
...
 configurar las variables de entorno `INPUT_PATH` y `OUTPUT_PATH`.
